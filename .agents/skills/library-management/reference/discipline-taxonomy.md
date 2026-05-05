# Discipline Taxonomy

Controlled vocabulary for the `discipline` column on the Standards worksheet. Choose based on the document's primary subject matter, not by inferring from downstream use.

| Value | Use when the standard covers | Do NOT use for |
|---|---|---|
| `geotechnical` | Ground investigation, foundation design, earthworks, retaining structures, slope stability, ground improvement | Structural design of foundations (use `structural`) |
| `structural` | Design of structural elements: beams, columns, slabs, connections, frames, bridges | Material specifications (use `materials`); test methods (use `materials testing`) |
| `materials` | Material product specifications: chemical composition, mechanical properties, grades, dimensional tolerances (e.g. steel reinforcing, concrete grades, timber species) | Test methods for materials (use `materials testing`); design using those materials (use `structural`) |
| `materials testing` | Test methods and procedures for materials: tensile testing, compressive testing, chemical analysis, particle size distribution | Product specifications (use `materials`) |
| `loading` | Actions on structures: dead loads, live loads, wind loads, snow loads, load combinations, general design actions | Seismic actions (use `seismic`) |
| `seismic` | Earthquake design, seismic actions, seismic hazard assessment, liquefaction | General loading (use `loading`) |
| `environmental` | Environmental management systems, contamination assessment, noise, air quality, waste management | Workplace safety (use `occupational health and safety`) |
| `plumbing` | Water services, drainage, sanitary plumbing, gas fitting, on-site wastewater | Water/hydraulic engineering at infrastructure scale (use `general`) |
| `electrical` | Electrical installations, wiring rules, hazardous area classification, electrical equipment | Fire alarm systems (use `fire`) |
| `fire` | Fire resistance, fire safety systems, fire testing, fire detection and alarm systems, sprinklers | Workplace fire evacuation procedures (use `occupational health and safety`) |
| `occupational health and safety` | Workplace safety, confined spaces, PPE, hazardous substances, fall protection, scaffolding | Environmental management (use `environmental`) |
| `quality` | Quality management systems (ISO 9001 family), auditing (ISO 19011), risk management (ISO 31000), information governance | Discipline-specific quality controls (use the relevant discipline) |
| `general` | Does not fit any category above; multi-discipline standards; general engineering practice | Avoid unless no other category applies |
