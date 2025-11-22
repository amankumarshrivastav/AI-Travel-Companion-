# AI Travel Companion

An intelligent chatbot that helps you plan your travel routes, suggests attractions, and finds gas stations along your journey.

## Features

- Route planning and optimization
- Attraction suggestions based on location and preferences
- Gas station finder along routes
- Interactive chat interface
- Real-time travel recommendations

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   GOOGLE_MAPS_API_KEY=your_google_maps_api_key
   ```
4. Run the application:
   ```
   streamlit run app.py
   ```

## Required API Keys

- OpenAI API Key: For the chatbot functionality
- Google Maps API Key: For maps, places, and directions services

## Usage

1. Start the application
2. Enter your travel preferences and requirements
3. Chat with the AI to get personalized travel recommendations
4. Get detailed route information, attraction suggestions, and gas station locations 