# Standards Copyright Field Design for Library Index

**Sub-domain**: standards-and-codes
**Last verified**: 2026-05-05
**Confidence**: practitioner-grounded
**Sources**: Graeme's professional experience (25+ years, large NZ geotechnical consultancy); existing knowledge document `nz-au-standards-ip-classification.md`

---

## Summary

Practical guidance for designing a `copyright` controlled vocabulary and companion fields in the Redline library index. Covers the real-world copyright/licensing categories encountered across NZS, AS, AS/NZS, BS, EN, ISO, and professional society publications. Designed to support 257+ AS/NZS standards now and BS/EN/ISO expansion later.

---

## Key Facts

1. **All engineering standards are copyrighted.** There is no "public domain" category for current standards. Even freely accessible standards have a copyright holder.

2. **Referencing by clause number is always permitted.** No standards body has challenged clause-number citation in professional practice. This is the foundation of the citation-only architecture.

3. **Reproduction of text, tables, and figures is restricted** under all proprietary and subscription access models. This is the constraint that bites for software products generating output.

4. **Organisational subscriptions do not grant software ingestion rights.** SAI Global, BSI Knowledge, and Standards NZ Online subscriptions explicitly prohibit systematic downloading or ingestion into other systems.

5. **Crown copyright (NZS standards via MBIE) may allow more liberal use** than pure proprietary standards, but commercial reproduction still requires permission.

6. **Professional society guidance (NZGS, CIRIA, ACENZ, ICE)** sits in a grey area — often freely distributed but with unverified reproduction terms.

---

## Recommended Controlled Vocabulary — `copyright` Field

| Value | Meaning |
|---|---|
| `proprietary` | Purchased from standards body or reseller. Full copyright protection. Cite by reference only. |
| `subscription` | Accessed via organisational subscription (SAI Global, BSI Knowledge, Standards NZ Online). Same copyright as proprietary — distinction tracks access mechanism. |
| `crown` | Crown copyright (NZS via MBIE, some UK standards). May allow more liberal use but commercial reproduction still requires permission. |
| `free-access` | Made freely available by the issuing body but still copyrighted. Cite by reference. Do not assume reproduction rights. |
| `society-guidance` | Professional society publications (NZGS, CIRIA, ACENZ, ICE). Copyright held by society. Often freely distributed. Reproduction terms typically unverified. |
| `draft` | Draft for public comment. Not to be cited as current. Temporary document. |

## Recommended Companion Fields

| Field | Type | Purpose |
|---|---|---|
| `access_source` | Controlled vocabulary | Where we actually get the document: `sai-global`, `standards-nz-online`, `bsi-knowledge`, `nzgs-website`, `direct-purchase`, `other` |
| `citation_permitted` | Boolean (default TRUE) | Can we cite clause numbers in generated output? YES for all categories. Exists to make the default explicit. |
| `reproduction_permitted` | Enum: `none`, `limited`, `unverified`, `permitted` | Can we reproduce actual text? `none` for proprietary/subscription. `limited` for Crown copyright (with attribution). `unverified` for society guidance. `permitted` only with explicit written permission. |
| `licence_verified` | Boolean | Have we contacted the copyright holder and confirmed programmatic use terms? Almost everything starts as FALSE. |
| `licence_notes` | Free text | Specific terms, contact details, or outcomes from licence enquiries. |

## Design Decisions

- **No separate value for international adoptions.** An AS/NZS ISO standard is `proprietary` or `subscription`. Track adoption relationship in a separate `adopted_from` field if needed.
- **No `quote_limit` field.** No standards body publishes a word count threshold for fair dealing. False precision.
- **`subscription` is distinct from `proprietary`** because it tracks how we have access, which matters for licence verification and renewal tracking.

---

## Practical Constraints for Redline

- **Safe:** "See NZS 4431:2022, Clause 6.3 for pile design requirements" — clause reference, no copyright issue.
- **Unsafe without licence:** Reproducing Table 6.1 from NZS 4431 in generated output.
- **Grey area:** Paraphrasing procedural steps from a standard — legally a derivative work, practically unchallenged in geotechnical engineering.
- **High-risk:** Systematic ingestion of standards content for applicability mappings — no known NZ/AU precedent for a software vendor licence. Direct enquiry with Standards NZ and Standards Australia required.

---

## Open Questions

1. Does the `copyright` field need to distinguish between AS-only, NZS-only, and AS/NZS joint publications? Current recommendation: no — copyright terms are functionally identical. Track the standards body in a separate `publisher` field.
2. Should `draft` standards be indexed at all? They are temporary. Recommendation: index only if the consultancy is actively participating in the review process.

---

## Further Reading

- Existing knowledge: [nz-au-standards-ip-classification.md](nz-au-standards-ip-classification.md)
- Standards New Zealand licensing: `standards.govt.nz/support/licensing/`
- NZ Copyright Act 1994, Section 43 — fair dealing provisions
