# Prompt Rewriting Rules

When rewriting any agent JD, apply `rag-prompting` principles:

- One concrete task per instruction.
- Every hard constraint must be testable: "You MUST NOT edit files outside X" — not "try to stay in your domain."
- Replace every pronoun reference with an explicit noun phrase.
- State output format explicitly for every artifact the agent produces.
- Replace vague directives ("be helpful", "be accurate") with measurable ones ("query the notebook before answering", "cite the source").
- Ground every domain constraint in Redline's actual context (geotechnical/civil engineering B2B SaaS for engineers, not generic knowledge workers).
- Frame responsibilities as outcomes and decisions, not as a fixed task list (Jesuthasan & Boudreau anti-pattern: rigid JD that traps work in a title).
