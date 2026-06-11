# HubSpot Property Reference

OSI-specific HubSpot property names and owner IDs. HubSpot has renamed some standard fields and added custom ones — using the wrong name returns empty results with no error.

## Owner IDs

- **Brian Charrette**: `213536174`
- **Adam Cooney**: confirm via `search_owners` if needed — Brian's partner, joint accounts flagged "Bri & Adam Biz"

When creating contacts or tasks for Brian, set `hubspot_owner_id` to `213536174`.

## Company object — key properties

Standard fields:
- `name` — company name
- `domain` — primary web domain (no www, no protocol)
- `industry`
- `numberofemployees` — integer
- `annualrevenue` — integer, in USD
- `lifecyclestage` — lead, marketingqualifiedlead, salesqualifiedlead, opportunity, customer, evangelist, other
- `hubspot_owner_id` — OSI rep assigned
- `createdate`
- `hs_lastmodifieddate`
- `notes_last_contacted`
- `notes_last_activity_date`
- `city`, `state`, `country`
- `phone`

Custom OSI fields (if present on the record):
- `last_enrichment_date` — optional; set by this skill when enrichment runs. If the property doesn't exist on the portal, log a note on the company instead rather than attempting to create the property.

## Contact object — key properties

Standard fields:
- `firstname`, `lastname`
- `email` — primary work email (must be verified to create a new contact)
- `jobtitle`
- `phone`, `mobilephone`
- `lifecyclestage`
- `hubspot_owner_id`
- `hs_lead_status`
- `notes_last_contacted`
- `notes_last_activity_date`
- `linkedinbio` — if populated, shows LI URL

For new contacts created by this skill, always set:
- `hubspot_owner_id: 213536174`
- `lifecyclestage: lead`
- associate with the company record (via the associations API, not a property)

## Deal object — key properties

- `dealname`
- `amount` — total deal value
- `iqmargin` — **OSI's GP (gross profit) field** — this is the critical number for rep P&L, not `amount`
- `dealstage`
- `pipeline`
- `closedate`
- `hubspot_owner_id`
- `client_id__cv_name_` — **OSI's company-on-deal field** — use this instead of the default company association when both exist, since some legacy deals only have this populated
- `dealtype`
- `hs_deal_stage_probability`

When building the deal history table in the report, pull `dealname`, `amount`, `iqmargin`, `dealstage`, `closedate`. Sort by `closedate` descending. Sum `iqmargin` for total GP.

## Task object — key properties

For the outreach tasks this skill creates:
- `hs_task_subject` — format: `"bc-account-enrichment: reach out to [Name] at [Company] — [angle]"`
- `hs_task_body` — longer note with the scoring rationale and suggested talking points
- `hs_task_priority` — `HIGH`, `MEDIUM`, `LOW`
- `hs_task_status` — `NOT_STARTED` for new tasks
- `hs_task_type` — `EMAIL`, `CALL`, `TODO` — use `TODO` unless Brian specifies
- `hs_timestamp` — due date (ms epoch or ISO8601)
- `hubspot_owner_id: 213536174`
- Associate with the contact and company records

Default due date: 3 business days from creation.

## Associations

HubSpot tracks relationships through the associations API, not properties. When creating a new contact:
1. Create the contact record
2. Create an association between contact and company (`contact_to_company`)

When creating a task:
1. Create the task
2. Associate with contact (`task_to_contact`)
3. Associate with company (`task_to_company`)

## Account tagging — "Bri & Adam Biz"

If the company's `hubspot_owner_id` matches Brian's (213536174) AND Adam Cooney is listed on any associated deal or contact, flag the account in the report as "Bri & Adam Biz." This affects commission splits and strategic calls — Brian wants to see it surfaced.

## Search patterns

Use `search_crm_objects` with these filter shapes:

Company by name (partial match):
```json
{
  "objectType": "companies",
  "filterGroups": [{"filters": [{"propertyName": "name", "operator": "CONTAINS_TOKEN", "value": "Smithsonian"}]}]
}
```

Contacts at a company (by company ID):
```json
{
  "objectType": "contacts",
  "filterGroups": [{"filters": [{"propertyName": "associatedcompanyid", "operator": "EQ", "value": "12345"}]}]
}
```

Deals owned by Brian, last 12 months:
```json
{
  "objectType": "deals",
  "filterGroups": [{"filters": [
    {"propertyName": "hubspot_owner_id", "operator": "EQ", "value": "213536174"},
    {"propertyName": "closedate", "operator": "GTE", "value": "2025-04-21"}
  ]}]
}
```

## Things to NEVER do

- Don't overwrite existing contact owners when enriching — if a contact already has an owner, leave it. Only set owner on new contacts.
- Don't create duplicate companies. Search first by name AND domain before adding.
- Don't create contacts without a verified work email. ZI contact emails are generally reliable; LinkedIn-only leads without email stay in the report but do not get added to HS.
- Don't modify deal records from this skill. Enrichment is read-only on deals.
