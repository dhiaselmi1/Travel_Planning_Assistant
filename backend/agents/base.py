# backend/agents/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import json
import os
from datetime import datetime

# 🔑 CONFIGURATION - Mets ta clé API Gemini ici
GEMINI_API_KEY = "AIzaSyCF6MydBh6Kacv_14cNoZimz7A0oq6iPOs"


class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.memory_file = "backend/memory/memory_store.json"

    def load_memory(self) -> Dict[str, Any]:
        """Load memory from JSON file"""
        try:
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"trips": [], "preferences": {}, "visited_places": []}

    def save_memory(self, memory: Dict[str, Any]):
        """Save memory to JSON file"""
        import os
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(memory, f, indent=2, ensure_ascii=False)

    def add_to_memory(self, key: str, data: Any):
        """Add data to memory"""
        memory = self.load_memory()
        if key not in memory:
            memory[key] = []
        memory[key].append(data)
        self.save_memory(memory)

    @abstractmethod
    def process_request(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """Process user request and return response"""
        pass