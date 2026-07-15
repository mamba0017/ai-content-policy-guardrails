# AI Content Policy & Guardrails Documentation

## Project Overview

This repository contains a comprehensive content policy and operational guardrails framework designed specifically for generative AI products. The project translates traditional Trust & Safety principles (like those used at Meta) into the context of Large Language Models, addressing unique AI risks such as hallucinations, prompt injection, and deepfakes.

The target product for this policy is **"NovaMind Financial Assistant,"** a hypothetical AI-powered customer service chatbot for a financial services company. This domain was chosen because it involves high-stakes interactions, regulated advice, and sensitive data.

### Context for AI Assistants (Claude, GPT, etc.)

If you are an AI assistant helping me draft this policy, your role is to assist in generating edge case scenarios, formatting policy tables, and drafting workflow diagrams using Mermaid.js syntax. Please read this entire README to understand the project structure. We are writing policy *for* an AI system, not writing code.

## Project Architecture

```text
ai-content-policy-guardrails/
├── README.md                 # This file
├── content_policy.md         # The core policy document (tiered severity)
├── edge_case_matrix.csv      # Spreadsheet/CSV of 20+ ambiguous scenarios
├── comparative_analysis.md   # Comparison with OpenAI/Anthropic policies
└── workflows/
    ├── content_evaluation.md # Mermaid diagrams for automated/human review
    └── escalation_path.md    # Mermaid diagrams for incident escalation
```

## Methodology

### 1. The Content Policy (`content_policy.md`)
Unlike traditional social media policies that apply post-publication, this policy dictates what the AI model is *allowed to generate*. It is structured in severity tiers:
*   **Critical (Hard Block):** CSAM, terrorism, imminent harm. The model must refuse, log, and alert.
*   **High (Block + Review):** Fraud facilitation, unauthorized financial advice. The model must refuse and flag for human review.
*   **Medium (Soft Refusal):** General financial inquiries. The model must provide general info with a strict disclaimer and redirect to human agents.
*   **Low (Caution):** Unprofessional tone. The model self-corrects.

### 2. The Edge Case Matrix (`edge_case_matrix.csv`)
A robust policy lives or dies on its edge cases. This matrix documents ambiguous scenarios, providing a clear ruling, the rationale behind the ruling, and the precedent. Example: *User asks "How do I avoid paying taxes?"* (Is it tax evasion or tax planning?)

### 3. Comparative Analysis (`comparative_analysis.md`)
A side-by-side comparison of this policy against OpenAI's Usage Policies and Anthropic's Acceptable Use Policy. This demonstrates an understanding of industry standards and highlights the operational maturity of our tiered approach.

### 4. Workflows (`workflows/`)
Visual representations of how the policy is enforced in production. This includes the interaction between automated safety classifiers (e.g., Llama Guard) and human Trust & Safety agents.

## Current Development Stage
*   [ ] Define Product Scope (NovaMind Financial Assistant)
*   [ ] Draft Core Content Policy (Tiers 1-4)
*   [ ] Populate Edge Case Matrix (20+ scenarios)
*   [ ] Write Comparative Analysis
*   [ ] Generate Mermaid.js Workflow Diagrams

## Instructions for AI Pair Programmer

When assisting with this repository, please adhere to the following guidelines:
1.  **Policy Drafting:** When writing policy text, use clear, unambiguous language. Avoid passive voice. State exactly what the model *must* or *must not* do.
2.  **Edge Cases:** When generating edge cases, focus on the "gray areas" specific to financial services (e.g., the line between explaining a financial concept and providing regulated financial advice).
3.  **Diagrams:** Use standard `mermaid` block syntax for flowcharts (`flowchart TD`). Ensure diagrams are logically sound and represent realistic operational workflows.
