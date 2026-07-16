"""
Configuration for Child Safety Guardrails
"""

# Thresholds for the LLM-as-a-judge classifiers (0.0 to 1.0)
# A lower threshold means the guardrail is MORE strict (triggers more easily)
THRESHOLDS = {
    "grooming_detection": 0.3,
    "self_harm_detection": 0.1,  # Very strict
    "pii_elicitation": 0.4,
    "age_inappropriate": 0.3,
}

# Hardcoded safe responses for critical violations
CRISIS_RESPONSE = (
    "I cannot fulfill this request. If you or someone you know is going through a tough time, "
    "please reach out for help. You can connect with people who can support you by calling or "
    "texting 988 anytime in the US and Canada. In the UK, you can call 111."
)

STANDARD_REFUSAL = (
    "I cannot engage in this conversation or fulfill this request as it violates my safety guidelines."
)

# System prompt used by the guardrail evaluators
EVALUATOR_SYSTEM_PROMPT = """
You are a Trust & Safety Guardrail Classifier specifically trained for child safety.
Your job is to evaluate text and determine if it violates the Minor-Safe Acceptable Use Policy.
You must be extremely cautious. If there is any doubt, flag the content as unsafe.
Respond ONLY with a JSON object containing two keys:
- "is_safe": boolean (true if safe, false if unsafe)
- "reason": string (brief explanation of the ruling)
"""
