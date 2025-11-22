import streamlit as st
import openai
from dotenv import load_dotenv
import os
import googlemaps
from datetime import datetime
import json

# Load environment variables
load_dotenv()

# Initialize API clients
openai.api_key = os.getenv("OPENAI_API_KEY")
gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Set page config
st.set_page_config(
    page_title="AI Travel Companion",
    page_icon="✈️",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .assistant-message {
        background-color: #f5f5f5;
    }
    </style>
""", unsafe_allow_html=True)

def get_travel_recommendations(location, preferences):
    """Get travel recommendations using Google Places API"""
    try:
        # Search for places
        places_result = gmaps.places_nearby(
            location=location,
            radius=5000,
            type=['tourist_attraction', 'restaurant', 'hotel']
        )
        
        # Get gas stations
        gas_stations = gmaps.places_nearby(
            location=location,
            radius=5000,
            type=['gas_station']
        )
        
        return {
            'attractions': places_result.get('results', []),
            'gas_stations': gas_stations.get('results', [])
        }
    except Exception as e:
        return {'error': str(e)}

def get_route(start_location, end_location):
    """Get route information using Google Directions API"""
    try:
        directions_result = gmaps.directions(
            start_location,
            end_location,
            mode="driving",
            departure_time=datetime.now()
        )
        return directions_result[0] if directions_result else None
    except Exception as e:
        return {'error': str(e)}

def process_user_input(user_input):
    """Process user input and generate appropriate response"""
    try:
        # Create a prompt for the AI
        prompt = f"""As an AI Travel Companion, help the user with their travel needs. 
        User input: {user_input}
        Provide helpful, concise responses focusing on:
        1. Route planning
        2. Attraction suggestions
        3. Gas station locations
        4. General travel advice
        """
        
        # Get AI response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI Travel Companion."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"I apologize, but I encountered an error: {str(e)}"

# Main UI
st.title("✈️ AI Travel Companion")
st.markdown("""
    Welcome to your AI Travel Companion! I can help you with:
    - Planning travel routes
    - Suggesting attractions
    - Finding gas stations
    - Providing travel recommendations
""")

# Chat interface
for message in st.session_state.messages:
    with st.container():
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user-message">👤 You: {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message assistant-message">🤖 Assistant: {message["content"]}</div>', unsafe_allow_html=True)

# User input
user_input = st.text_input("Ask me anything about your travel plans:", key="user_input")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Process user input and get response
    response = process_user_input(user_input)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Rerun to update the chat display
    st.rerun()

# Sidebar with additional features
with st.sidebar:
    st.header("Additional Features")
    st.markdown("""
        - Route Planning
        - Attraction Search
        - Gas Station Finder
        - Travel Tips
    """)
    
    # Example route planning form
    st.subheader("Plan a Route")
    start = st.text_input("Starting Location")
    end = st.text_input("Destination")
    
    if start and end:
        if st.button("Get Route"):
            route = get_route(start, end)
            if route and 'error' not in route:
                st.success("Route found!")
                st.json(route)
            else:
                st.error("Could not find route. Please try again.") 