# AI Verification Shift Evidence

**Sub-domain**: report-writing
**Last verified**: 2026-05-27
**Confidence**: cross-referenced
**Sources**: Ground Engineering Magazine (March 2026, late 2025 issues), Geotechnical Report Workflows notebook (internal consultancy QA documentation), Redline strategic-bets.md Bet 2

## Summary

Industry evidence from Ground Engineering magazine (2025-2026) and internal consultancy QA documentation showing that major geotechnical firms are actively deploying AI tools in report workflows, that the engineer's role is shifting toward "intelligent editor," and that AI-specific error classes in geotechnical reports are an emerging concern requiring new review capabilities.

## Key Facts

### AI Tools in Active Use by Major Firms

1. **Mott MacDonald's "EMMA"** (Every Mott MacDonald Answer): Internal generative AI assistant that searches company data to pull relevant information instantly, cutting time spent locating documents, extracting parameters, and performing repetitive actions. [Source: Ground Engineering Magazine, 2025-2026]

2. **Arup's "ProjectGPT"**: AI-powered NLP module within the "Fuse" platform. Users query unstructured project documents, design standards, and historical studies. Returns precise answers with source citations. Used on Bakerloo Line Extension to locate TfL standards and previous design studies, reducing design rework risk. [Source: Ground Engineering Magazine, 2025-2026]

3. **A-squared Studio**: Geotechnical engineers routinely use LLMs (ChatGPT, Claude, Microsoft Copilot) to support deliverable preparation, retrieve information, and assist with coding tasks. [Source: Ground Engineering Magazine, 2025-2026]

### The "Intelligent Editor" Role Shift

4. GE (March 2026) explicitly names this shift: AI's impact "is less about replacing geotechnical engineers and more about reshaping what it means to be one." [Source: Ground Engineering Magazine, March 2026]

5. Routine and mundane administrative tasks are being stripped away, creating hybrid roles that blend engineering judgment with data science. [Source: Ground Engineering Magazine, March 2026]

6. Engineers are moving into roles akin to an "intelligent editor" where AI acts as an augmentation tool. [Source: Ground Engineering Magazine, March 2026]

7. Professional judgment, responsibility, and liability remain firmly with the engineer. [Source: Ground Engineering Magazine, March 2026]

8. Growing expectation across regulated professions to declare when AI has been used in formal technical or advisory work. [Source: Ground Engineering Magazine, March 2026]

### Junior Engineer Training Concerns (Expertise Paradox)

9. Jim De Waele (BGA executive committee member): "Using AI rather than a junior engineer to produce a sketch, calculations or even an outline report may be expedient, but who will be training the experienced engineers of the future?" [Source: Ground Engineering Magazine, March 2026]

10. Domenico Lombardi (A-squared): "Experienced engineers develop their knowledge over several years by undertaking routine tasks, many times in different situations and in varying ground conditions. There is a risk that over time, effective AI governance may not be possible without wise geotechnical engineers." [Source: Ground Engineering Magazine, March 2026]

11. Primary concern: junior engineers traditionally develop knowledge by undertaking routine tasks (sketches, calculations, outline reports) across varying ground conditions. AI automating these foundational tasks creates an ethical and structural dilemma. [Source: Ground Engineering Magazine, March 2026]

### Existing Review Bottleneck (Pre-AI)

12. Report production already has multiple mandatory review gates: Component Review (calculations), Formatting Check (BIS/PC), Technical Review (TR), Oversight Review (PD). [Source: Geotechnical Report Workflows notebook]

13. A report cannot be issued without physical or electronic signature of PD and TR, alongside PM agreement. [Source: Geotechnical Report Workflows notebook]

14. The existing bottleneck: reviewers are meant to be "safety nets," but when authors don't contribute a solid foundation, "the reviewer is forced to pick up the pieces, and the whole process will be dragged out." [Source: Geotechnical Report Workflows notebook]

15. Recurring mechanical defects waste reviewer time: mixed tenses, overly long sentences, inconsistent formatting. [Source: Geotechnical Report Workflows notebook]

### AI Pre-Review Tools Already Being Built

16. **"Faultless" app + "T+T Writing Coach Model"**: An NZ consultancy is developing automated AI review tools that act as a "Pre-PD" review gate. Authors run drafts through AI to check technical content, style compliance, grammar, and cross-reference integrity before a human reviewer sees it. [Source: Geotechnical Report Workflows notebook]

17. The app uses a "Rule Matrix" for mechanical syntax and formatting checks, with developers actively mapping prompt engineering frameworks to give the AI "analytical depth" for assessing "Technical Validity" (checking if methods are justified and conclusions logically derive from evidence). [Source: Geotechnical Report Workflows notebook]

18. If AI is used, it must be documented in the Project Management Plan (PMP). [Source: Geotechnical Report Workflows notebook]

19. Governance rule: "Communicate where and how digital tools, inclusive of AI, is used so technical and PD reviews can be tailored accordingly." [Source: Geotechnical Report Workflows notebook]

20. Training warns that AI is "a drafting and proofing tool, not a replacement for thinking," instructing reviewers to be alert to AI "hallucinations," American English spelling, and "overly enthusiastic language." [Source: Geotechnical Report Workflows notebook]

### AI-Specific Error Classes in Geotechnical Reports

21. Fabricated citations that look authoritative (e.g., NZS 4407:2015 for SPT (Standard Penetration Test) -- a roading standard). [Source: strategic-bets.md, Bet 2]

22. Correct-range-but-wrong values (plausible SPT N-value, wrong borehole). [Source: strategic-bets.md, Bet 2]

23. Method-correct but context-wrong (valid design method applied to wrong soil classification). [Source: strategic-bets.md, Bet 2]

24. Fluent interpolation beyond data (ground conditions between investigation points stated as fact, not inference). [Source: strategic-bets.md, Bet 2]

## Standards Referenced

No specific standards clauses referenced in this evidence. The evidence is industry practice and editorial commentary.

## Open Questions

- How widespread is the "Pre-PD" AI review gate pattern beyond the single NZ consultancy documented here?
- Are professional bodies (IPENZ/Engineering New Zealand, ICE, BGA) developing formal guidance on AI disclosure requirements for geotechnical reports?
- What is the timeline for insurers (professional indemnity) to begin differentiating AI-assisted vs. manually-produced reports in their underwriting?
- How are firms measuring whether AI-assisted junior engineers are developing equivalent domain competence to those trained without AI?

## Further Reading

- Ground Engineering Magazine archive (2025-2026 issues covering AI adoption in geotechnical engineering)
- Redline `docs/research/software-development/20260526-accelerate-problem-diagnosis-ai-era.md` for structural mapping to DORA 2024-2026 findings on AI-assisted software development
- BGA (British Geotechnical Association) committee publications on AI in ground engineering
- Engineering New Zealand guidance on AI use in professional engineering practice (if published)
