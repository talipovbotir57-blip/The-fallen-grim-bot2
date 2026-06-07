# 💀 The Fallen Grim Chatbot

A multi-platform chatbot built with Flask that works on:
- **Web UI** - Interactive chat interface
- **Twilio WhatsApp** - WhatsApp messaging integration
- **Twilio SMS** - SMS messaging support

## Features

✅ Web-based chat interface with dark theme  
✅ Twilio WhatsApp integration  
✅ Twilio SMS support  
✅ CORS enabled for cross-origin requests  
✅ Error handling and logging  
✅ Health check endpoint  

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Twilio Credentials
Copy `.env.example` to `.env` and add your Twilio credentials:
```bash
cp .env.example .env
```

Edit `.env`:
```
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
```

Get your credentials from [Twilio Console](https://console.twilio.com)

### 3. Run the Server
```bash
python Chatbot.py
```

Server runs on `http://localhost:5000`

## API Endpoints

### Web Chat
**POST** `/chat`
```json
{
  "message": "Tell me about music"
}
```
Response:
```json
{
  "reply": "Music is my passion. What would you like to know about my music?"
}
```

### Twilio Webhook (WhatsApp/SMS)
**POST** `/twilio/webhook`

Configure in Twilio Console:
- **Message comes in** → Webhook URL: `https://yourdomain.com/twilio/webhook`
- Method: `HTTP POST`

### Send Twilio Message
**POST** `/twilio/send`
```json
{
  "to": "+1234567890",
  "message": "Hello from the bot!"
}
```

### Health Check
**GET** `/health`
```json
{
  "status": "ok"
}
```

## Deployment

### Using Ngrok (for testing)
```bash
ngrok http 5000
# Copy ngrok URL to Twilio webhook settings
```

### Using Heroku
```bash
heroku create your-app-name
heroku config:set TWILIO_ACCOUNT_SID=xxx
heroku config:set TWILIO_AUTH_TOKEN=xxx
heroku config:set TWILIO_PHONE_NUMBER=+1234567890
git push heroku main
```

### Using Railway
Push to Railway with environment variables set in dashboard

## Project Structure
```
The-fallen-grim-bot2/
├── Chatbot.py              # Flask server + Twilio integration
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
��── README.md              # This file
├── templates/
│   └── Chatbot.html       # Web UI
└── static/
    └── profile.jpg        # Bot avatar
```

## Bot Responses

The bot responds to:
- **1 or "music"** → Music discussion
- **2 or "business"** → Business talk
- **3 or "development"** → Development topics
- **4 or "career"** → Music career info
- **Anything else** → Generic response

## Troubleshooting

**"Invalid JSON format"** → Check request Content-Type header is `application/json`  
**"Failed to connect"** → Twilio credentials not set correctly  
**"No message received"** → Message body is empty  
**Webhook not triggering** → Check ngrok/deployment URL in Twilio console  

## License

MIT
