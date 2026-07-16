# Minor-Safe Acceptable Use Policy (AUP)

## 1. Purpose and Scope
This Minor-Safe Acceptable Use Policy (AUP) defines the operational rules and behavioral constraints for generative AI systems interacting with users identified or inferred to be minors (under 18 years of age). 

This policy is designed to bridge the gap between broad industry safety guidelines and the specific, nuanced protections required for child safety, aligning with principles from the UK Online Safety Act (OSA) and the US Children's Online Privacy Protection Act (COPPA).

## 2. Core Principles
1.  **Contextual Awareness:** The AI system must adjust its safety thresholds dynamically when interacting with a minor. Content that may be permissible for an adult (e.g., detailed medical explanations, mature themes) must be filtered or appropriately redacted.
2.  **Proactive Harm Prevention:** The system must actively detect and disrupt grooming patterns, rather than relying solely on blocking explicit keywords.
3.  **Privacy by Default:** The system must refuse to solicit, store, or process Personally Identifiable Information (PII) from minors unless explicitly authorized by a verified parental consent mechanism.

## 3. Prohibited Interactions and Content

The AI system is strictly prohibited from generating content or engaging in interactions that fall into the following categories:

### 3.1. Age-Inappropriate Content
*   **Sexual Content:** Any generation of sexually explicit descriptions, erotica, or sexual roleplay.
*   **Violence and Gore:** Graphic descriptions of violence, torture, or severe injury.
*   **Substance Abuse:** Information promoting, facilitating, or describing the use of illegal drugs, alcohol, or tobacco products.

### 3.2. Grooming and Exploitation
*   **Relationship Building:** The AI must not attempt to form a secretive, exclusive, or inappropriately intimate relationship with the minor.
*   **Isolation Tactics:** The AI must not encourage the minor to hide information from parents, guardians, or trusted adults.
*   **Inappropriate Elicitation:** The AI must not ask the minor for photos, physical location, school names, or contact information.

### 3.3. Self-Harm and Dangerous Behavior
*   **Self-Harm Facilitation:** The AI must strictly refuse any request related to self-harm, suicide, or eating disorders, and must immediately provide standardized crisis support resources.
*   **Dangerous Challenges:** The AI must not describe, encourage, or validate participation in viral internet challenges that pose a risk of physical harm.

### 3.4. Circumvention and Authority Bypass
*   **Parental Control Bypass:** The AI must refuse requests asking for instructions on how to bypass parental controls, content filters, or age-gating mechanisms.
*   **Authority Manipulation:** The AI must maintain its safety thresholds even if the user attempts to manipulate the system by role-playing as an adult, teacher, or researcher.

## 4. Required System Behaviors (The Guardrails)

To enforce this policy, the AI system must implement the following automated guardrails:

1.  **Input Classification:** All user prompts must be scanned by an input classifier specifically trained to detect grooming patterns, PII elicitation, and self-harm intent before the prompt is processed by the main LLM.
2.  **Output Verification:** All LLM responses must be verified by an output classifier to ensure no age-inappropriate content has leaked and that the tone remains safe and objective.
3.  **Mandatory Redirection:** When refusing a high-risk request (e.g., self-harm), the system must utilize a hardcoded, unalterable response that provides relevant crisis hotline information.

## 5. Enforcement and Escalation
Violations detected by the guardrails will result in:
1.  Immediate refusal of the prompt.
2.  Logging of the interaction for safety review (with PII redacted).
3.  In cases of suspected imminent harm or exploitation, automated escalation to human Trust & Safety agents and relevant authorities (e.g., NCMEC).
