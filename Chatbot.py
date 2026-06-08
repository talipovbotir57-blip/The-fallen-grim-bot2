import logging
import os
from functools import wraps
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Flask app setup
app = Flask(__name__, template_folder='templates')
CORS(app)

# Configuration from environment variables
def get_config():
    """Load and validate configuration from environment variables"""
    config = {
        'TWILIO_ACCOUNT_SID': os.getenv('TWILIO_ACCOUNT_SID'),
        'TWILIO_AUTH_TOKEN': os.getenv('TWILIO_AUTH_TOKEN'),
        'TWILIO_PHONE_NUMBER': os.getenv('TWILIO_PHONE_NUMBER'),
        'API_KEY': os.getenv('API_KEY'),
        'DEBUG': os.getenv('DEBUG', 'False').lower() == 'true',
        'PORT': int(os.getenv('PORT', 5000))
    }
    
    return config

try:
    config = get_config()
    # Initialize Twilio client
    twilio_client = Client(config['TWILIO_ACCOUNT_SID'], config['TWILIO_AUTH_TOKEN'])
    logger.info("Twilio client initialized successfully")
except ValueError as e:
    logger.critical(f"Configuration error: {e}")
    raise

# Authentication decorator
def require_api_key(f):
    """Decorator to require API key for protected endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != config['API_KEY']:
            logger.warning(f"Unauthorized access attempt from {request.remote_addr}")
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    """Serve the main chatbot interface"""
    try:
        return render_template('Chatbot.html')
    except Exception as e:
        logger.error(f"Error loading index: {e}")
        return jsonify({'error': 'Failed to load chatbot'}), 500

@app.route('/chat', methods=['POST'])
def chat():
    """Handle web chat requests"""
    try:
        data = request.get_json(silent=True)
        if data is None:
            logger.warning("Received invalid JSON format")
            return jsonify({'reply': 'Invalid JSON format'}), 400
        
        user_message = data.get('message', '').strip()
        
        if not user_message:
            logger.warning("Received empty message")
            return jsonify({'reply': 'No message received'}), 400
        
        # Sanitize input (basic protection)
        if len(user_message) > 1000:
            logger.warning("Message exceeds length limit")
            return jsonify({'reply': 'Message too long'}), 400
        
        bot_reply = generate_response(user_message)
        logger.info(f"Web chat - User: {user_message[:50]}... Bot: {bot_reply[:50]}...")
        return jsonify({'reply': bot_reply}), 200
        
    except Exception as error:
        logger.error(f"Web Chat Error: {error}", exc_info=True)
        return jsonify({'reply': 'Server error'}), 500

@app.route('/twilio/webhook', methods=['POST'])
def twilio_webhook():
    """Handle Twilio WhatsApp/SMS webhook"""
    try:
        # Validate Twilio request (optional but recommended)
        incoming_msg = request.form.get('Body', '').strip()
        sender_phone = request.form.get('From', '')
        
        if not incoming_msg:
            logger.warning("Received empty message from Twilio")
            resp = MessagingResponse()
            resp.message("No message received")
            return str(resp)
        
        # Sanitize input
        if len(incoming_msg) > 1000:
            logger.warning(f"Message from {sender_phone} exceeds length limit")
            resp = MessagingResponse()
            resp.message("Message too long")
            return str(resp)
        
        # Generate bot response
        bot_reply = generate_response(incoming_msg)
        
        # Create Twilio response
        resp = MessagingResponse()
        resp.message(bot_reply)
        
        logger.info(f"Twilio message from {sender_phone}: {incoming_msg[:50]}...")
        
        return str(resp), 200
        
    except Exception as error:
        logger.error(f"Twilio Webhook Error: {error}", exc_info=True)
        resp = MessagingResponse()
        resp.message("Failed to connect to bot")
        return str(resp), 500

@app.route('/twilio/send', methods=['POST'])
@require_api_key
def twilio_send():
    """Send Twilio message (for outbound messages)"""
    try:
        data = request.get_json(silent=True)
        if data is None:
            logger.warning("Invalid JSON format in twilio/send request")
            return jsonify({'error': 'Invalid JSON format'}), 400
        
        recipient_phone = data.get('to', '').strip()
        message_body = data.get('message', '').strip()
        
        if not recipient_phone or not message_body:
            logger.warning("Missing phone or message in twilio/send request")
            return jsonify({'error': 'Missing phone or message'}), 400
        
        # Validate phone format (basic check)
        if not recipient_phone.startswith('+'):
            recipient_phone = '+' + recipient_phone
        
        # Validate message length
        if len(message_body) > 1000:
            logger.warning("Message exceeds length limit in twilio/send")
            return jsonify({'error': 'Message too long'}), 400
        
        # Send message via Twilio
        message = twilio_client.messages.create(
            body=message_body,
            from_=config['TWILIO_PHONE_NUMBER'],
            to=recipient_phone
        )
        
        logger.info(f"Sent message to {recipient_phone}: {message_body[:50]}... (SID: {message.sid})")
        
        return jsonify({
            'success': True,
            'message_sid': message.sid
        }), 200
        
    except Exception as error:
        logger.error(f"Twilio Send Error: {error}", exc_info=True)
        return jsonify({'error': 'Failed to send message'}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'version': '1.0'}), 200

# Bot response generation
def generate_response(user_input):
    """Generate bot response based on user input"""
    user_input_lower = user_input.lower().strip()
    
    # Response mapping
    responses = {
        'music': 'Music is my passion. What would you like to know about my music?',
        'business': 'I love discussing business strategies. Ask me anything!',
        'development': 'Development is where innovation happens. What interests you?',
        'career': 'My music career has been an amazing journey. Want to hear more?',
        'help': 'I can help you with music, business, development, or career questions. What interests you?',
    }
    
    # Check for keyword matches
    for keyword, response in responses.items():
        if keyword in user_input_lower:
            return response
    
    # Check for numeric input (1-4)
    if user_input_lower in ['1', '2', '3', '4']:
        numeric_responses = {
            '1': 'Music is my passion. What would you like to know about my music?',
            '2': 'I love discussing business strategies. Ask me anything!',
            '3': 'Development is where innovation happens. What interests you?',
            '4': 'My music career has been an amazing journey. Want to hear more?',
        }
        return numeric_responses.get(user_input_lower, "That's interesting! Tell me more.")
    
    # Default response
    return "That's interesting! Tell me more."

# Error handlers
@app.errorhandler(404)
def not_found(error):
    logger.warning(f"404 error: {request.path}")
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 error: {error}", exc_info=True)
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info(f"Starting Chatbot application (debug={config['DEBUG']}, port={config['PORT']})")
    app.run(debug=config['DEBUG'], port=config['PORT'], host='0.0.0.0')
