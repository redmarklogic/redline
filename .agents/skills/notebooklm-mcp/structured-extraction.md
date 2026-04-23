# NotebookLM Structured Extraction Guide

Reference for extracting data from NotebookLM into CSV, JSON, or any structured
format. Apply **after** [`prompting-guide.md`](prompting-guide.md) — Rules 1–5
still apply to every structured query.

---

## Rule 6 — Schema Contract

When extracting data, the generation step has no schema constraint. Without an
explicit contract the model improvises column names, invents enum synonyms
("Critical" instead of "High"), wraps output in markdown fences, and injects
conversational filler — all of which break downstream parsing.

NotebookLM has no API-level schema enforcement (unlike OpenAI structured outputs).
Emulate Pydantic AI: define a strict **Schema Contract** directly in the prompt.

### Five required parts

1. **Explicit Types** — label each field: `[String]`, `[Integer]`, `[Float]`, `[Enum]`.
2. **Enum Constraints** — list exact allowed values (e.g. `"High", "Medium", "Low"`).
3. **Missing-Value Sentinel** — `"N/A"` for strings, `null` for numbers. For
   booleans use a three-value enum (`"TRUE"`, `"FALSE"`, `"UNKNOWN"`) so "not
   stated" is distinguishable from a confirmed negative.
4. **Delimiter & Row Separator** (CSV) — state comma delimiter and one row per line.
5. **One-Shot Example** — a single example row/object that anchors exact format.

### Required OUTPUT FORMAT instructions

| Format | Add verbatim to OUTPUT FORMAT block |
|--------|-------------------------------------|
| CSV    | `Provide raw CSV only. No markdown code fences, no commentary. Do not embed citation numbers or markers inside field values. Use comma (,) delimiter. One row per line.` |
| JSON   | `Raw JSON array only. No markdown code fences, no explanations. Do not embed citation numbers or markers inside field values. Start your response with [ and end with ]. Nothing else.` |

### Cold-start failure for nested schemas

On the **first message** in a session, complex nested schemas often fail — the
model defaults to narrative mode. For any nested extraction (parent with child
arrays), always warm up first:

1. **Step 1** — flat query in a new session (extracts top-level objects).
2. **Step 2** — nested follow-up in the **same `session_id`**.

---

## Which template to use

| Need | Format | Template |
|------|--------|----------|
| Rows of data → spreadsheet / Excel | CSV | Flat CSV |
| Objects with simple fields → JSON | JSON | Flat JSON |
| Objects with child arrays → JSON | JSON | Nested (two-step) |

---

## Template: Flat CSV

```
# Bad:  "Extract the design requirements from Section 4 and put them in a table."
# Messy result: inconsistent delimiters, invented risk labels, markdown fences.

# Good:
Explain for the uninitiated. Define any specialist term the first time it appears.
Keep citations. Avoid ambiguity.

Extract all design requirements from Section 4 of the guidelines.

OUTPUT FORMAT:
Provide raw CSV only. No markdown code fences, no commentary.
Do not embed citation numbers or markers inside field values.
Use comma (,) as the column delimiter. Place each row on its own line.

SCHEMA (each row = one requirement):
- "Clause":      [String]  Exact clause reference, e.g. "4.1.2".
- "Requirement": [String]  One-sentence summary. Maximum 15 words.
- "Risk_Level":  [Enum]    Exactly one of: "High", "Medium", "Low".
- "Actionable":  [Enum]    Exactly one of: "TRUE", "FALSE", "UNKNOWN".

MISSING VALUES: Use "N/A" for strings. Use "UNKNOWN" when not stated in sources.

EXAMPLE (first two rows):
Clause,Requirement,Risk_Level,Actionable
4.1.2,Foundation must resist lateral loads,High,TRUE

Answer only using information found in the notebook sources. If not covered, say so.
```

---

## Template: Flat JSON

```
# Bad:  "List all soil layers in Borehole BH-01 with depths and classification. Return as JSON."
# Messy result: depths in free text, no consistent keys, flat strings instead of typed fields.

# Good:
Explain for the uninitiated. Define any specialist term the first time it appears.
Keep citations. Avoid ambiguity.

Extract all soil layers logged in Borehole BH-01.

OUTPUT FORMAT:
Raw JSON array only. No markdown code fences, no explanations.
Do not embed citation numbers or markers inside field values.
Start your response with [ and end with ]. Nothing else.

SCHEMA (each object = one layer):
- "top_m":       [Float]  Top depth in metres.
- "base_m":      [Float]  Base depth in metres.
- "description": [String] Soil description as logged. Maximum 20 words.
- "uscs_class":  [String] USCS classification symbol, e.g. "SM", "CL".
- "origin":      [Enum]   Exactly one of: "Fill", "Natural", "Unknown".

MISSING VALUES: Use null for numbers, "N/A" for strings, "Unknown" for origin.

EXAMPLE:
[{"top_m": 0.0, "base_m": 1.5, "description": "Compacted hardfill", "uscs_class": "GP", "origin": "Fill"}]

Answer only using information found in the notebook sources. If not covered, say so.
```

---

## Template: Nested JSON (two-step)

```
# Step 1 — Flat warm-up (first message, creates session)
Explain for the uninitiated. Define any specialist term the first time it appears.
Keep citations. Avoid ambiguity.

List all contract frameworks mentioned in the sources that describe subsurface
construction risk allocation. For each framework, state who bears the default
risk and the primary allocation mechanism.

OUTPUT FORMAT:
Raw JSON array only. No markdown code fences, no explanations.
Do not embed citation numbers or markers inside field values.
Start your response with [ and end with ]. Nothing else.

SCHEMA (each object = one framework):
- "framework":            [String] Name. Maximum 6 words.
- "allocated_to_default": [Enum]   Exactly one of: "Owner", "Contractor", "Shared", "Unspecified".
- "mechanism":            [String] How allocation works. Maximum 15 words.

EXAMPLE:
[{"framework":"FIDIC Emerald Book","allocated_to_default":"Shared","mechanism":"GBR baseline exceedance triggers owner liability"}]

Answer only using information found in the notebook sources. If not covered, say so.
```

```
# Step 2 — Nested follow-up (same session_id)
Now expand each framework with its specific risk categories.

OUTPUT FORMAT:
Raw JSON array only. No markdown code fences, no explanations.
Do not embed citation numbers or markers inside field values.
Start your response with [ and end with ]. Nothing else.

SCHEMA (top-level = one framework):
- "framework":        [String] Name. Maximum 6 words.
- "risk_allocations": [Array]  Array of objects.

SCHEMA (each object inside "risk_allocations"):
- "risk_category": [String] Type of risk. Maximum 8 words.
- "allocated_to":  [Enum]   Exactly one of: "Owner", "Contractor", "Shared", "Unspecified".
- "mechanism":     [String] How allocation works. Maximum 15 words.

MISSING VALUES: "N/A" for strings, "Unspecified" for enums.

EXAMPLE:
[{"framework":"FIDIC Emerald Book","risk_allocations":[{"risk_category":"Unforeseen ground conditions","allocated_to":"Shared","mechanism":"GBR baseline exceedance triggers owner liability"}]}]

Answer only using information found in the notebook sources. If not covered, say so.
```

---

## Common Mistakes (structured output)

| Mistake | Why it fails | Fix |
|---------|-------------|-----|
| No schema contract | Improvised columns, invented synonyms | Rule 6: types, enums, sentinels, example |
| No delimiter instruction (CSV) | Rows collapsed to one line or space-separated | Add `"comma delimiter, one row per line"` |
| No boundary anchoring (JSON) | JSON wrapped in conversational prose | Add `"Start with [ end with ]. Nothing else."` |
| Citation markers in values | `\n1\n` breaks JSON/CSV parsing | Add `"Do not embed citation numbers inside field values"`; strip with regex `\n\d+\n` if needed |
| Nested schema on cold start | Model defaults to narrative prose | Flat warm-up first, nested follow-up in same session |
| Boolean fields | Model uses "Yes"/"No"/"Maybe" | Replace with three-value enum: `"TRUE"`, `"FALSE"`, `"UNKNOWN"` |
