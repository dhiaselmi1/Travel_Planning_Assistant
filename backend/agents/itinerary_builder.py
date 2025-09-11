# backend/agents/itinerary_builder.py
import google.generativeai as genai
import json
from typing import Dict, Any, List
from .base import BaseAgent, GEMINI_API_KEY
from datetime import datetime


class ItineraryBuilderAgent(BaseAgent):
    def __init__(self):
        super().__init__("Itinerary Builder")
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
        interests = user_input.get("interests", [])
        duration = user_input.get("duration", 3)

        # Load previous preferences from memory
        memory = self.load_memory()
        previous_trips = memory.get("trips", [])
        preferences = memory.get("preferences", {})

        prompt = f"""
        Create a detailed {duration}-day itinerary for {destination}.
        Budget: ${budget}
        Interests: {', '.join(interests)}

        Previous travel preferences: {json.dumps(preferences, indent=2)}

        Please provide:
        1. Daily schedule with activities
        2. Time slots for each activity
        3. Transportation suggestions
        4. Must-see attractions based on interests
        5. Free/budget-friendly alternatives

        Format as JSON with this structure:
        {{
            "days": [
                {{
                    "day": 1,
                    "activities": [
                        {{
                            "time": "09:00",
                            "activity": "Activity name",
                            "location": "Location",
                            "duration": "2 hours",
                            "cost_estimate": "$20",
                            "description": "Brief description"
                        }}
                    ]
                }}
            ]
        }}
        """

        response = self.call_gemini(prompt)

        # Try to parse JSON from response
        try:
            # Extract JSON from response if it contains other text
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx != -1 and end_idx != -1:
                json_str = response[start_idx:end_idx]
                itinerary_data = json.loads(json_str)
            else:
                # Fallback if JSON parsing fails
                itinerary_data = {"days": [], "error": "Could not parse itinerary"}
        except json.JSONDecodeError:
            itinerary_data = {"days": [], "error": "Invalid JSON response"}

        # Save to memory
        trip_data = {
            "destination": destination,
            "budget": budget,
            "interests": interests,
            "duration": duration,
            "itinerary": itinerary_data,
            "created_at": str(datetime.now())
        }
        self.add_to_memory("trips", trip_data)

        return {
            "agent": self.name,
            "itinerary": itinerary_data,
            "raw_response": response
        }