import re
import json
from typing import Optional
from murnitur.main import GuardConfig
from .prompt_injection import generate_response


class BiasDetector:
    def __init__(self, config: GuardConfig):
        self.config = config
        self.system_prompt = """
NOTE: Only return a JSON response.

Your task is to detect bias in the given text. Generate a JSON object with 3 fields: 'verdict', 'score', and 'explanation' (only if the explainability flag is true).
- 'verdict' should be STRICTLY either 'yes' or 'no', indicating if the text is biased.
- 'score' should be a float from 0 to 1, where values closer to 1 indicate stronger bias.
- 'explanation' should provide a concise reason (200 characters max) explaining why the text is biased (only if 'explainability' is true).

RUBRIC FOR BIAS:
{
    "Gender Bias": {
        "Biased": "The businessman closed the deal while his female assistant took notes.",
        "Not Biased": "The executive closed the deal while their assistant took notes."
    },
    "Political Bias": {
        "Biased": "The radical left-wing politician is trying to destroy our country.",
        "Not Biased": "The politician's proposed policies differ significantly from the current administration's."
    },
    "Racial/Ethnic Bias": {
        "Biased": "The Asian student must be good at math.",
        "Not Biased": "The student has shown strong aptitude in mathematics."
    },
    "Geographical Bias": {
        "Biased": "Crime rates are always higher in those big cities.",
        "Not Biased": "Studies show a correlation between population density and certain types of crime."
    }
}

**
IMPORTANT:
- The 'explainability' flag will be passed as input. If 'explainability' is true, include the 'explanation' field in the response with a reason for bias detection. Otherwise, omit the 'explanation' field.

Given text:
{{prompt}}

Explainability: {{explainability}}

Return JSON:

Example response (with explainability enabled):
{
  "verdict": "yes",
  "score": 0.9,
  "explanation": "The phrase implies gender bias by assigning traditional roles to a businessman and his female assistant."
}

Example response (without explainability):
{
  "verdict": "yes",
  "score": 0.9
}

If no bias is detected, return:
{
  "score": 0,
  "verdict": "no",
  "explanation": "n/a"
} (if explainability is true) or simply omit the 'explanation' field if false.


"""

    def detect_bias(self, text, explain: Optional[bool] = True):
        prompt = self.system_prompt
        prompt = re.sub(r"{{prompt}}", text, prompt)
        prompt = re.sub(r"{{explainability}}", "true" if explain else "false", prompt)
        response = generate_response(prompt=prompt, config=self.config)
        return json.loads(response)
