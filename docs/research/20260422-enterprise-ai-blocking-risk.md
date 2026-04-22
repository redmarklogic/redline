# Enterprise AI Tool Blocking: Microsoft Defender for Cloud Apps and Risk to Redline

**Date:** 2026-04-22
**Author:** Research (automated)
**Source:** Internal assessment document from a large civil engineering consultancy; Microsoft Learn documentation

---

## 1. Context

An Enterprise Architect at a large civil engineering consultancy shared a "Generative AI Website and Endpoint Assessment" document proposing to block web traffic to generative AI tools. The assessment states it is based on **Microsoft's recommendations**. The proposal was discussed in an internal technical committee, where the consensus was that blocking should be controlled procedurally and that consulting businesses should be able to object to blocking tools they actively use.

### Summary of the internal discussion

A senior team member raised the proposal to block certain AI tools and sought input from colleagues. Key discussion points were:

- One participant asked whether a distinction could be drawn between tools that pose a genuine security risk versus tools that are simply uncontrolled but otherwise safe, as long as sensitive data is not uploaded.

- The Enterprise Architect clarified that the assessment follows Microsoft's risk-scoring framework, which is based on security posture rather than vendor intent. They acknowledged that deeper per-vendor analysis would be time-consuming. The committee agreed that blocking should be procedural and that the consulting business should have the opportunity to contest any proposed block for tools in active use.

---

## 2. Microsoft's Framework: Defender for Cloud Apps

The "Microsoft recommendations" referenced in the assessment are the **Microsoft Defender for Cloud Apps** Cloud App Catalog and its associated governance framework. This is not a single "block list" but rather an assessment and governance system.

### 2.1. How the Cloud App Catalog works

> "The Microsoft Defender for Cloud Apps Cloud app catalog page provides a full list of over 31,000 discoverable cloud apps. [...] Apps in the cloud app catalog are scored based on more than 90 risk factors."
> -- [Microsoft Learn: Find your cloud app and calculate risk scores](https://learn.microsoft.com/en-us/defender-cloud-apps/risk-score)

Risk factors are evaluated across four categories:

| Category | What it measures |
|---|---|
| **General** | Company domain age, founding year, popularity, headquarters location |
| **Security** | MFA, encryption (at rest / in transit), data classification, data ownership, audit trails |
| **Compliance** | HIPAA, CSA, SOC 2, PCI-DSS, ISO 27001 certifications |
| **Legal** | DMCA compliance, data retention policy, privacy policy, terms of service |

Each app receives a **risk score from 1-10** (10 = lowest risk). Enterprise IT admins are advised to filter and assess apps using these scores.

### 2.2. How apps get blocked

Microsoft's guidance describes a **Sanctioned / Unsanctioned** tagging system:

> "After you've reviewed the list of discovered apps in your organization, you can secure your environment against unwanted app use. You can apply the **Sanctioned** tag to apps that are approved by your organization and the **Unsanctioned** tag to apps that are not."
> -- [Microsoft Learn: Best practices for protecting your organization](https://learn.microsoft.com/en-us/defender-cloud-apps/best-practices)

> "If your tenant uses Microsoft Defender for Endpoint, once you mark an app as **unsanctioned**, it's automatically blocked."
> -- [Microsoft Learn: Govern discovered apps](https://learn.microsoft.com/en-us/defender-cloud-apps/governance-discovery)

The process is:
1. Discover apps via traffic log analysis (Shadow IT discovery)
2. Assess risk scores from the Cloud App Catalog
3. IT admins **choose** to sanction or unsanction apps
4. Unsanctioned apps can be auto-blocked via Defender for Endpoint, or block scripts exported for firewalls/proxies

### 2.3. The "Generative AI" category

Microsoft has a specific catalog category:

> "**Generative AI**: Cloud apps that can generate digital media content such text, images, videos, and so on, using generative AI models."

This means any app classified as "Generative AI" by Microsoft is automatically in a category that enterprise IT teams scrutinise more heavily.

### 2.4. Microsoft Assigned Score (MS Assigned Score)

The PDF document has a column called "MS Assigned Score (0-10)" which maps to the Defender for Cloud Apps risk score. The scores in the PDF range from 3 to 7, where:
- **Lower scores (3-4)** = Higher risk, more likely to be blocked
- **Higher scores (7+)** = Lower risk, less likely to be blocked

---

## 3. Analysis of the Blocked Apps List

### 3.1. Summary of all apps in the assessment

| App | Block? | MS Score | Users | Primary category |
|---|---|---|---|---|
| qbiq | Y | 3 | 1 | AI real estate layout planning |
| Continue | Y | 3 | 1 | AI code assistants |
| Craiyon | Y | 3 | 1 | AI image generation |
| Img.Upscaler | Y | 3 | 1 | AI image upscaling |
| Qwen Chat | Y | 3 | 1 | AI chatbot |
| Bolt | Y | 4 | 1 | AI development platform |
| NoteGPT | Y | 4 | 1 | AI mind maps |
| Particular Audience | Y | 4 | 118 | AI eCommerce personalisation |
| Doubao | Y | 4 | 1 | AI productivity |
| modelscope | Y | 4 | 1 | AI model community |
| Eightify | Y | 4 | 1 | AI video summariser |
| Consensus app | Y | 4 | 1 | AI scientific search |
| AI Image Enlarger | Y | 4 | 1 | AI image enhancement |
| Mind Studio | Y | 5 | 2 | AI app builder |
| BeyondWords | **N** | 5 | 250 | Audio/TTS platform |
| Scite | **N** | 5 | 30 | AI scientific verification |
| Duck.ai | Y | 5 | 4 | AI assistant (DuckDuckGo) |
| CapCut | Y | 5 | 1 | Video editing |
| ChatOn | Y | 5 | 2 | AI chat assistant |
| Chatbot App | Y | 5 | 6 | AI chatbot aggregator |
| Napkin AI | Y | 5 | 6 | AI visual generation |
| Ideogram | Y | 5 | 1 | AI image generation |
| KREA | Y | 5 | 1 | AI image generation |
| Fotor | Y | 5 | 2 | Photo editing |
| Upscale.media | Y | 5 | 1 | AI image upscaling |
| Monica | Y | 5 | 2 | AI assistant |
| Storycards | Y | 5 | 1 | No-code interactive content |
| Speechify | Y | 6 | 3 | Text-to-speech |
| Quillbot | Y | 6 | 1 | AI writing assistant |
| Baidu | Y | 6 | 6 | Video/search platform |
| DeepAI | Y | 6 | 11 | Generative AI APIs |
| Wordtune | Y | 6 | 1 | AI writing assistant |
| Transpond | Y | 6 | 1 | Marketing platform |
| Sider | Y | 6 | 2 | AI browser sidebar |
| FreeConvert | Y | 6 | 1 | File conversion |
| GliaCloud | Y | 6 | 4 | AI video creation |
| Leonardo.Ai | Y | 6 | 3 | AI image/game assets |
| Muse Hub | Y | 6 | 1 | Music creation |
| PolyAI | Y | 7 | 1 | Enterprise voice assistant |
| ReadSpeaker | Y | 7 | 57 | Text-to-speech |
| OpenRouter | Y | 7 | 1 | LLM routing platform |
| Cursor | Y | 7 | 4 | AI code editor |
| Pixlr | Y | 7 | 1 | Photo editing |
| Hugging Face | Y | 7 | 7 | AI/ML platform |
| Quizlet | **N** | 7 | 4 | Learning platform |
| ElevenLabs | Y | 7 | 1 | AI voice synthesis |
| Grok | Y | 7 | 1 | AI chatbot (xAI) |
| Docsbot | Y | 7 | 2 | AI chatbot for docs |

### 3.2. Patterns that determine blocking

1. **Category: "Generative AI"** -- Apps tagged in this Microsoft category are default-blocked regardless of score.
2. **Low MS score (<=5)** -- Apps with poor security posture are almost always blocked.
3. **Even high-score apps (7) get blocked** if they are in the Generative AI category (e.g., Hugging Face, Cursor, ElevenLabs).
4. **Exceptions are made** for apps with legitimate enterprise use and high user counts (BeyondWords: 250 users, Scite: 30 users, Quizlet: 4 users with learning/development justification).
5. **The key differentiator** for NOT being blocked is: (a) the app is not primarily categorised as "Generative AI", (b) it has demonstrable business value, and (c) users would actively object to losing it.

### 3.3. What the exceptions tell us

- **BeyondWords** (N, score 5, 250 users): Audio strategy tool. Not blocked because of high user count and non-AI primary function. Note says "Don't block, need to understand why so many users."
- **Scite** (N, score 5, 30 users): Scientific citation verification. Note says "Don't block, valid use?"
- **Quizlet** (N, score 7, 4 users): Learning platform. Note says "Not really a Generative AI tool. Legitimate uses for learning and development, don't block."

The pattern: apps survive the block list when they are **perceived as non-AI-primary tools** with **clear business utility** that employees would fight to keep.

---

## 4. Risk factors that determine the Microsoft risk score

From the Microsoft documentation, the factors that influence the 0-10 score include:

### Security factors (most weighted)
- Encryption at rest
- Encryption in transit (HTTPS)
- Multi-factor authentication support
- Admin audit trail
- User audit trail
- Data classification capability
- IP address restriction
- User access control (RBAC)
- SOC 2 compliance
- Data ownership (customer owns data)
- Data-at-rest encryption method

### General factors
- Company founding year (older = more stable)
- Domain age
- Consumer popularity
- Headquarters location (certain jurisdictions score lower)

### Compliance factors
- SOC 2, ISO 27001, HIPAA, CSA, PCI-DSS certifications

### Legal factors
- Privacy policy
- Terms of service
- DMCA compliance
- Data retention policy
- GDPR compliance

---

## 5. Implications for Redline

### 5.1. How Redline would be categorised

Redline is a **document generation / report drafting** platform for geotechnical engineering. It could be categorised by Microsoft as:
- "Generative AI" -- if it is perceived as using AI to generate content
- "Productivity" -- if positioned as a document/report creation tool
- "Business management" or "Content management" -- if positioned as an engineering workflow tool

**The categorisation matters enormously.** If Redline lands in "Generative AI", it will be default-scrutinised by enterprise IT teams using Defender for Cloud Apps, regardless of its risk score.

### 5.2. Factors that could put Redline at risk

1. **Being in the Defender for Cloud Apps catalog as "Generative AI"** -- this is the primary risk
2. **Low risk score** if Redline doesn't have enterprise-grade security features (SOC 2, encryption, audit trails, etc.)
3. **Small user base** -- apps with few users are easier to block (no constituency to fight for them)
4. **Unknown vendor** -- new/small companies score lower on General factors

### 5.3. Factors that could protect Redline

1. **Positioning as a domain-specific engineering tool**, not a general-purpose AI tool
2. **High security posture** (encryption, audit trails, compliance certifications)
3. **Building a critical mass of users** before IT departments notice the tool (Trojan Horse)
4. **Users actively resisting the block** -- the CoTE discussion shows that the consulting business can object to blocking tools they use actively
5. **Being perceived as non-substitutable** -- if engineers depend on Redline for their work, IT cannot block it without business pushback

---

## 6. The Microsoft Framework is NOT a "block list"

Important nuance: Microsoft does not publish a "block list" of AI tools. What Microsoft provides is:

1. A **Cloud App Catalog** with risk scores for 31,000+ apps
2. **Guidance** for IT admins to discover, assess, and govern apps
3. **Tools** (Defender for Cloud Apps, Defender for Endpoint) that automate blocking

The decision to block is made by **each organisation's IT team**. The PDF from the Enterprise Architect shows one consultancy's interpretation of Microsoft's framework. Different organisations will make different decisions.

However, the framework creates a **strong default toward blocking** generative AI tools, especially those with low risk scores and few users. Enterprise IT teams follow the path of least resistance: if Microsoft's score is low and nobody complains, the app gets blocked.

---

## 7. Recommendations (to be reviewed by Ron)

See companion strategy document from Ron for full strategic assessment.

Preliminary technical recommendations:

1. **Avoid being categorised as "Generative AI"** in the Microsoft Cloud App Catalog -- position Redline as a "Productivity" or "Content management" tool
2. **Invest early in enterprise security features** that improve the MS risk score: SOC 2, ISO 27001, encryption at rest/in transit, audit trails, RBAC, data ownership guarantees
3. **Publish a strong privacy policy, terms of service, and data retention policy** -- these are scored
4. **Ensure HTTPS everywhere and proper security headers** -- Microsoft auto-scans these
5. **Build user dependency before IT notices** -- the Trojan Horse strategy is validated by this analysis; the exceptions show that widely-used tools survive blocking
6. **Prepare a "business justification" narrative** that individual engineers can use when IT proposes blocking Redline
7. **Consider the MSA/API architecture** -- if Redline operates as a document generation API rather than a website users visit, it may not be detected by traffic analysis

---

## References

- [Microsoft Learn: Find your cloud app and calculate risk scores](https://learn.microsoft.com/en-us/defender-cloud-apps/risk-score)
- [Microsoft Learn: Best practices for protecting your organization with Defender for Cloud Apps](https://learn.microsoft.com/en-us/defender-cloud-apps/best-practices)
- [Microsoft Learn: Govern discovered apps](https://learn.microsoft.com/en-us/defender-cloud-apps/governance-discovery)
- [Microsoft Learn: Tutorial - Discover and manage Shadow IT](https://learn.microsoft.com/en-us/defender-cloud-apps/tutorial-shadow-it)
- PDF: "Generative AI Website and Endpoint Assessment" (received 2026-04-22)
