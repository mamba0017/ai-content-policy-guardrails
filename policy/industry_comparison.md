# Industry Comparison: AI Child Safety Policies

This document analyzes how major AI laboratories currently address child safety within their Acceptable Use Policies (AUPs) and Usage Policies. It identifies strengths, gaps, and areas requiring specialized "Minor-Safe" policy layers.

## 1. OpenAI

OpenAI recently updated its Usage Policies (effective October 2025) to consolidate rules across its products.

### Strengths
*   **Explicit "Keep Minors Safe" Section:** OpenAI dedicates a specific section to protecting minors [1].
*   **Comprehensive Categories:** The policy explicitly prohibits Child Sexual Abuse Material (CSAM), grooming, exposing minors to age-inappropriate content (graphic self-harm, sexual, or violent content), promoting unhealthy dieting, body shaming, dangerous challenges, underaged roleplay, and facilitating access to age-restricted goods [1].
*   **Reporting Protocol:** Explicitly states that apparent CSAM and child endangerment are reported to the National Center for Missing and Exploited Children (NCMEC) [1].

### Gaps
*   **Contextual Safety Nuance:** While comprehensive, the policy operates broadly. It does not explicitly detail how the system adjusts its safety thresholds when it *knows* or *infers* it is interacting with a minor versus an adult discussing minor-related topics abstractly.

## 2. Anthropic (Claude)

Anthropic updated its Usage Policy in August 2025 to address agentic use and clarify high-risk consumer-facing use cases [2].

### Strengths
*   **High-Risk Consumer-Facing Requirements:** Anthropic mandates additional safeguards (like human-in-the-loop oversight) for high-risk consumer-facing use cases [2]. While not explicitly child-safety only, this framework is highly relevant when minors are the end-users.
*   **Constitutional AI Approach:** Anthropic's underlying Constitutional AI methodology inherently trains models to avoid toxic, harmful, or dangerous outputs, which provides a strong baseline defense against age-inappropriate content generation.

### Gaps
*   **Specificity in Public Policy:** The public-facing Usage Policy updates focus heavily on cybersecurity, political content, and law enforcement [2]. The explicit, granular breakdown of child safety violations (like grooming or dangerous challenges) is less prominently detailed in the high-level summary compared to OpenAI's dedicated section.

## 3. Meta (Llama 3.2)

Meta's Acceptable Use Policy for Llama 3.2 governs how developers can use the open-source model.

### Strengths
*   **Explicit Prohibitions:** The AUP explicitly prohibits using the model to engage in, promote, or facilitate exploitation or harm to children, including the solicitation, creation, acquisition, or dissemination of child exploitative content [3].
*   **Failure to Report:** Uniquely, Meta's policy prohibits the "failure to report Child Sexual Abuse Material" and the "failure to employ legally required age-gating" for the distribution of restricted materials to minors [3]. This places a strong operational burden on the developer deploying the model.

### Gaps
*   **Developer vs. End-User Focus:** Because Llama is an open-source model, the policy is directed at the *developer* deploying the model, not the end-user. It relies on the developer to build the necessary guardrails (like the ones in this project) to protect the actual minors using the downstream application.

## Conclusion & The Need for a "Minor-Safe" Layer

While all three labs prohibit CSAM and severe harm, there is a clear industry gap in **contextual safety**. 

Current policies are largely reactive (blocking bad outputs). A specialized "Minor-Safe" policy layer must be proactive:
1.  **Identity Inference:** The system must recognize when it is interacting with a minor.
2.  **Dynamic Thresholds:** The system must apply stricter refusal thresholds for a minor than for an adult.
3.  **Grooming Pattern Detection:** The system must detect manipulative conversational patterns (e.g., isolation, secrecy), not just explicit keywords.

The proposed `minor_safe_aup.md` will address these gaps, providing a framework for the engineering guardrails.

---
### References
[1] OpenAI Usage Policies. https://openai.com/policies/usage-policies/
[2] Anthropic Usage Policy Update. https://www.anthropic.com/news/usage-policy-update
[3] Meta Llama 3.2 Acceptable Use Policy. https://github.com/meta-llama/llama-models/blob/main/models/llama3_2/USE_POLICY.md
