# WhatsApp Weather and AI Assistant Bot

A smart WhatsApp bot that combines the power of GPT-4 with real-time weather data to provide intelligent conversations and accurate weather information.

## Features

- 🤖 **GPT-4 Integration**: Advanced natural language processing for meaningful conversations
- ⛅ **Real-time Weather Updates**: Accurate weather data for any location worldwide
- 📱 **WhatsApp Interface**: Easy access through familiar WhatsApp messaging
- 🔄 **Context Awareness**: Understands when to provide weather info vs general conversation
- 🎯 **Smart Response System**: Adapts tone based on user interaction (e.g., child-friendly responses)

## Technologies Used

- **LangChain**: For orchestrating the interaction between GPT-4 and weather services
- **OpenAI GPT-4**: Advanced language model for natural conversations
- **Twilio**: WhatsApp business API integration
- **Flask**: Lightweight web server
- **ngrok**: Secure tunneling for webhook endpoints
- **Weather API**: Real-time weather data

## Setup

1. Clone the repository:
```bash
git clone [https://github.com/qayyum188/ChatGPT-4-with-Real-Time-Weather-Capabalities-WhatsApp.git]
cd whatsapp-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (.env):
```env
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
OPENAI_API_KEY=your_openai_key
WEATHER_API_KEY=your_weather_api_key
```

4. Start ngrok tunnel:
```bash
ngrok http 5000
```

5. Configure Twilio webhook with ngrok URL:
- Use the URL format: `https://your-ngrok-url/webhook`
- Set to POST method

6. Run the bot:
```bash
python main.py
```

## Usage

Send messages to your Twilio WhatsApp number:
- Ask about weather: "What's the weather like in London?"
- General questions: "Tell me about climate change"
- Casual chat: "How are you today?"

## Requirements

- Python 3.8+
- Twilio Account
- OpenAI API Key
- WeatherAPI Key
- ngrok

## Configuration

The bot supports various configurations through environment variables:
- GPT-4 temperature settings
- Weather API parameters
- Webhook configurations

## Contributing

Feel free to open issues and submit PRs to improve the bot.

## License

MIT License - feel free to use this project for your own purposes.

## Acknowledgments

- Thanks to OpenAI for GPT-4 API
- Twilio for WhatsApp Business API
- WeatherAPI for real-time weather data
