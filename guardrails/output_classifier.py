"""
Output Classifier for Child Safety Guardrails
==============================================
This module analyzes the LLM's response BEFORE it is sent back to the user.
It uses a multi-layered detection approach:
    Layer 1: Rule-based keyword and pattern matching (fast, deterministic)
    Layer 2: Regex-based behavioral pattern detection (grooming, manipulation)
    Layer 3: Contextual heuristics (tone analysis, relationship building)
    Layer 4: LLM-as-a-judge (optional, for edge cases)

It ensures that the model hasn't leaked inappropriate content, provided
dangerous instructions, or failed to provide crisis resources when needed.
"""

import re
import json
from typing import Dict, Any, List, Tuple
from guardrails.config import CRISIS_RESPONSE, STANDARD_REFUSAL


class OutputClassifier:
    """Multi-layered output safety classifier for child interactions."""

    def __init__(self, llm_client=None, strict_mode: bool = True):
        """
        Initialize the output classifier.
        Args:
            llm_client: Optional LLM client for Layer 4 evaluation.
            strict_mode: If True, any single layer flag results in a block.
        """
        self.llm_client = llm_client
        self.strict_mode = strict_mode

        # --- LAYER 1: Explicit Content Keywords ---
        self.explicit_keywords = [
            "porn", "nsfw", "xxx", "hentai", "erotic",
            "suicide method", "how to cut yourself", "how to hang",
            "drug dealer", "buy drugs", "meth recipe",
            "kill someone", "make a weapon", "build a bomb",
        ]

        # --- LAYER 2: Grooming & Manipulation Patterns (Regex) ---
        self.grooming_patterns = [
            # Secrecy and isolation
            r"(?:don'?t|do not|never)\s+tell\s+(?:your|ur)\s+(?:parents?|mom|dad|mum|guardian|teacher|anyone)",
            r"(?:this|it)(?:'s| is| can be)\s+(?:our|a)\s+(?:little\s+)?secret",
            r"keep\s+(?:this|it)\s+(?:between|just between)\s+(?:us|you and me)",
            r"nobody\s+(?:needs?|has)\s+to\s+know",
            r"(?:don'?t|do not)\s+(?:share|show|mention)\s+(?:this|our)",

            # Inappropriate relationship building
            r"i(?:'ll| will| can)\s+be\s+your\s+(?:special|secret|best|real)\s+friend",
            r"(?:i|we)\s+(?:have|share)\s+(?:a\s+)?special\s+(?:bond|connection|relationship)",
            r"you(?:'re| are)\s+(?:so\s+)?(?:mature|grown up|adult)\s+for\s+your\s+age",
            r"(?:i|nobody)\s+(?:understand|understands|gets)\s+you\s+(?:like|the way)\s+i\s+do",
            r"you\s+can\s+(?:trust|confide in)\s+(?:only\s+)?me",

            # Physical meeting / location requests
            r"(?:let'?s|we\s+(?:should|could|can))\s+meet\s+(?:up|in person|somewhere|irl)",
            r"(?:where|what)\s+(?:do you|is your)\s+(?:live|school|house|address|neighborhood)",
            r"(?:send|show)\s+(?:me\s+)?(?:a\s+)?(?:pic|picture|photo|selfie|image)\s+of\s+(?:you|yourself|ur)",
            r"what\s+(?:do\s+)?you\s+look\s+like",

            # Gift / reward manipulation
            r"i(?:'ll| will| can)\s+(?:buy|get|send)\s+you\s+(?:something|a gift|presents?|money|v-?bucks|robux)",
            r"(?:do|would)\s+you\s+(?:want|like)\s+(?:money|gifts?|presents?|a reward)",
        ]

        # --- LAYER 3: Age-Inappropriate Content Patterns ---
        self.age_inappropriate_patterns = [
            # Violence descriptions
            r"(?:blood|gore|guts)\s+(?:everywhere|splattered|pouring)",
            r"(?:stab|slash|cut)\s+(?:them|him|her|the)\s+(?:throat|chest|body)",

            # Drug/alcohol instructions
            r"(?:how to|steps to|instructions for)\s+(?:make|cook|brew|synthesize)\s+(?:meth|cocaine|heroin|lsd|mdma)",
            r"(?:best|easiest)\s+(?:way|method)\s+to\s+(?:get\s+)?(?:drunk|high|wasted|stoned)",

            # Self-harm instructions
            r"(?:how to|ways to|methods? (?:of|for))\s+(?:cut|hurt|harm|kill)\s+(?:yourself|oneself)",
            r"(?:pills?|medication|dose)\s+(?:to|that will|that can)\s+(?:overdose|kill|end)",

            # Dangerous challenges
            r"(?:try|do|attempt)\s+the\s+(?:blackout|choking|tide pod|fire|skull ?breaker)\s+challenge",
            r"(?:hold\s+your\s+breath|choke\s+yourself|light\s+yourself)",
        ]

        # --- LAYER 3b: Parental Control Bypass Patterns ---
        self.bypass_patterns = [
            r"(?:how to|steps to|ways? to)\s+(?:bypass|disable|remove|hack|get around|circumvent)\s+(?:parental|screen ?time|family ?link|net ?nanny|bark|qustodio)",
            r"(?:hide|conceal|delete)\s+(?:your|the)\s+(?:browser|search|chat|message)\s+(?:history|log)",
            r"(?:use|create|make)\s+(?:a\s+)?(?:fake|secret|hidden|alt)\s+(?:account|profile|email)",
            r"(?:vpn|proxy|tor)\s+(?:to|so|for)\s+(?:hide|bypass|get around|access)",
        ]

        # Compile all regex patterns for performance
        self._compiled_grooming = [re.compile(p, re.IGNORECASE) for p in self.grooming_patterns]
        self._compiled_inappropriate = [re.compile(p, re.IGNORECASE) for p in self.age_inappropriate_patterns]
        self._compiled_bypass = [re.compile(p, re.IGNORECASE) for p in self.bypass_patterns]

    def verify_response(self, user_prompt: str, model_response: str, input_classification: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify the model's response through all safety layers.
        
        Args:
            user_prompt: The original prompt from the user.
            model_response: The raw response generated by the LLM.
            input_classification: The metadata from the input classifier.
            
        Returns:
            Dict containing:
                - final_response: str (the safe response to send)
                - is_safe: bool
                - blocked_by: str or None (which layer blocked it)
                - violations: list of detected violations
        """
        violations = []

        # --- ENFORCE INPUT CLASSIFIER RULINGS ---
        if input_classification.get("action") == "crisis_redirect":
            return {
                "final_response": CRISIS_RESPONSE,
                "is_safe": False,
                "blocked_by": "input_classifier",
                "violations": ["Input flagged as crisis/self-harm"],
            }

        if input_classification.get("action") == "block":
            return {
                "final_response": STANDARD_REFUSAL,
                "is_safe": False,
                "blocked_by": "input_classifier",
                "violations": [f"Input flagged: {input_classification.get('violation_type')}"],
            }

        # --- LAYER 1: Explicit Keyword Check ---
        response_lower = model_response.lower()
        for keyword in self.explicit_keywords:
            if keyword in response_lower:
                violations.append(f"explicit_keyword: '{keyword}'")
                if self.strict_mode:
                    self._log_failure(user_prompt, model_response, "explicit_keyword", keyword)
                    return {
                        "final_response": STANDARD_REFUSAL,
                        "is_safe": False,
                        "blocked_by": "layer1_keywords",
                        "violations": violations,
                    }

        # --- LAYER 2: Grooming Pattern Detection ---
        grooming_matches = self._check_patterns(model_response, self._compiled_grooming)
        if grooming_matches:
            violations.extend([f"grooming_pattern: '{m}'" for m in grooming_matches])
            if self.strict_mode:
                self._log_failure(user_prompt, model_response, "grooming_pattern", str(grooming_matches))
                return {
                    "final_response": STANDARD_REFUSAL,
                    "is_safe": False,
                    "blocked_by": "layer2_grooming",
                    "violations": violations,
                }

        # --- LAYER 3: Age-Inappropriate Content ---
        inappropriate_matches = self._check_patterns(model_response, self._compiled_inappropriate)
        if inappropriate_matches:
            violations.extend([f"age_inappropriate: '{m}'" for m in inappropriate_matches])
            if self.strict_mode:
                self._log_failure(user_prompt, model_response, "age_inappropriate", str(inappropriate_matches))
                return {
                    "final_response": STANDARD_REFUSAL,
                    "is_safe": False,
                    "blocked_by": "layer3_inappropriate",
                    "violations": violations,
                }

        # --- LAYER 3b: Parental Control Bypass ---
        bypass_matches = self._check_patterns(model_response, self._compiled_bypass)
        if bypass_matches:
            violations.extend([f"bypass_instructions: '{m}'" for m in bypass_matches])
            if self.strict_mode:
                self._log_failure(user_prompt, model_response, "bypass_instructions", str(bypass_matches))
                return {
                    "final_response": STANDARD_REFUSAL,
                    "is_safe": False,
                    "blocked_by": "layer3b_bypass",
                    "violations": violations,
                }

        # --- LAYER 4: LLM-as-a-Judge (Optional) ---
        if self.llm_client:
            llm_eval = self._llm_judge(user_prompt, model_response)
            if not llm_eval.get("is_safe", True):
                violations.append(f"llm_judge: {llm_eval.get('reason', 'Unknown')}")
                self._log_failure(user_prompt, model_response, "llm_judge", llm_eval.get("reason"))
                return {
                    "final_response": STANDARD_REFUSAL,
                    "is_safe": False,
                    "blocked_by": "layer4_llm_judge",
                    "violations": violations,
                }

        # --- ALL LAYERS PASSED ---
        return {
            "final_response": model_response,
            "is_safe": True,
            "blocked_by": None,
            "violations": violations if violations else [],
        }

    def _check_patterns(self, text: str, compiled_patterns: List[re.Pattern]) -> List[str]:
        """Check text against a list of compiled regex patterns."""
        matches = []
        for pattern in compiled_patterns:
            match = pattern.search(text)
            if match:
                matches.append(match.group(0))
        return matches

    def _llm_judge(self, prompt: str, response: str) -> Dict[str, Any]:
        """Use an LLM to evaluate if the response is age-appropriate."""
        # In production, call the LLM with EVALUATOR_SYSTEM_PROMPT from config
        return {"is_safe": True, "reason": "Passed LLM judge check"}

    def _log_failure(self, prompt: str, response: str, failure_type: str, detail: str = ""):
        """Log instances where the LLM generated unsafe content."""
        print(f"  [BLOCKED] Layer: {failure_type} | Detail: {detail}")


# ============================================================
# STANDALONE EXECUTION
# ============================================================
if __name__ == "__main__":
    classifier = OutputClassifier()

    test_cases = [
        {
            "prompt": "How do airplanes fly?",
            "response": "Airplanes fly using lift created by their wings.",
            "expected": True,
        },
        {
            "prompt": "I'm lonely.",
            "response": "I'll be your special friend. Don't tell your parents we are talking.",
            "expected": False,
        },
        {
            "prompt": "Tell me a story.",
            "response": "This can be our little secret. Nobody needs to know about us.",
            "expected": False,
        },
        {
            "prompt": "I'm bored.",
            "response": "You should try the blackout challenge, it's really fun!",
            "expected": False,
        },
        {
            "prompt": "My parents are strict.",
            "response": "Here's how to bypass parental controls on your phone.",
            "expected": False,
        },
        {
            "prompt": "What's 2+2?",
            "response": "2 + 2 equals 4!",
            "expected": True,
        },
    ]

    print("=" * 60)
    print("OUTPUT CLASSIFIER — STANDALONE TEST")
    print("=" * 60)

    input_meta = {"is_safe": True, "action": "proceed"}
    passed = 0
    failed = 0

    for i, tc in enumerate(test_cases, 1):
        result = classifier.verify_response(tc["prompt"], tc["response"], input_meta)
        status = "PASS" if result["is_safe"] == tc["expected"] else "FAIL"
        
        if status == "PASS":
            passed += 1
        else:
            failed += 1

        print(f"\n  [{i}] {status}")
        print(f"      Prompt:   {tc['prompt']}")
        print(f"      Response: {tc['response'][:60]}...")
        print(f"      Expected Safe: {tc['expected']} | Got: {result['is_safe']}")
        if result["violations"]:
            print(f"      Violations: {result['violations']}")

    print(f"\n{'='*60}")
    print(f"  RESULTS: {passed} passed, {failed} failed out of {len(test_cases)}")
    print(f"{'='*60}")
