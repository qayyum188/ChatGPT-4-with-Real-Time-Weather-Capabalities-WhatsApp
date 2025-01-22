from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize Twilio client
TWILIO_ACCOUNT_SID = 'enter yours'
TWILIO_AUTH_TOKEN = 'enter yours'
TWILIO_PHONE_NUMBER = 'enter yours'

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Initialize OpenAI chat model
chat_model = ChatOpenAI(
    model_name="gpt-4o",  # Using GPT-4 Turbo
    temperature=0.7,
    api_key=os.getenv('OPENAI_API_KEY')
)

# Initialize Weather API
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
WEATHER_BASE_URL = "http://api.weatherapi.com/v1"

def get_weather(location):
    """Get weather data for a location"""
    try:
        url = f"{WEATHER_BASE_URL}/current.json"
        params = {
            'key': WEATHER_API_KEY,
            'q': location,
            'aqi': 'no'
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        current = data['current']
        return f"Weather in {data['location']['name']}:\n" + \
               f"Temperature: {current['temp_c']}°C\n" + \
               f"Condition: {current['condition']['text']}\n" + \
               f"Humidity: {current['humidity']}%\n" + \
               f"Wind: {current['wind_kph']} km/h"
    except Exception as e:
        print(f"Error getting weather: {e}")
        return "Sorry, I couldn't get the weather information at the moment."

def process_message(message):
    """Process incoming message and generate response"""
    try:
        system_prompt = """You are a helpful assistant who can:
        1. Chat naturally with users
        2. Help with weather-related queries
        3. Answer general questions
        
        If the user asks about weather, respond with: WEATHER_CHECK:{location}
        Otherwise, engage in natural conversation while staying helpful and friendly."""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=message)
        ]
        
        response = chat_model.invoke(messages)
        
        if response.content.startswith("WEATHER_CHECK:"):
            location = response.content.split(":")[1].strip()
            return get_weather(location)
        
        return response.content
        
    except Exception as e:
        print(f"Error processing message: {e}")
        return "I apologize, but I'm having trouble understanding that right now. Could you try again?"

# Root endpoint accepting both GET and POST
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return 'WhatsApp Bot is running!'
    else:
        # Handle POST request similar to webhook
        return webhook()

# Main webhook endpoint
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    """Handle incoming WhatsApp messages"""
    # Print debug information
    print(f"\nReceived {request.method} request")
    print(f"URL: {request.url}")
    print(f"Headers: {dict(request.headers)}")
    print(f"Form Data: {dict(request.form)}")
    print(f"JSON Data: {request.get_json(silent=True)}")
    
    try:
        # Get incoming message
        incoming_msg = request.values.get('Body', '').strip()
        sender = request.values.get('From', '')
        
        print(f"Received message: {incoming_msg} from {sender}")
        
        # Handle verification GET request
        if request.method == 'GET':
            return 'Webhook is working!'
            
        # No message received
        if not incoming_msg:
            resp = MessagingResponse()
            resp.message("Hello! How can I help you today?")
            return str(resp)
        
        # Process message and get response
        response_text = process_message(incoming_msg)
        
        # Create Twilio response
        resp = MessagingResponse()
        resp.message(response_text)
        
        print(f"Sending response: {response_text}")
        return str(resp)
        
    except Exception as e:
        print(f"Error in webhook: {e}")
        resp = MessagingResponse()
        resp.message("Sorry, I encountered an error. Please try again.")
        return str(resp)

if __name__ == '__main__':
    print("Starting Flask server...")
    print("Make sure to configure the Twilio webhook URL to: <your_ngrok_url>/webhook")
    app.run(debug=True, port=5000)
