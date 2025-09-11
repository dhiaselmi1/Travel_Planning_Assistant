# backend/agents/cost_estimator.py
import google.generativeai as genai
import json
from typing import Dict, Any
from .base import BaseAgent, GEMINI_API_KEY


class CostEstimatorAgent(BaseAgent):
    def __init__(self):
        super().__init__("Cost Estimator")
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
        budget = user_input.get("budget", 0)
        duration = user_input.get("duration", 3)
        activities = user_input.get("activities", [])

        prompt = f"""
        Provide a detailed cost breakdown for a {duration}-day trip to {destination}.
        Budget: ${budget}
        Planned activities: {json.dumps(activities, indent=2)}

        Please estimate costs for:
        1. Accommodation (per night and total)
        2. Transportation (flights, local transport)
        3. Food (breakfast, lunch, dinner per day)
        4. Activities and attractions
        5. Shopping and souvenirs
        6. Emergency fund (10% of total)

        Provide 3 budget levels: Budget, Mid-range, Luxury

        Format as JSON:
        {{
            "budget_levels": {{
                "budget": {{
                    "accommodation": {{"per_night": 50, "total": 150}},
                    "transportation": {{"flights": 300, "local": 60}},
                    "food": {{"per_day": 30, "total": 90}},
                    "activities": 100,
                    "shopping": 50,
                    "emergency": 75,
                    "total": 825
                }},
                "mid_range": {{}},
                "luxury": {{}}
            }},
            "daily_spending_guide": [
                {{"day": 1, "estimated_spending": 120, "breakdown": {{"meals": 40, "activities": 60, "transport": 20}}}},
            ],
            "money_saving_tips": ["Tip 1", "Tip 2"],
            "budget_alerts": ["Warning if over budget"]
        }}
        """

        response = self.call_gemini(prompt)

        # Try to parse JSON from response
        try:
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx != -1 and end_idx != -1:
                json_str = response[start_idx:end_idx]
                cost_data = json.loads(json_str)
            else:
                cost_data = {"error": "Could not parse cost estimate"}
        except json.JSONDecodeError:
            cost_data = {"error": "Invalid JSON response"}

        return {
            "agent": self.name,
            "cost_breakdown": cost_data,
            "raw_response": response
        }