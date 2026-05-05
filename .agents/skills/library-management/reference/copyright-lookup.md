# Copyright Lookup Table

Use this table to determine the `copyright` and `reproduction_permitted` values when indexing a standard.

## `copyright` values

| Value | Definition | When to use | Typical `reproduction_permitted` |
|---|---|---|---|
| `proprietary` | Purchased single-user or per-copy licence from a standards body or retailer | Most AS/NZS, BS EN, ISO standards bought from SAI Global, BSI Shop, or equivalent | `clause-reference` |
| `subscription` | Accessed via an organisational subscription (e.g. Standards Online, BSI BSOL, Techstreet) | Consultancy-wide access through annual licence | `partial-quote` (check subscription terms) |
| `crown` | Crown copyright -- government-authored, typically more permissive reproduction rules | Some NZ and UK standards, building codes, government-published codes of practice | `partial-quote` |
| `free-access` | Freely available (older withdrawn editions made public, or released for public interest) | Withdrawn editions published openly, post-disaster releases, freely downloadable from standards body | `partial-quote` |
| `society-guidance` | Published by a professional or industry body with its own terms (not a formal national standard) | CIRIA reports, NZGS guidelines, ICE guidance notes, ASCE manuals | `clause-reference` (varies -- check publisher) |
| `draft` | Circulated for public comment -- reproduction restricted to commenting purpose | DR-prefixed documents, DPC (Draft for Public Comment), committee drafts | `none` |

## `reproduction_permitted` values

| Value | Definition | Product implication |
|---|---|---|
| `none` | No text reproduction allowed under any circumstances | Can reference by standard number and title only. Cannot extract or quote clause text |
| `clause-reference` | May cite clause numbers and titles, but not reproduce clause text | Can build clause reference tables, cross-reference matrices. Cannot include clause wording in generated reports |
| `partial-quote` | May quote limited extracts (typically up to 10% or a single table/figure) with attribution | Can include brief extracts in reports with proper attribution. Check specific licence for limits |
| `full-with-licence` | Full reproduction permitted under a specific licence agreement | Can include full clause text in generated documents. Licence details must be recorded in `licence_notes` |

## Decision flow

1. **Is it a draft (DR, DPC)?** -> `copyright = draft`, `reproduction_permitted = none`
2. **Is it from CIRIA, NZGS, ICE, or similar professional body?** -> `copyright = society-guidance`, check publisher terms
3. **Is it Crown copyright (check title page)?** -> `copyright = crown`, `reproduction_permitted = partial-quote`
4. **Is it freely downloadable from the standards body website?** -> `copyright = free-access`
5. **Was it accessed via organisational subscription?** -> `copyright = subscription`, check subscription terms
6. **Was it purchased per-copy?** -> `copyright = proprietary`, `reproduction_permitted = clause-reference`
7. **When in doubt:** `copyright = proprietary`, `reproduction_permitted = clause-reference`, `licence_verified = FALSE`
