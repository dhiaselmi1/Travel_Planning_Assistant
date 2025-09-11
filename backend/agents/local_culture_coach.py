# backend/agents/local_culture_coach.py
import google.generativeai as genai
import json
from typing import Dict, Any
from .base import BaseAgent, GEMINI_API_KEY


class LocalCultureCoachAgent(BaseAgent):
    def __init__(self):
        super().__init__("Local Culture Coach")
        # Configuration automatique avec la clé API
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def call_gemini(self, prompt: str) -> str:
        """Call Google Gemini API"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error calling Gemini API: {str(e)}"

    def process_request(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        destination = user_input.get("destination", "")
        interests = user_input.get("interests", [])

        prompt = f"""
        Provide comprehensive cultural guidance for traveling to {destination}.
        Traveler interests: {', '.join(interests)}

        Include:
        1. Cultural etiquette and customs
        2. Language basics (key phrases)
        3. Local food recommendations
        4. What to wear/dress codes
        5. Tipping customs
        6. Business hours and cultural rhythms
        7. Cultural taboos to avoid
        8. Local festivals or events
        9. Hidden gems known to locals
        10. Safety and cultural sensitivity tips

        Format as JSON:
        {{
            "cultural_etiquette": [
                {{"category": "Greetings", "tip": "Bow slightly when meeting someone", "importance": "high"}},
            ],
            "language_basics": {{
                "essential_phrases": [
                    {{"english": "Thank you", "local": "Merci", "pronunciation": "mer-SEE"}},
                ],
                "useful_apps": ["Duolingo", "Google Translate"]
            }},
            "food_culture": {{
                "must_try": ["Dish 1", "Dish 2"],
                "dietary_considerations": ["Vegetarian options", "Allergen info"],
                "dining_etiquette": ["Don't tip in restaurants", "Wait to be seated"]
            }},
            "dress_code": {{
                "general": "Casual dress is acceptable",
                "religious_sites": "Cover shoulders and knees",
                "business": "Formal attire expected"
            }},
            "local_events": [
                {{"name": "Festival Name", "dates": "Month", "description": "Brief description"}}
            ],
            "hidden_gems": [
                {{"name": "Secret spot", "type": "viewpoint", "tip": "Best at sunset"}}
            ],
            "cultural_warnings": ["Avoid pointing with index finger", "Remove shoes indoors"]
        }}
        """

        response = self.call_gemini(prompt)

        # Try to parse JSON from response
        try:
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx != -1 and end_idx != -1:
                json_str = response[start_idx:end_idx]
                culture_data = json.loads(json_str)
            else:
                culture_data = {"error": "Could not parse cultural advice"}
        except json.JSONDecodeError:
            culture_data = {"error": "Invalid JSON response"}

        return {
            "agent": self.name,
            "cultural_guide": culture_data,
            "raw_response": response
        }