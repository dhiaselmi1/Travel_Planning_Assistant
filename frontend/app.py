# frontend/app.py
import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Configuration
API_BASE_URL = "http://localhost:8000"
st.set_page_config(
    page_title="✈️ Travel Planning Assistant",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .agent-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    .timeline-item {
        background: #f8f9fa;
        border-left: 4px solid #007bff;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 5px 5px 0;
    }
</style>
""", unsafe_allow_html=True)


def call_api(endpoint, data=None, method="GET"):
    """Helper function to call API"""
    url = f"{API_BASE_URL}{endpoint}"
    try:
        if method == "POST":
            response = requests.post(url, json=data)
        else:
            response = requests.get(url)

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None


def main():
    # Header
    st.markdown('<h1 class="main-header">✈️ Travel Planning Assistant</h1>', unsafe_allow_html=True)
    st.markdown("Plan your perfect trip with AI-powered agents!")

    # Sidebar for input
    with st.sidebar:
        st.header("🎯 Trip Details")

        destination = st.text_input("📍 Destination", placeholder="e.g., Paris, France")

        col1, col2 = st.columns(2)
        with col1:
            budget = st.number_input("💰 Budget ($)", min_value=0, value=1000, step=100)
        with col2:
            duration = st.number_input("📅 Duration (days)", min_value=1, max_value=30, value=3)

        st.subheader("🎨 Interests")
        interests = st.multiselect(
            "Select your interests:",
            ["Culture", "History", "Food", "Nature", "Adventure", "Shopping",
             "Architecture", "Museums", "Nightlife", "Beach", "Art", "Photography"],
            default=["Culture", "Food"]
        )

        # Agent selection
        st.subheader("🤖 Choose Agents")
        agent_choice = st.selectbox(
            "Select agent(s):",
            ["All Agents", "Itinerary Builder", "Cost Estimator", "Local Culture Coach"]
        )

        agent_map = {
            "All Agents": "all",
            "Itinerary Builder": "itinerary",
            "Cost Estimator": "cost",
            "Local Culture Coach": "culture"
        }

        plan_button = st.button("🚀 Plan My Trip!", type="primary")

        st.divider()

        # Memory management
        st.subheader("💾 Memory")
        if st.button("📚 View History"):
            st.session_state.show_history = True
        if st.button("🗑️ Clear Memory"):
            response = call_api("/memory/clear", method="POST")
            if response and response.get("success"):
                st.success("Memory cleared!")

    # Main content area
    if plan_button and destination and interests:
        with st.spinner("🔍 Planning your amazing trip..."):
            # Prepare request data
            request_data = {
                "destination": destination,
                "budget": budget,
                "interests": interests,
                "duration": duration,
                "agent": agent_map[agent_choice]
            }

            # Call API
            response = call_api("/plan-trip", request_data, "POST")

            if response and response.get("success"):
                st.success("🎉 Trip planned successfully!")
                results = response.get("results", {})

                # Create tabs for different agents
                if agent_choice == "All Agents":
                    tab1, tab2, tab3 = st.tabs(["📋 Itinerary", "💰 Cost Breakdown", "🏛️ Cultural Guide"])

                    with tab1:
                        display_itinerary(results.get("itinerary", {}))

                    with tab2:
                        display_cost_breakdown(results.get("cost_estimate", {}))

                    with tab3:
                        display_cultural_guide(results.get("cultural_guide", {}))
                else:
                    # Single agent result
                    if agent_choice == "Itinerary Builder":
                        display_itinerary(results)
                    elif agent_choice == "Cost Estimator":
                        display_cost_breakdown(results)
                    elif agent_choice == "Local Culture Coach":
                        display_cultural_guide(results)

    # Show history if requested
    if st.session_state.get("show_history", False):
        display_travel_history()


def display_itinerary(itinerary_data):
    """Display itinerary results"""
    st.subheader("📋 Your Personalized Itinerary")

    if "error" in itinerary_data.get("itinerary", {}):
        st.error("Could not generate itinerary. Please try again.")
        return

    itinerary = itinerary_data.get("itinerary", {})
    days = itinerary.get("days", [])

    if not days:
        st.warning("No itinerary data available")
        return

    # Timeline view
    for day_data in days:
        day_num = day_data.get("day", 1)
        activities = day_data.get("activities", [])

        st.markdown(f"### 📅 Day {day_num}")

        for activity in activities:
            with st.container():
                col1, col2, col3 = st.columns([2, 2, 1])

                with col1:
                    st.markdown(f"**🕐 {activity.get('time', 'TBD')}**")
                    st.markdown(f"📍 {activity.get('location', 'Location TBD')}")

                with col2:
                    st.markdown(f"**{activity.get('activity', 'Activity')}**")
                    st.markdown(activity.get('description', ''))

                with col3:
                    st.markdown(f"⏱️ {activity.get('duration', 'TBD')}")
                    st.markdown(f"💰 {activity.get('cost_estimate', '$0')}")

                st.divider()


def display_cost_breakdown(cost_data):
    """Display cost breakdown"""
    st.subheader("💰 Cost Breakdown & Budget Planning")

    cost_breakdown = cost_data.get("cost_breakdown", {})

    if "error" in cost_breakdown:
        st.error("Could not generate cost estimate. Please try again.")
        return

    budget_levels = cost_breakdown.get("budget_levels", {})

    if budget_levels:
        # Budget comparison chart
        budget_names = list(budget_levels.keys())
        budget_totals = [budget_levels[level].get("total", 0) for level in budget_names]

        fig = px.bar(
            x=budget_names,
            y=budget_totals,
            title="Budget Options Comparison",
            labels={"x": "Budget Level", "y": "Total Cost ($)"},
            color=budget_totals,
            color_continuous_scale="viridis"
        )
        st.plotly_chart(fig, use_container_width=True)

        # Detailed breakdown
        for level_name, level_data in budget_levels.items():
            with st.expander(f"💳 {level_name.title()} Budget Details"):
                col1, col2 = st.columns(2)

                with col1:
                    for category, amount in level_data.items():
                        if category != "total":
                            if isinstance(amount, dict):
                                st.metric(f"{category.title()}", f"${amount.get('total', 0)}")
                            else:
                                st.metric(f"{category.title()}", f"${amount}")

                with col2:
                    st.metric("Total Budget", f"${level_data.get('total', 0)}", delta=None)

    # Money saving tips
    tips = cost_breakdown.get("money_saving_tips", [])
    if tips:
        st.subheader("💡 Money Saving Tips")
        for tip in tips:
            st.info(tip)


def display_cultural_guide(culture_data):
    """Display cultural guide"""
    st.subheader("🏛️ Cultural Guide & Local Insights")

    cultural_guide = culture_data.get("cultural_guide", {})

    if "error" in cultural_guide:
        st.error("Could not generate cultural guide. Please try again.")
        return

    # Cultural etiquette
    etiquette = cultural_guide.get("cultural_etiquette", [])
    if etiquette:
        st.subheader("🤝 Cultural Etiquette")
        for item in etiquette:
            importance = item.get("importance", "medium")
            color = "🔴" if importance == "high" else "🟡" if importance == "medium" else "🟢"
            st.markdown(f"{color} **{item.get('category', 'General')}**: {item.get('tip', '')}")

    # Language basics
    language = cultural_guide.get("language_basics", {})
    if language:
        st.subheader("🗣️ Essential Phrases")
        phrases = language.get("essential_phrases", [])
        if phrases:
            phrase_df = pd.DataFrame(phrases)
            st.dataframe(phrase_df, use_container_width=True)

    # Food culture
    food = cultural_guide.get("food_culture", {})
    if food:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🍽️ Must-Try Foods")
            must_try = food.get("must_try", [])
            for food_item in must_try:
                st.markdown(f"• {food_item}")

        with col2:
            st.subheader("🍴 Dining Etiquette")
            etiquette = food.get("dining_etiquette", [])
            for rule in etiquette:
                st.markdown(f"• {rule}")

    # Hidden gems
    gems = cultural_guide.get("hidden_gems", [])
    if gems:
        st.subheader("💎 Hidden Gems")
        for gem in gems:
            st.markdown(f"**{gem.get('name', 'Unknown')}** ({gem.get('type', 'attraction')})")
            st.markdown(f"💡 {gem.get('tip', '')}")

    # Cultural warnings
    warnings = cultural_guide.get("cultural_warnings", [])
    if warnings:
        st.subheader("⚠️ Important Cultural Notes")
        for warning in warnings:
            st.warning(warning)


def display_travel_history():
    """Display travel history from memory"""
    st.header("📚 Travel History")

    memory_data = call_api("/memory")
    if memory_data:
        trips = memory_data.get("trips", [])

        if trips:
            for i, trip in enumerate(trips):
                with st.expander(
                        f"Trip {i + 1}: {trip.get('destination', 'Unknown')} - {trip.get('created_at', '')[:10]}"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Destination", trip.get('destination', 'N/A'))
                    with col2:
                        st.metric("Budget", f"${trip.get('budget', 0)}")
                    with col3:
                        st.metric("Duration", f"{trip.get('duration', 0)} days")

                    st.markdown("**Interests:** " + ", ".join(trip.get('interests', [])))
        else:
            st.info("No trip history found. Start planning your first trip!")


if __name__ == "__main__":
    main()
