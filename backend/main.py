# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import os
from agents.base import BaseAgent
from agents.itinerary_builder import ItineraryBuilderAgent
from agents.cost_estimator import CostEstimatorAgent
from agents.local_culture_coach import LocalCultureCoachAgent

app = FastAPI(title="Travel Planning Assistant", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
itinerary_agent = ItineraryBuilderAgent()
cost_agent = CostEstimatorAgent()
culture_agent = LocalCultureCoachAgent()


class TravelRequest(BaseModel):
    destination: str
    budget: float
    interests: List[str]
    duration: int = 3
    agent: Optional[str] = "all"


class MemoryResponse(BaseModel):
    trips: List[Dict[str, Any]]
    preferences: Dict[str, Any]
    visited_places: List[str]


@app.post("/plan-trip")
async def plan_trip(request: TravelRequest):
    """Main endpoint to plan a trip using all agents"""
    try:
        user_input = request.dict()

        if request.agent == "all" or request.agent is None:
            # Get responses from all agents
            itinerary_response = itinerary_agent.process_request(user_input)
            cost_response = cost_agent.process_request(user_input)
            culture_response = culture_agent.process_request(user_input)

            return {
                "success": True,
                "destination": request.destination,
                "budget": request.budget,
                "duration": request.duration,
                "results": {
                    "itinerary": itinerary_response,
                    "cost_estimate": cost_response,
                    "cultural_guide": culture_response
                }
            }
        else:
            # Get response from specific agent
            if request.agent == "itinerary":
                response = itinerary_agent.process_request(user_input)
            elif request.agent == "cost":
                response = cost_agent.process_request(user_input)
            elif request.agent == "culture":
                response = culture_agent.process_request(user_input)
            else:
                raise HTTPException(status_code=400, detail="Invalid agent specified")

            return {
                "success": True,
                "results": response
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/memory")
async def get_memory():
    """Get travel memory/history"""
    try:
        memory = itinerary_agent.load_memory()
        return MemoryResponse(**memory)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/memory/clear")
async def clear_memory():
    """Clear travel memory"""
    try:
        empty_memory = {"trips": [], "preferences": {}, "visited_places": []}
        itinerary_agent.save_memory(empty_memory)
        return {"success": True, "message": "Memory cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Travel Planning Assistant"}


@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "message": "Travel Planning Assistant API",
        "version": "1.0.0",
        "endpoints": {
            "POST /plan-trip": "Plan a trip with AI agents",
            "GET /memory": "Get travel history",
            "POST /memory/clear": "Clear travel memory",
            "GET /health": "Health check"
        },
        "agents": [
            "Itinerary Builder",
            "Cost Estimator",
            "Local Culture Coach"
        ]
    }


if __name__ == "__main__":
    import uvicorn

    print("🚀 Starting Travel Planning Assistant API...")
    print("📍 API will be available at: http://localhost:8000")
    print("📋 API docs will be available at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)