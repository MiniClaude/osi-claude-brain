"""
OSI Email Validator. Single source of truth for hard-stop checks before queue write.

Called by every drafting skill (osi-outreach-sequence, osi-3email-new,
osi-3email-reengagement, osi-old-customer-reengagement, osi-cold-reengagement,
osi-email-task-drafts, osi-email2-rewriter) BEFORE writing to email-queue.json.

Also called by osi-email-sender at send time as belt-and-suspenders, in case a
queue entry was hand-edited and bypassed the write-time validator.

Also called by osi-monitor's weekly audit pass over the last 7 days of sent
emails to catch drift.

The rules live in plain English at C:\\Claude-Brain\\playbook\\drafting-rules.md.
This file enforces them in code.

Hygiene: this source file contains ZERO literal em-dashes (U+2014) and ZERO
literal en-dashes (U+2013). Both characters are constructed via chr() so the
file itself can't accidentally pass dashes through.
"""

import re
import json
import os
from typing import List, Dict, Optional

EM_DASH = chr(0x2014)
EN_DASH = chr(0x2013)


# Banned vocabulary (case-insensitive whole-word match).
BANNED_VOCAB = [
    "crucial",
    "pivotal",
    "landscape",
    "underscore",
    "delve",
    "showcase",
    "testament",
    "enhance",
    "foster",
    "garner",
    "leverage",
    "leveraging",
    "leveraged",
    "unlock",
    "unlocks",
    "unlocking",
    "supercharge",
    "supercharges",
    "supercharging",
    "revolutionize",
    "revolutionizes",
    "revolutionizing",
    "seamless",
    "seamlessly",
    "robust",
    "holistic",
    "synergy",
    "synergies",
    "cutting edge",
    "cutting-edge",
    "best in class",
    "best-in-class",
    "world class",
    "world-class",
]


# Dead phrases (case-insensitive substring match).
DEAD_PHRASES = [
    "worth a conversation",
    "would this be worth",
    "worth 15 minutes",
    "worth a few minutes",
    "worth fifteen minutes",
    "quick overview",
    "brief overview",
    "touch base",
    "ping you",
    "pick your brain",
    "hop on a call",
    "hop on a quick call",
    "jump on a call",
    "jump on a quick call",
    "circle back",  # OK in re-engagement; caller can pass allow_circle_back=True
]


# Forbidden cold-opener patterns (regex, case-insensitive, anchored at start of body).
# Only checked for email_index == 1 in cold sequences.
COLD_OPENER_PATTERNS = [
    r"^\s*(?:Hi|Hello|Hey)?\s*[A-Z][a-z]+\s*,?\s*\n+\s*I'?m\s+Andy",
    r"^\s*(?:Hi|Hello|Hey)?\s*[A-Z][a-z]+\s*,?\s*\n+\s*I\s+am\s+Andy",
    r"^\s*(?:Hi|Hello|Hey)?\s*[A-Z][a-z]+\s*,?\s*\n+\s*I'?m\s+(?:with|at)\s+OSI",
    r"^\s*(?:Hi|Hello|Hey)?\s*[A-Z][a-z]+\s*,?\s*\n+\s*I\s+am\s+(?:with|at)\s+OSI",
    r"^\s*(?:Hi|Hello|Hey)?\s*[A-Z][a-z]+\s*,?\s*\n+\s*I\s+work\s+with\s+(?:IT|infrastructure|network|telecom|data center|cloud)",
    r"^\s*(?:Hi|Hello|Hey)?\s*[A-Z][a-z]+\s*,?\s*\n+\s*I\s+help\s+(?:IT|infrastructure|network|telecom|data center|cloud)",
    r"^\s*(?:Hi|Hello|Hey)?\s*[A-Z][a-z]+\s*,?\s*\n+\s*I\s+wanted\s+to\s+reach\s+out",
    r"^\s*(?:Hi|Hello|Hey)?\s*[A-Z][a-z]+\s*,?\s*\n+\s*I'?m\s+reaching\s+out",
]


# Forbidden manufacturing claims (case-insensitive substring).
MANUFACTURE_CLAIMS = [
    "we manufacture",
    "manufactured by us",
    "manufactured by OSI",
    "OSI manufactures",
    "we make our own optics",
    "we make our optics",
    "we produce our own",
    "we build our own optics",
    "OSI builds the",
    "we build the optics",
]


# Hyphen-allowed tokens. The validator scans for hyphens; if a hyphen appears
# inside any token in this list, it's allowed.
HYPHEN_ALLOWLIST = [
    "QSFP-DD",
    "QSFP-DD800",
    "Wi-Fi",
    "ZR-",  # ZR-something is allowed (ZR plus modifier); plain ZR is fine without hyphen.
    "Tier-1",
    "Tier-2",
    "Tier-3",
    "co-located",  # technical term, OK
    "DC-",  # DC-prefix tokens like DC-001 in some product lines
    # Don't include "third-party" here. Voice rules say "third party".
    # Don't include "end-of-life". Voice rules say "end of life".
    # Don't include "multi-vendor". Voice rules say "multi vendor".
]


# Word-count limits per email index.
WORD_LIMITS = {
    1: 90,
    2: 50,
    3: 80,
    4: 80,
    5: 80,
    6: 30,  # Breakup email is short.
}


# Product-line keyword clusters. If two or more clusters appear in one body,
# Surgical Isolation is violated (one product line per email).
PRODUCT_LINE_KEYWORDS = {
    "optics": ["transceiver", "transceivers", "SFP", "QSFP", "optic", "optics", "SFP+"],
    "dwdm": ["DWDM", "ZR/ZR+", "coherent", "open line system", "wavelength", "DCP-"],
    "compute": ["DIMM", "DIMMs", "RAM", "memory", "DDR4", "DDR5", "server refresh", "Samsung", "Hynix", "Micron"],
    "storage": ["pre-owned NetApp", "NetApp storage", "NetApp gear", "storage refresh", "storage gear", "storage hardware", "FAS-", "AFF-"],
    "tpm": ["TPM", "third party maintenance", "third-party maintenance", "OEM support", "SmartNet", "ProSupport", "maintenance contract", "maintenance renewal", "TPM coverage"],
    "preowned": ["pre-owned Cisco", "pre-owned Juniper", "pre-owned Arista", "Nokia networking"],
    "proserv": ["professional services", "deployment support", "smart hands", "Smarthands"],
}


def _word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text or ""))


def _check_dashes(body: str, subject: str) -> List[Dict]:
    """Section 1.1, NO em-dashes or en-dashes anywhere."""
    violations = []
    if EM_DASH in body:
        violations.append({
            "rule": "1.1-em-dash-in-body",
            "severity": "abort",
            "detail": f"Em-dash (U+2014) present in body. Replace with period or comma.",
        })
    if EN_DASH in body:
        violations.append({
            "rule": "1.1-en-dash-in-body",
            "severity": "abort",
            "detail": f"En-dash (U+2013) present in body. Replace with period or comma.",
        })
    if EM_DASH in (subject or ""):
        violations.append({
            "rule": "1.1-em-dash-in-subject",
            "severity": "abort",
            "detail": f"Em-dash (U+2014) present in subject.",
        })
    if EN_DASH in (subject or ""):
        violations.append({
            "rule": "1.1-en-dash-in-subject",
            "severity": "abort",
            "detail": f"En-dash (U+2013) present in subject.",
        })
    return violations


def _check_smartoptics_in_cold(body: str, subject: str, email_index: int, is_cold: bool) -> List[Dict]:
    """Section 1.2, NO SmartOptics by name in cold outreach."""
    violations = []
    if not is_cold:
        return violations
    pattern = re.compile(r"\bsmart\s*optics\b", re.IGNORECASE)
    if pattern.search(body):
        violations.append({
            "rule": "1.2-smartoptics-in-cold-body",
            "severity": "abort",
            "detail": f"'SmartOptics' appears in body of cold Email {email_index}. Refer to optics as 'OSI transceivers'.",
        })
    if pattern.search(subject or ""):
        violations.append({
            "rule": "1.2-smartoptics-in-cold-subject",
            "severity": "abort",
            "detail": "'SmartOptics' appears in subject of cold email.",
        })
    return violations


def _check_manufacture_claims(body: str) -> List[Dict]:
    """Section 1.3, NO 'we manufacture' claim."""
    violations = []
    body_l = body.lower()
    for phrase in MANUFACTURE_CLAIMS:
        if phrase.lower() in body_l:
            violations.append({
                "rule": "1.3-manufacture-claim",
                "severity": "abort",
                "detail": f"Forbidden manufacturing claim: '{phrase}'. OSI does not manufacture optics. SmartOptics manufactures.",
            })
    return violations


def _check_credentials_opener(body: str, email_index: int) -> List[Dict]:
    """Section 1.4, NO credentials-first openers (Email 1 only)."""
    violations = []
    if email_index != 1:
        return violations
    for pattern in COLD_OPENER_PATTERNS:
        if re.search(pattern, body, re.IGNORECASE | re.MULTILINE):
            violations.append({
                "rule": "1.4-credentials-opener",
                "severity": "abort",
                "detail": f"Email 1 leads with credentials, not pain. Lead with the prospect's Personal Hook. Pattern hit: {pattern[:60]}...",
            })
            break
    return violations


def _check_banned_vocab(body: str, subject: str) -> List[Dict]:
    """Section 1.5, NO banned vocab."""
    violations = []
    body_l = body.lower()
    subject_l = (subject or "").lower()
    for word in BANNED_VOCAB:
        word_l = word.lower()
        # Use whole-word boundary for single words; substring for multi-word phrases.
        if " " in word or "-" in word:
            if word_l in body_l:
                violations.append({
                    "rule": "1.5-banned-vocab-body",
                    "severity": "abort",
                    "detail": f"Banned vocab in body: '{word}'.",
                })
            if word_l in subject_l:
                violations.append({
                    "rule": "1.5-banned-vocab-subject",
                    "severity": "abort",
                    "detail": f"Banned vocab in subject: '{word}'.",
                })
        else:
            if re.search(rf"\b{re.escape(word_l)}\b", body_l):
                violations.append({
                    "rule": "1.5-banned-vocab-body",
                    "severity": "abort",
                    "detail": f"Banned vocab in body: '{word}'.",
                })
            if re.search(rf"\b{re.escape(word_l)}\b", subject_l):
                violations.append({
                    "rule": "1.5-banned-vocab-subject",
                    "severity": "abort",
                    "detail": f"Banned vocab in subject: '{word}'.",
                })
    return violations


def _check_dead_phrases(body: str, subject: str, allow_circle_back: bool = False) -> List[Dict]:
    """Section 1.6, NO dead phrases."""
    violations = []
    body_l = body.lower()
    subject_l = (subject or "").lower()
    for phrase in DEAD_PHRASES:
        if phrase == "circle back" and allow_circle_back:
            continue
        if phrase in body_l:
            violations.append({
                "rule": "1.6-dead-phrase-body",
                "severity": "abort",
                "detail": f"Dead phrase in body: '{phrase}'. Replace with a concrete ask.",
            })
        if phrase in subject_l:
            violations.append({
                "rule": "1.6-dead-phrase-subject",
                "severity": "abort",
                "detail": f"Dead phrase in subject: '{phrase}'.",
            })
    return violations


def _check_hyphens(body: str, subject: str) -> List[Dict]:
    """Section 1.7, NO hyphens in bodies (allowlist below).
    Number ranges (8-10, 40-60%), ISO dates (2026-04-30), and dash runs (3+
    in a row, separately checked) are NOT hyphen-rule violations."""
    violations = []

    def scan(text: str, where: str) -> List[Dict]:
        local_violations = []
        # Find every word containing a hyphen.
        for match in re.finditer(r"\S*-\S*", text):
            token = match.group(0)
            # Strip trailing punctuation.
            token_clean = token.rstrip(".,!?;:'\"")
            if not token_clean:
                continue
            # Skip if the token is 3+ consecutive dashes (a quote separator, handled by _check_quote_leak).
            if re.match(r"^-{3,}$", token_clean):
                continue
            # Skip if the token is a pure number range (e.g., "8-10", "40-60%", "100-200ms").
            if re.match(r"^\d+(\.\d+)?-\d+(\.\d+)?\S*$", token_clean):
                continue
            # Skip if the token is an ISO date (2026-04-30).
            if re.match(r"^\d{4}-\d{2}-\d{2}$", token_clean):
                continue
            # Check against the product-name allowlist (case-insensitive).
            if any(allowed.lower() in token_clean.lower() for allowed in HYPHEN_ALLOWLIST):
                continue
            # Otherwise, violation.
            local_violations.append({
                "rule": f"1.7-hyphen-in-{where}",
                "severity": "abort",
                "detail": f"Hyphen in {where}: '{token_clean}'. Voice rule, no hyphens. Use plain English (e.g., 'third party' not 'third-party').",
            })
        return local_violations

    violations.extend(scan(body, "body"))
    violations.extend(scan(subject or "", "subject"))
    return violations


def _check_quote_leak(body: str, email_index: int) -> List[Dict]:
    """Detects quoted-thread artifacts that leaked into Email 3+ bodies.
    These are STANDALONE fresh-subject emails per Step 4 of osi-outreach-sequence;
    any quote separator or 'On ... wrote:' line is a bug."""
    violations = []
    if email_index < 3:
        return violations  # Email 2 is RE: thread, separators are expected post-send.
    # Long dash runs (used as quote separators).
    if re.search(r"-{5,}", body):
        violations.append({
            "rule": "quote-leak-dashrun",
            "severity": "abort",
            "detail": f"Email {email_index} body contains a 5+ dash run, looks like a quoted-thread separator. Email 3+ are STANDALONE fresh-subject touches; no quoted thread allowed.",
        })
    # 'On <date> ... wrote:' pattern.
    if re.search(r"\nOn .* wrote\s*:?", body):
        violations.append({
            "rule": "quote-leak-onwrote",
            "severity": "abort",
            "detail": f"Email {email_index} body contains 'On ... wrote:' marker. Email 3+ are STANDALONE; strip the quoted prior thread.",
        })
    # '> ' quoted line at start of a line.
    if re.search(r"\n>\s+", body):
        violations.append({
            "rule": "quote-leak-gtprefix",
            "severity": "abort",
            "detail": f"Email {email_index} body contains '> ' quoted lines. Email 3+ are STANDALONE; strip the quoted prior thread.",
        })
    # 'From: Andrew McLean' Outlook reply header in body.
    if "From: Andrew McLean" in body or "From: Andy McLean" in body:
        violations.append({
            "rule": "quote-leak-fromheader",
            "severity": "abort",
            "detail": f"Email {email_index} body contains an Outlook From: header. Strip prior thread.",
        })
    return violations


def _check_andy_signoff(body: str) -> List[Dict]:
    """Section 1.11, NO 'Andy' sign-off."""
    violations = []
    # Look at the last few lines.
    last_lines = body.strip().split("\n")[-3:]
    last_block = "\n".join(last_lines).strip()
    # Patterns like "Andy" alone on a line, or "Best, Andy", "Thanks, Andy", "Cheers, Andy", "- Andy".
    signoff_patterns = [
        r"^\s*Andy\s*$",
        r"^\s*Best,?\s*Andy\s*$",
        r"^\s*Thanks,?\s*Andy\s*$",
        r"^\s*Cheers,?\s*Andy\s*$",
        r"^\s*Regards,?\s*Andy\s*$",
        r"^\s*-\s*Andy\s*$",
    ]
    for line in last_block.split("\n"):
        for pat in signoff_patterns:
            if re.match(pat, line, re.IGNORECASE):
                violations.append({
                    "rule": "1.11-andy-signoff",
                    "severity": "abort",
                    "detail": f"'Andy' sign-off in body: '{line.strip()}'. Outlook signature handles this; remove from body.",
                })
                break
    return violations


def _check_surgical_isolation(body: str) -> List[Dict]:
    """Section 1.12, ONE product line per email."""
    violations = []
    body_l = body.lower()
    matched_clusters = []
    for cluster, keywords in PRODUCT_LINE_KEYWORDS.items():
        for kw in keywords:
            # Use word-boundary match to avoid false substring hits (e.g. "RAM" in "Ramana")
            if re.search(r'\b' + re.escape(kw.lower()) + r'\b', body_l):
                matched_clusters.append(cluster)
                break
    matched_unique = set(matched_clusters)
    if len(matched_unique) >= 2:
        violations.append({
            "rule": "1.12-surgical-isolation",
            "severity": "abort",
            "detail": f"Multiple product lines in one email: {sorted(matched_unique)}. Surgical Isolation rule. One product line per email.",
        })
    return violations


def _check_word_limit(body: str, email_index: int) -> List[Dict]:
    """Section 14, brevity limits."""
    violations = []
    limit = WORD_LIMITS.get(email_index)
    if limit is None:
        return violations
    count = _word_count(body)
    if count > limit:
        violations.append({
            "rule": f"14-word-limit-email-{email_index}",
            "severity": "abort",
            "detail": f"Email {email_index} body is {count} words, limit is {limit}. Tighten.",
        })
    return violations


def _check_negative_parallelism(body: str) -> List[Dict]:
    """Section 1.10, NO negative parallelisms."""
    violations = []
    patterns = [
        (r"it'?s\s+not\s+just\s+\w+,?\s+it'?s\s+\w+", "It's not just X, it's Y"),
        (r"not\s+only\s+\w+\s+but\s+also\s+\w+", "Not only A but also B"),
        (r"less\s+\w+,?\s+more\s+\w+", "Less of X, more of Y"),
    ]
    for pat, label in patterns:
        if re.search(pat, body, re.IGNORECASE):
            violations.append({
                "rule": "1.10-negative-parallelism",
                "severity": "abort",
                "detail": f"Negative parallelism construction: '{label}'. LinkedIn-influencer cadence. Rewrite.",
            })
    return violations


def validate_email(
    body: str,
    subject: str,
    email_index: int,
    is_cold: bool = True,
    allow_circle_back: bool = False,
    company_name: Optional[str] = None,
    sequence_type: Optional[str] = None,
) -> List[Dict]:
    """
    Run all hard-stop checks on a drafted email body and subject.

    Args:
        body: the email body text (no Outlook signature, no quoted thread for Emails 3+).
        subject: the email subject line.
        email_index: 1, 2, 3, 4, 5, or 6.
        is_cold: True for cold sequences (qualification handoff). False for re-engagement
                 of prior customers (where SmartOptics may be named because brand
                 was already established).
        allow_circle_back: True for re-engagement skills only (osi-3email-reengagement,
                           osi-old-customer-reengagement). False for cold.
        company_name: optional, used for company-specific checks if added later.
        sequence_type: optional, used for template-specific checks if added later.

    Returns:
        List of violation dicts. Empty list = passes. Each dict has:
            - rule: the rule ID (e.g. "1.1-em-dash-in-body").
            - severity: "abort" or "warn". The skill MUST refuse to write any entry
                        with severity == "abort".
            - detail: human-readable description for logs.
    """
    violations = []
    violations.extend(_check_dashes(body, subject))
    violations.extend(_check_smartoptics_in_cold(body, subject, email_index, is_cold))
    violations.extend(_check_manufacture_claims(body))
    violations.extend(_check_credentials_opener(body, email_index))
    violations.extend(_check_banned_vocab(body, subject))
    violations.extend(_check_dead_phrases(body, subject, allow_circle_back=allow_circle_back))
    violations.extend(_check_hyphens(body, subject))
    violations.extend(_check_quote_leak(body, email_index))
    violations.extend(_check_andy_signoff(body))
    violations.extend(_check_surgical_isolation(body))
    violations.extend(_check_word_limit(body, email_index))
    violations.extend(_check_negative_parallelism(body))
    return violations


def validate_or_raise(
    body: str,
    subject: str,
    email_index: int,
    is_cold: bool = True,
    allow_circle_back: bool = False,
    company_name: Optional[str] = None,
    sequence_type: Optional[str] = None,
) -> None:
    """
    Run validate_email and raise ValueError if any abort-level violation hit.
    Use from drafting skills as a one-liner.
    """
    violations = validate_email(
        body=body,
        subject=subject,
        email_index=email_index,
        is_cold=is_cold,
        allow_circle_back=allow_circle_back,
        company_name=company_name,
        sequence_type=sequence_type,
    )
    aborts = [v for v in violations if v["severity"] == "abort"]
    if aborts:
        msg_lines = [f"Validator aborted Email {email_index} write. {len(aborts)} violation(s):"]
        for v in aborts:
            msg_lines.append(f"  [{v['rule']}] {v['detail']}")
        raise ValueError("\n".join(msg_lines))


def audit_queue_file(queue_path: str = r"C:\\Claude-Brain\\email-queue.json", days_back: int = 7) -> List[Dict]:
    """
    Used by osi-monitor's weekly audit pass. Scans recent sent entries through
    the validator. Returns a list of {entry_id, violations} for any entry that
    fails. Empty list = clean.
    """
    import datetime
    if not os.path.exists(queue_path):
        return []
    with open(queue_path, "r", encoding="utf-8") as f:
        queue = json.load(f)

    cutoff = (datetime.date.today() - datetime.timedelta(days=days_back)).isoformat()
    findings = []
    for entry in queue:
        if entry.get("status") != "sent":
            continue
        send_date = entry.get("sendDate") or ""
        if send_date < cutoff:
            continue
        # Infer email_index from id suffix (id pattern: name-company-N).
        email_index = 1
        m = re.search(r"-(\d)$", entry.get("id", ""))
        if m:
            email_index = int(m.group(1))
        violations = validate_email(
            body=entry.get("body", ""),
            subject=entry.get("subject", ""),
            email_index=email_index,
            is_cold=True,
        )
        aborts = [v for v in violations if v["severity"] == "abort"]
        if aborts:
            findings.append({
                "id": entry.get("id"),
                "prospect": entry.get("prospectName"),
                "company": entry.get("company"),
                "sendDate": send_date,
                "violations": aborts,
            })
    return findings


if __name__ == "__main__":
    christopher_body = """Christopher,

I'm Andy McLean at OSI Global. I work with IT infrastructure managers at large financial institutions on two areas where OEM pricing tends to be painful: transceivers and third party maintenance.

We manufacture SmartOptics transceivers at 80 to 90 percent below Cisco OEM list, and we do multi vendor TPM covering Cisco, Dell, NetApp, HP, and Arista at 40 to 60 percent below OEM rates.

BNY's Pittsburgh infrastructure footprint is significant. Happy to drop a sample optics box or run a quick TPM benchmark to show you the delta.

Worth 15 minutes?"""
    christopher_subject = "Quick question on your infrastructure spend"
    violations = validate_email(christopher_body, christopher_subject, email_index=1, is_cold=True)
    print(f"Christopher email violations: {len(violations)}")
    for v in violations:
        print(f"  [{v['rule']}] {v['detail']}")
    if not violations:
        print("ERROR: Christopher email should have failed validation but passed.")
        exit(1)
    else:
        print("\nGOOD: Christopher email correctly failed validation.")
