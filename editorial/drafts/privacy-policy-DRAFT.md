# DRAFT — NEEDS REVIEW — Privacy Policy for westfwliving.com

**Status: NOT PUBLISHED. Do not deploy without human review.**

Privacy/consent disclosures are a safeguarded category under `editorial/DAILY_RUN.md`, so
this was drafted and flagged rather than published. It is a skeleton grounded in what the
site *actually does* — every field below was read out of the repository, not assumed — with
each policy judgement left explicitly open for a human.

## Why this is urgent (the finding that produced it)

Every hardened lead form on the site carries a **required** consent checkbox reading:

> I agree to be contacted about my inquiry by email or phone and accept the
> [privacy policy](/privacy/). No spam — unsubscribe anytime.

`/privacy/` **does not exist** — it 404s. The Spanish equivalent `/es/privacidad/` also 404s.
Confirmed 2026-08-16 by `scripts/apply_standing_fixes.py`:

- `/privacy/` — linked from **197** pages
- `/es/privacidad/` — linked from **42** pages

So the site currently requires users to accept a document it does not serve. That is a
consent-integrity problem, not just a broken link, which is why it is backlog item #1.

## What the site actually collects (verified from the code)

Read from `gen/common.py` (`lead_form()`) and the hardened forms across the tree.

**Submitted by the user:**
| Field | Notes |
| --- | --- |
| `name` | required |
| `email` | required |
| `phone` | required |
| `lease_end` / `move_date` / `sell_timeline` | one per page, by context; optional |
| `property_address` | selling pages only; optional |
| `consent` | required checkbox |

**Captured automatically** (`aw-utm-capture` inline script, stored in `sessionStorage` under
`aw_ft`, written into hidden fields on submit):
`utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content`, `referrer`,
`landing_page`, `page_url`, `consent_ts` (ISO timestamp stamped at submit).

**Anti-spam:** `_honey` honeypot field (off-screen; a human never sees or fills it).

**Processor:** form posts go to FormSubmit (`https://formsubmit.co/<hashed-endpoint>`), which
relays to the operator's destination address. The hash is a privacy proxy for that address —
the cleartext address is deliberately absent from the markup, and the gate asserts it stays
absent. **FormSubmit is a third-party processor and its own privacy terms apply.**

**Third parties referenced in `netlify.toml`'s CSP:** Google Tag Manager / `googletagmanager.com`
and `google-analytics.com` are permitted in `script-src` / `connect-src`, and Google Fonts in
`style-src` / `font-src`. **Open question for review:** GA4 appears to be permitted but not
yet wired — confirm whether analytics is actually running before the policy describes it.

**Hosting:** Netlify (server logs, including IP addresses, are processed by the host).

## Sections to fill in — each needs a human decision

1. **Who the controller is** — the legal entity and a contact address.
2. **Retention** — how long lead submissions are kept. *Not inferable from the code.*
3. **Sharing / onward transfer** — the site is publisher-mode and states it is not a
   brokerage and makes no lender placements. Confirm leads are not sold or shared with
   third-party service providers, and say so plainly if true.
4. **Unsubscribe mechanism** — the consent copy promises "unsubscribe anytime." Name the
   actual mechanism (reply-to-unsubscribe, a link, an address).
5. **Texas / US privacy rights** — whether the Texas Data Privacy and Security Act applies to
   this operator (it has small-business thresholds), and the request channel if so.
6. **Analytics + cookies** — resolve the GA4 question above. `sessionStorage` is used for
   attribution and should be disclosed regardless.
7. **Children** — standard not-directed-to-children statement.
8. **Effective date + change process.**
9. **Spanish mirror** — `/es/privacidad/` must be a true translation, published at the same
   time, with bidirectional hreflang.

## Suggested implementation once approved

Author as `gen/pages_privacy.py` using `page()` so both language versions get the standard
chrome, canonical and hreflang, then add `/privacy/` and `/es/privacidad/` to `RECIPROCAL`
if a visible footer link is wanted, and **remove both entries from `KNOWN_MISSING`** in
`scripts/apply_standing_fixes.py` so `link-assert` enforces them from then on.

---
Drafted 2026-08-16 by the daily publishing cycle. Flagged `NEEDS REVIEW`; nothing deployed.
