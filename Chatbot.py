import logging
import os
from functools import wraps
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

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
        'API_KEY': os.getenv('API_KEY'),
        'DEBUG': os.getenv('DEBUG', 'False').lower() == 'true',
        'PORT': int(os.getenv('PORT', 5000))
    }
    
    return config

try:
    config = get_config()
    logger.info("Configuration loaded successfully")
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
