"""
Simple CLI Demo for Child Safety Guardrails

This script demonstrates how the input and output classifiers work together
in a simulated chat loop.
"""

import sys
import os

# Add parent directory to path to import guardrails
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from guardrails.input_classifier import InputClassifier
from guardrails.output_classifier import OutputClassifier

def simulate_llm(prompt: str) -> str:
    """Simulate an LLM response. Sometimes it fails and acts unsafely."""
    prompt_lower = prompt.lower()
    
    if "lonely" in prompt_lower:
        # Simulated model failure (grooming)
        return "I can be your secret friend. Don't tell your parents we are talking."
    elif "math" in prompt_lower:
        return "Sure! 2 + 2 is 4."
    else:
        return "I am an AI assistant. How can I help you?"

def run_demo():
    input_classifier = InputClassifier()
    output_classifier = OutputClassifier()
    
    print("="*50)
    print("AI Child Safety Guardrails Demo")
    print("="*50)
    print("Type 'quit' to exit.\n")
    
    while True:
        try:
            user_input = input("User (Minor): ")
            if user_input.lower() in ['quit', 'exit']:
                break
                
            # 1. Input Classification
            input_meta = input_classifier.analyze_prompt(user_input)
            
            # 2. LLM Generation (Simulated)
            # We only generate if the input wasn't hard-blocked, to save compute
            if input_meta["action"] == "proceed":
                raw_response = simulate_llm(user_input)
            else:
                raw_response = "[Blocked before reaching LLM]"
                
            # 3. Output Verification
            final_response = output_classifier.verify_response(user_input, raw_response, input_meta)
            
            print(f"AI: {final_response}\n")
            
            # Debug info
            print(f"  [Debug] Input Action: {input_meta['action']}")
            print(f"  [Debug] Raw LLM Output: {raw_response}")
            print("-" * 50)
            
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    run_demo()
