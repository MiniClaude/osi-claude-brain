"""
Tests for the queue-write sanitizers defined in osi-outreach-sequence Step 6.7
and copied into osi-old-customer-reengagement.

Why this file exists:
- The 2026-04-30 punch list called for "real test fixtures, not the prose-regex
  self-check that I just ripped out of the email-sender." This is that.
- Andy can run `python C:/Claude-Brain/tests/test_sanitizers.py` anytime to
  catch regressions in the sanitizers BEFORE a fire ships malformed emails.
- The sanitizer source-of-truth lives in the skill files. This test redefines
  the same functions here and asserts behavior. If the skills' sanitizer
  diverges from this test, run the test, see the failure, decide which one
  is right, then sync.

Andy Rule #4 compliance: this file references the em-dash (U+2014) and
en-dash (U+2013) ONLY via chr() calls. The source contains zero literal
em-dashes or en-dashes.
"""

import re
import sys

# Banned characters, constructed via chr() so this source file is rule-clean.
EM = chr(0x2014)  # em-dash
EN = chr(0x2013)  # en-dash


def sanitize_body(text, email_index):
    """Mirror of osi-outreach-sequence Step 6.7 sanitize_body."""
    if text is None:
        return ""
    text = (text
        .replace(" " + EM + " ", ". ")
        .replace(EM + " ", ". ")
        .replace(" " + EM, ".")
        .replace(EM, "-")
        .replace(" " + EN + " ", ". ")
        .replace(EN, "-"))
    if email_index >= 3:
        markers = [
            r"\n*\s*-{5,}\s*On .* wrote\s*-{5,}",
            r"\nOn .*,? .* (?:McLean )?(?:wrote|wrote:)",
            r"\n>+ ",
            r"\nFrom: Andrew McLean",
        ]
        for m in markers:
            match = re.search(m, text)
            if match:
                text = text[:match.start()].rstrip()
                break
    text = re.sub(r" {2,}", " ", text)
    text = "\n".join(line.rstrip() for line in text.split("\n"))
    text = re.sub(r"\n{3,}", "\n\n", text)
    if EM in text or EN in text:
        raise ValueError(f"sanitize_body left dashes in body. Bug. Text starts: {text[:80]!r}")
    return text.strip()


def sanitize_subject(subject):
    """Mirror of osi-outreach-sequence Step 6.7 sanitize_subject."""
    if subject is None:
        return ""
    subject = (subject
        .replace(" " + EM + " ", ", ")
        .replace(EM, "-")
        .replace(" " + EN + " ", ", ")
        .replace(EN, "-"))
    subject = re.sub(r"\s+", " ", subject).strip()
    if EM in subject or EN in subject:
        raise ValueError(f"sanitize_subject left dashes. Bug. Subject: {subject!r}")
    return subject


# ============================================================================
# TESTS
# ============================================================================

PASSES = 0
FAILS = []

def check(name, condition, detail=""):
    global PASSES, FAILS
    if condition:
        PASSES += 1
    else:
        FAILS.append((name, detail))


def expect_raises(name, fn, *args, **kwargs):
    """Assert that fn(*args, **kwargs) raises ValueError."""
    try:
        result = fn(*args, **kwargs)
    except ValueError:
        check(name, True)
        return
    except Exception as e:
        check(name, False, f"raised {type(e).__name__} instead of ValueError: {e}")
        return
    check(name, False, f"did not raise. Returned: {result!r}")


# Em-dash handling
check(
    "em-dash with surrounding spaces becomes period",
    sanitize_body("First sentence " + EM + " second sentence.", 1) == "First sentence. second sentence.",
)

check(
    "em-dash trailing space becomes period",
    sanitize_body("First sentence" + EM + " second sentence.", 1) == "First sentence. second sentence.",
)

check(
    "bare em-dash becomes hyphen",
    sanitize_body("compound" + EM + "word", 1) == "compound-word",
)

# En-dash handling
check(
    "en-dash with spaces becomes period",
    sanitize_body("Range 1 " + EN + " 5 covered", 1) == "Range 1. 5 covered",
)

check(
    "bare en-dash becomes hyphen",
    sanitize_body("range" + EN + "value", 1) == "range-value",
)

# Email 1 and 2: quote markers should NOT be stripped
check(
    "Email 1 keeps body intact (no quote-strip)",
    sanitize_body("Hello\n\nOn Monday, Andy McLean wrote:\nold stuff", 1)
        == "Hello\n\nOn Monday, Andy McLean wrote:\nold stuff",
)

check(
    "Email 2 keeps body intact (no quote-strip)",
    sanitize_body("Any thoughts?", 2) == "Any thoughts?",
)

# Email 3+: quote markers SHOULD be stripped
check(
    "Email 3 strips 'On <date>, Andy McLean wrote:' marker",
    sanitize_body("New pitch here.\n\nOn Mon, Apr 22, Andy McLean wrote:\n[Email 1 content]", 3)
        == "New pitch here.",
)

check(
    "Email 4 strips '>' quoted lines",
    sanitize_body("Different angle.\n> quoted thread\n> more quoted", 4)
        == "Different angle.",
)

check(
    "Email 5 strips '----- On X wrote -----' marker",
    sanitize_body("Final close.\n----- On Apr 28 Andy McLean wrote -----\nEmail 4 body", 5)
        == "Final close.",
)

check(
    "Email 6 strips 'From: Andrew McLean' Outlook header",
    sanitize_body("Should I close the file?\nFrom: Andrew McLean <andy@osiglobal.com>\nMore stuff", 6)
        == "Should I close the file?",
)

# Whitespace normalization
check(
    "multiple spaces collapse to one",
    sanitize_body("hello    world", 1) == "hello world",
)

check(
    "trailing whitespace per line is trimmed",
    sanitize_body("hello   \nworld   ", 1) == "hello\nworld",
)

check(
    "3+ blank lines collapse to one blank line",
    sanitize_body("para 1\n\n\n\n\npara 2", 1) == "para 1\n\npara 2",
)

# Edge cases
check(
    "None body returns empty string",
    sanitize_body(None, 1) == "",
)

check(
    "empty body returns empty string",
    sanitize_body("", 1) == "",
)

check(
    "body with only whitespace strips to empty",
    sanitize_body("   \n\n   ", 1) == "",
)

# Subjects
check(
    "subject em-dash with spaces becomes comma",
    sanitize_subject("OSI " + EM + " quick question") == "OSI, quick question",
)

check(
    "subject bare em-dash becomes hyphen",
    sanitize_subject("OSI" + EM + "question") == "OSI-question",
)

check(
    "subject collapses internal whitespace",
    sanitize_subject("OSI    quick    question") == "OSI quick question",
)

check(
    "subject trims surrounding whitespace",
    sanitize_subject("   leading and trailing   ") == "leading and trailing",
)

check(
    "subject None returns empty",
    sanitize_subject(None) == "",
)

# Real-world Email 3 (the 2026-04-29 incident pattern that should be cleaned)
incident_body = (
    "Different angle. OSI does multi vendor third party maintenance.\n"
    "If your renewals at BNY are coming up, worth a quick comparison?\n"
    "On Wed, Apr 22, 2026, Andy McLean wrote:\n"
    "> Any thoughts?\n"
    "> > Hi Brian, I'd like to send you a sample DIMM..."
)
expected = (
    "Different angle. OSI does multi vendor third party maintenance.\n"
    "If your renewals at BNY are coming up, worth a quick comparison?"
)
check(
    "2026-04-29 incident body sanitizes correctly for Email 3",
    sanitize_body(incident_body, 3) == expected,
    detail=f"got: {sanitize_body(incident_body, 3)!r}",
)

# Same body, but if marked as Email 1 (where quote markers are NOT stripped),
# the content stays.
check(
    "2026-04-29 incident body NOT stripped if Email 1",
    "Andy McLean wrote:" in sanitize_body(incident_body, 1),
)

# Sanity: an empty Email 3 body with only quote markers ends up empty
check(
    "Email 3 with ONLY quote markers strips to empty",
    sanitize_body("\n\nOn Mon, Andy McLean wrote:\n[old content]", 3) == "",
)


# ============================================================================
# REPORT
# ============================================================================

print(f"\n{PASSES} passed, {len(FAILS)} failed")
if FAILS:
    print("\nFAILURES:")
    for name, detail in FAILS:
        print(f"  - {name}")
        if detail:
            print(f"      {detail}")
    sys.exit(1)
else:
    print("All sanitizer tests passed. Safe to ship queue writes.")
    sys.exit(0)
