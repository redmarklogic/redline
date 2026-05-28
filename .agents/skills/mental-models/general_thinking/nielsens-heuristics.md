# Nielsen's 10 Usability Heuristics

## What it is

Ten broad principles for evaluating interaction design, originally developed by Jakob Nielsen and Rolf Molich in 1990 and refined by Nielsen in 1994. They are called heuristics because they are rules of thumb rather than specific checklists, and they have remained applicable across 30+ years of interface evolution.

## Core principle

Most usability problems are predictable. The majority of interface failures can be diagnosed using ten orthogonal lenses covering system feedback, user control, consistency, error handling, and cognitive load.

## When to invoke

- Conducting a heuristic evaluation without access to user research or usability testing
- Reviewing a design for obvious issues before committing to development
- Prioritising UI fixes: scan all ten heuristics, rate severity, triage by impact
- Communicating a UX problem to stakeholders by citing an established authority

## How to apply

Evaluate the interface against each heuristic in sequence, logging violations with a severity rating (0 = no problem, 4 = usability catastrophe):

1. **Visibility of system status** -- keep users informed about what is happening through timely, appropriate feedback
2. **Match between system and real world** -- use the user's language, not internal jargon; follow real-world conventions and natural mapping
3. **User control and freedom** -- provide clearly marked exits; support undo and redo for accidental actions
4. **Consistency and standards** -- follow platform and industry conventions; do not make users guess whether different words or actions mean the same thing
5. **Error prevention** -- design to prevent problems before they occur; prefer constraints and confirmation over error messages
6. **Recognition rather than recall** -- make options, actions, and information visible; minimise memory burden between steps
7. **Flexibility and efficiency of use** -- provide accelerators for expert users without burdening novices; allow customisation of frequent actions
8. **Aesthetic and minimalist design** -- remove irrelevant information; every extra element competes with the relevant ones and reduces their visibility
9. **Help users recognize, diagnose, and recover from errors** -- plain-language error messages that precisely identify the problem and constructively suggest a fix
10. **Help and documentation** -- if help is required, make it searchable, contextual, and action-oriented with concrete steps

## Anti-patterns

- **Heuristic as binary checklist** -- mechanically marking each heuristic pass/fail without severity ratings produces an unusable list of equal-weight issues
- **Designer self-evaluation** -- evaluating your own design; familiarity blinds you to violations that a fresh evaluator would catch immediately; use at least two independent reviewers
- **Skipping triage** -- reporting every violation without prioritising by frequency and severity buries the critical issues in noise

## Source

*10 Usability Heuristics for User Interface Design* -- Jakob Nielsen (Nielsen Norman Group, 1994; updated 2024). nngroup.com/articles/ten-usability-heuristics/
