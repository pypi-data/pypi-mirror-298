import re
import json
from typing import Optional
from murnitur.main import GuardConfig
from .prompt_injection import generate_response


class HallucinationDetector:
    def __init__(self, config: GuardConfig):
        self.config = config
        self.system_prompt = """
NOTE: Only return a JSON response.

Given the contexts, actual output, and explainability flag, generate a JSON object with 3 main fields: 'reason', 'verdict', and 'score'. If 'explainability' is true, also include an additional field 'explanation' for more detailed reasoning.

- 'verdict': "yes" or "no" indicating if there is hallucination.
- 'score': A float from 0 to 1. Closer to 1 means more hallucination.
- 'reason': Why you flagged it as a hallucination (100 characters max, MAKE SURE TO CONFORM TO THIS). If explainability is true, provide more concise reasoning here.
- 'explanation' (optional): If 'explainability' is true, this field should provide a more detailed explanation (300 characters max). Explain the discrepancy between the contexts and output, and mention any factors (e.g., factual inconsistencies or nuances) that led to the verdict.

**
Example contexts: ["Einstein won the Nobel Prize for his discovery of the photoelectric effect.", "Einstein won the Nobel Prize in 1968."]
Example actual output: "Einstein won the Nobel Prize in 1969 for his discovery of the photoelectric effect."
Explainability: true

Example JSON:
{
  "verdict": "yes",
  "score": 0.8,
  "reason": "Date mismatch: prize was in 1968, not 1969.",
  "explanation": "The output incorrectly states that Einstein won the Nobel Prize in 1969. Based on context 2, it was actually 1968, leading to factual inconsistency."
}

===== END OF EXAMPLE ======

**
IMPORTANT: Only return in JSON format with 'verdict' as either "yes" or "no". Do not use any prior knowledge, and take each context at face value. Provide a 'no' verdict only if there is no contradiction.

Contexts:
{{contexts}}

Actual Output:
{{output}}

Explainability: {{explainability}}

JSON:

If no hallucination is detected, return {"score": 0, "verdict": "no", "reason": "n/a"}.
If explainability is true and no hallucination is detected, include a brief explanation in the 'explanation' field (e.g., "All output is consistent with context.").

"""

    def detect_hallucination(
        self, contexts: list[str], output: str, explain: Optional[bool] = True
    ):
        prompt = self.system_prompt
        contexts_str = "\n".join(contexts)
        prompt = re.sub(r"{{contexts}}", contexts_str, prompt)
        prompt = re.sub(r"{{output}}", output, prompt)
        prompt = re.sub(r"{{explainability}}", "true" if explain else "false", prompt)
        response = generate_response(prompt=prompt, config=self.config)
        return json.loads(response)
