from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__, template_folder='templates')
CORS(app)

# Twilio credentials (set these in environment variables)
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', 'your_account_sid')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', 'your_auth_token')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER', 'your_twilio_number')

# Initialize Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route('/')
def index():
    return render_template('Chatbot.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle web chat requests"""
    try:
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({'reply': 'Invalid JSON format'}), 400
        
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'reply': 'No message received'}), 400
        
        bot_reply = generate_response(user_message)
        return jsonify({'reply': bot_reply}), 200
        
    except Exception as error:
        print(f"Web Chat Error: {error}")
        return jsonify({'reply': 'Server error'}), 500

@app.route('/twilio/webhook', methods=['POST'])
def twilio_webhook():
    """Handle Twilio WhatsApp/SMS webhook"""
    try:
        # Get message from Twilio
        incoming_msg = request.form.get('Body', '').strip()
        sender_phone = request.form.get('From', '')
        
        if not incoming_msg:
            resp = MessagingResponse()
            resp.message("No message received")
            return str(resp)
        
        # Generate bot response
        bot_reply = generate_response(incoming_msg)
        
        # Create Twilio response
        resp = MessagingResponse()
        resp.message(bot_reply)
        
        print(f"Twilio message from {sender_phone}: {incoming_msg}")
        
        return str(resp), 200
        
    except Exception as error:
        print(f"Twilio Webhook Error: {error}")
        resp = MessagingResponse()
        resp.message("Failed to connect to bot")
        return str(resp), 500

@app.route('/twilio/send', methods=['POST'])
def twilio_send():
    """Send Twilio message (for outbound messages)"""
    try:
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({'error': 'Invalid JSON format'}), 400
        
        recipient_phone = data.get('to', '')
        message_body = data.get('message', '').strip()
        
        if not recipient_phone or not message_body:
            return jsonify({'error': 'Missing phone or message'}), 400
        
        # Send message via Twilio
        message = twilio_client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=recipient_phone
        )
        
        return jsonify({
            'success': True,
            'message_sid': message.sid
        }), 200
        
    except Exception as error:
        print(f"Twilio Send Error: {error}")
        return jsonify({'error': 'Failed to send message'}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200

def generate_response(user_input):
    """Generate bot response based on user input"""
    user_input_lower = user_input.lower()
    
    if '1' in user_input_lower or 'music' in user_input_lower:
        return 'Music is my passion. What would you like to know about my music?'
    elif '2' in user_input_lower or 'business' in user_input_lower:
        return 'I love discussing business strategies. Ask me anything!'
    elif '3' in user_input_lower or 'development' in user_input_lower:
        return 'Development is where innovation happens. What interests you?'
    elif '4' in user_input_lower or 'career' in user_input_lower:
        return 'My music career has been an amazing journey. Want to hear more?'
    else:
        return 'That\'s interesting! Tell me more.'

if __name__ == '__main__':
    app.run(debug=True, port=5000)
