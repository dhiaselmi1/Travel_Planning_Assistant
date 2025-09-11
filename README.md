# 🧳✨ Travel Planning Assistant ✨🧭

A collaborative 🤖 AI-powered travel planning application built with ⚡ FastAPI, 🎨 Streamlit, and 🌌 Gemini Flash 2.0 via 🐪 Ollama.

## 🌟 Features

### 🤖 AI Agents
- 🗓️ **Itinerary Builder**: Creates detailed day-by-day travel itineraries
- 💰 **Cost Estimator**: Provides budget breakdowns and cost estimates
- 🏛️ **Local Culture Coach**: Offers cultural insights and local tips

### ✨ Key Capabilities
- 🤝 Multi-agent collaboration for comprehensive trip planning
- 🧠 Memory system to store preferences and trip history
- 📅 Interactive timeline view of daily plans
- 📊 Budget comparison across different spending levels
- 🌍 Cultural etiquette and local insights
- 🔌 RESTful API with FastAPI backend
- 💻 Beautiful Streamlit web interface

## ⚙️ Installation & Setup

### 📋 Prerequisites
- 🐍 Python 3.8+
- 🐪 Ollama with Gemini Flash 2.0 model
- 📦 Required Python packages (see requirements below)

### 1️⃣ Install Dependencies
```bash
pip install fastapi uvicorn streamlit requests pydantic plotly pandas
```

### 2️⃣ Setup Ollama
Install and run Ollama, then pull the Gemini Flash 2.0 model:
```bash
ollama pull gemini-flash-2.0
ollama serve
```

### 3️⃣ File Structure
📂 Create the following directory structure:
```
Travel-Planning-Assistant/
├── backend/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── itinerary_builder.py
│   │   ├── cost_estimator.py
│   │   └── local_culture_coach.py
│   ├── memory/
│   │   └── memory_store.json
│   └── main.py
├── frontend/
│   └── app.py
└── README.md
```

### 4️⃣ Create `__init__.py` files
📝 Create empty `__init__.py` files in the agents directory for proper Python module imports.

### 5️⃣ Fix Import Issues
Update the import statements in `backend/main.py`:

```python
from agents.itinerary_builder import ItineraryBuilderAgent
from agents.cost_estimator import CostEstimatorAgent  
from agents.local_culture_coach import LocalCultureCoachAgent
```

## 🚀 Running the Application

### ▶️ Start the Backend API
```bash
cd backend
python main.py
```
The API will be available at 🌐 `http://localhost:8000`

### 💻 Start the Frontend
```bash
cd frontend
streamlit run app.py
```
The web interface will be available at 🌐 `http://localhost:8501`

## 🎯 Usage

### ✈️ Planning a Trip
1. 📝 **Enter Trip Details**: Destination, budget, duration, and interests
2. 🔍 **Select Agents**: Choose to use all agents or specific ones
3. 🪄 **Generate Plan**: Click "Plan My Trip!" to get comprehensive travel advice
4. 👀 **Review Results**: 
   - 🗓️ View detailed itineraries with timeline
   - 📊 Compare budget options with visual charts
   - 🌍 Learn about local culture and etiquette

### 🔎 Features Overview

#### 🗓️ Itinerary Builder
- 📅 Day-by-day activity planning
- ⏰ Time slots and duration estimates
- 📍 Location-based recommendations
- 💵 Cost estimates per activity

#### 💰 Cost Estimator
- 💸 Three budget levels (Budget, Mid-range, Luxury)
- 🧾 Detailed cost breakdowns
- 📆 Daily spending guides
- 💡 Money-saving tips
- 🚨 Budget alerts

#### 🏛️ Local Culture Coach
- 🙏 Cultural etiquette and customs
- 🗣️ Essential language phrases
- 🍲 Local food recommendations
- 👗 Dress codes for different occasions
- 🗺️ Hidden gems and local secrets
- ⚠️ Cultural warnings and taboos

### 🧠 Memory System
- 💾 Automatically saves trip plans and preferences
- 📜 View travel history
- 🧹 Clear memory when needed
- 🤖 Learns from past trips for better recommendations

## 🔌 API Endpoints

- `POST /plan-trip` ✈️ Generate travel plans
- `GET /memory` 📜 Retrieve travel history
- `POST /memory/clear` 🧹 Clear saved memory
- `GET /health` ❤️ Health check

## 🛠️ Configuration

### 🌌 Gemini Flash 2.0 Setup
The application is configured to use Gemini Flash 2.0 via Ollama. Make sure:
1. 🖥️ Ollama is running on `localhost:11434`
2. 🏷️ The model name matches your Ollama setup
3. ⚙️ Adjust the model name in the agents if needed

### 🎨 Customization
You can customize:
- ✍️ AI prompts in each agent file
- 🎨 Streamlit interface styling in `frontend/app.py`
- 🌐 API endpoints and validation in `backend/main.py`
- 💾 Memory storage format in `backend/memory/memory_store.json`

## 🐞 Troubleshooting

### Common Issues
1. ❌ **API Connection Error**: Ensure backend is running on port 8000
2. 🚫 **Gemini API Error**: Check if your API key is valid and has quota remaining
3. 📝 **Memory Issues**: Check if the memory directory exists and is writable
4. 🔄 **Import Errors**: Ensure all `__init__.py` files are created

### 🔧 Debug Mode
Add debug logging to troubleshoot issues:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔮 Future Enhancements
- 🌦️ Real-time weather integration
- 🏨 Hotel and ✈️ flight booking APIs
- 👥 Social trip sharing features
- 📱 Mobile app version
- 🌍 Multi-language support
- 🤝 Collaborative planning for groups

## 🤝 Contributing
Feel free to contribute by:
- ➕ Adding new AI agents
- 🎨 Improving the UI/UX
- 🌟 Adding new features
- 🐛 Bug fixes and optimizations

Enjoy planning your perfect trips! ✈️🌍🎒
