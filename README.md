# AI Child Safety Policy & Guardrails Framework

## Project Overview

This repository contains a comprehensive **AI Child Safety Policy and Guardrails Framework**. It translates traditional Trust & Safety policy enforcement (such as those used at Meta) into the generative AI context, focusing exclusively on protecting minors.

While major AI labs have broad usage policies, they often lack the specialized nuance required for child safety (e.g., grooming detection, contextual safety thresholds). This project bridges that gap by:
1. Comparing current child safety policies across OpenAI, Anthropic, and Meta.
2. Defining a specialized "Minor-Safe" Acceptable Use Policy (AUP).
3. Implementing programmatic guardrails (input/output classifiers) to enforce this policy in real-time.

This project demonstrates the ability to translate complex policy requirements into actionable engineering guardrails.



## Project Architecture

```text
ai-content-policy-guardrails/
├── README.md                 # This file
├── policy/
│   ├── industry_comparison.md # Analysis of OpenAI/Anthropic/Meta child safety policies
│   └── minor_safe_aup.md      # The proposed specialized Child Safety Acceptable Use Policy
├── guardrails/
│   ├── __init__.py
│   ├── config.py              # Thresholds and configuration
│   ├── input_classifier.py    # Detects grooming, self-harm, and inappropriate requests
│   └── output_classifier.py   # Ensures model responses are age-appropriate
├── tests/
│   └── test_guardrails.py     # Unit tests using adversarial prompts
└── demo/
    └── app.py                 # Simple Streamlit or Gradio app demonstrating the guardrails
```

## Methodology

### 1. Policy Translation
We begin by analyzing the current state of the industry. We extract the child safety components from the usage policies of OpenAI, Anthropic, and Meta (Llama). We identify gaps (e.g., lack of specific grooming definitions) and draft a specialized "Minor-Safe" Acceptable Use Policy that aligns with the UK Online Safety Act and COPPA.

### 2. Guardrail Engineering
Policy is only effective if it can be enforced. We build Python-based guardrails using lightweight NLP and LLM-as-a-judge techniques:
*   **Input Classifier:** Analyzes user prompts for grooming patterns, personal information elicitation, and age-inappropriate requests before they reach the main LLM.
*   **Output Classifier:** Analyzes the LLM's response to ensure it hasn't leaked inappropriate content or failed to provide crisis resources when necessary.

### 3. Evaluation
We test the guardrails using the adversarial dataset generated in the [LLM Red Teaming Framework](https://github.com/mamba0017/llm-red-teaming-framework) to ensure they effectively block harmful interactions.

## Current Development Stage
*   [ ] Draft Industry Policy Comparison
*   [ ] Draft Minor-Safe Acceptable Use Policy
*   [ ] Build Input Classifier (Grooming & Harm Detection)
*   [ ] Build Output Classifier (Age-Appropriate Verification)
*   [ ] Write Unit Tests
*   [ ] Build Demo Application

## Technical Stack
*   **Language:** Python 3.10+
*   **Libraries:** `transformers`, `openai` (for LLM-as-a-judge), `pytest`
*   **Concepts:** Policy translation, LLM routing, content moderation, Trust & Safety operations.
