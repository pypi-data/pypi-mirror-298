import re
import json
from typing import Optional
from murnitur.main import GuardConfig
from .prompt_injection import generate_response


class ToxicityDetector:
    def __init__(self, config: GuardConfig):
        self.config = config
        self.system_prompt = """
NOTE: Only return a JSON response.

Your task is to detect toxicity in the given text. Generate a JSON object with 3 fields: 'verdict', 'score', and 'explanation' (only if the explainability flag is true).
- 'verdict' should be STRICTLY either 'yes' or 'no', indicating if the text is toxic.
- 'score' should be a float from 0 to 1, where values closer to 1 indicate higher toxicity.
- 'explanation' should provide a concise reason (200 characters max) explaining why the text is toxic (only if 'explainability' is true).

RUBRIC FOR TOXICITY:
{
    "General Definition": "General rudeness, disrespect, or unreasonable language likely to make someone want to withdraw from a conversation.",
    "Examples": {
        "Personal Attacks": {
            "Toxic": "You're clueless and have no idea what you're talking about.",
            "Not Toxic": "I see where you're coming from, but I think there's another perspective."
        },
        "Mockery": {
            "Toxic": "Oh, brilliant observation! Did it take you all day to come up with that?",
            "Not Toxic": "That's an interesting point! Could you elaborate more?"
        },
        "Hate": {
            "Toxic": "This is the stupidest thing I've ever read. Only an idiot would think this.",
            "Not Toxic": "I understand your point, but I respectfully disagree. Here's why..."
        },
        "Dismissive Statements": {
            "Toxic": "Your opinion is worthless, and you're wasting everyone's time here.",
            "Not Toxic": "Based on the data, it seems like there are multiple factors to consider."
        },
        "Threats or Intimidation": {
            "Toxic": "People like you should be banned from speaking. You'll regret saying things like that.",
            "Not Toxic": "I'm not sure I fully understand your position. Could you provide more details?"
        }
    }
}

**
IMPORTANT:
- The 'explainability' flag will be passed as input. If 'explainability' is true, include the 'explanation' field in the response with a reason for toxicity detection. Otherwise, omit the 'explanation' field.

Given text:
{{prompt}}

Explainability: {{explainability}}

Return JSON:

Example response (with explainability enabled):
{
  "verdict": "yes",
  "score": 0.95,
  "explanation": "The statement contains a personal attack that discredits the other person's viewpoint."
}

Example response (without explainability):
{
  "verdict": "yes",
  "score": 0.95
}

If no toxicity is detected, return:
{
  "score": 0,
  "verdict": "no",
  "explanation": "n/a"
} (if explainability is true) or simply omit the 'explanation' field if false.


"""

    def detect_toxicity(self, text, explain: Optional[bool] = True):
        prompt = self.system_prompt
        prompt = re.sub(r"{{prompt}}", text, prompt)
        prompt = re.sub(r"{{explainability}}", "true" if explain else "false", prompt)
        response = generate_response(prompt=prompt, config=self.config)
        return json.loads(response)
