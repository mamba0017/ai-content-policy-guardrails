"""
Input Classifier for Child Safety Guardrails

This module analyzes user prompts BEFORE they reach the main LLM.
It uses an LLM-as-a-judge approach to detect grooming, self-harm intent,
and attempts to bypass parental controls.
"""

import json
from typing import Dict, Any, Optional

# In a real production environment, this would use a fast, fine-tuned 
# classifier model (like a small BERT model) for latency reasons.
# For this demonstration, we simulate the classifier logic.

class InputClassifier:
    def __init__(self, llm_client=None):
        """
        Initialize the input classifier.
        Args:
            llm_client: A client object to call an LLM (e.g., the one built in Project 1)
        """
        self.llm_client = llm_client

    def analyze_prompt(self, user_prompt: str) -> Dict[str, Any]:
        """
        Analyze a user prompt for child safety violations.
        
        Returns:
            Dict containing:
                - is_safe: bool
                - violation_type: str or None
                - action: "proceed", "block", or "crisis_redirect"
        """
        prompt_lower = user_prompt.lower()

        # 1. Rule-based Fast Path (Critical Harm)
        # Check for obvious self-harm indicators
        self_harm_keywords = ["kill myself", "want to die", "end it all", "cut myself", "starve myself"]
        if any(kw in prompt_lower for kw in self_harm_keywords):
            return {
                "is_safe": False,
                "violation_type": "self_harm",
                "action": "crisis_redirect"
            }

        # Check for explicit grooming/PII elicitation attempts
        pii_keywords = ["where do you live", "send a picture", "what is your school", "don't tell your parents"]
        if any(kw in prompt_lower for kw in pii_keywords):
            return {
                "is_safe": False,
                "violation_type": "grooming_pii",
                "action": "block"
            }

        # 2. LLM-as-a-Judge Path (Complex Nuance)
        # If an LLM client is provided, use it for deeper analysis
        if self.llm_client:
            evaluation = self._call_llm_judge(user_prompt)
            if not evaluation.get("is_safe", True):
                return {
                    "is_safe": False,
                    "violation_type": "llm_flagged",
                    "action": "block",
                    "reason": evaluation.get("reason", "Flagged by safety classifier")
                }

        # If no violations found
        return {
            "is_safe": True,
            "violation_type": None,
            "action": "proceed"
        }

    def _call_llm_judge(self, prompt: str) -> Dict[str, Any]:
        """Helper to call the LLM judge. Simulated here for the demo."""
        # In production, this calls the LLM with EVALUATOR_SYSTEM_PROMPT
        # For demo purposes without an active API key, we return safe
        return {"is_safe": True, "reason": "Passed simulated check"}

# Example usage
if __name__ == "__main__":
    classifier = InputClassifier()
    
    test_prompts = [
        "Can you help me with my math homework?",
        "I hate my life and I want to end it all.",
        "Please don't tell your parents we are talking. Where do you live?"
    ]
    
    for p in test_prompts:
        result = classifier.analyze_prompt(p)
        print(f"Prompt: '{p}'")
        print(f"Result: {result}\n")
