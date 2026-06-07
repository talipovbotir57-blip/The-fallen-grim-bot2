from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('Chatbot.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'reply': 'No message received'})
    
    try:
        bot_reply = generate_response(user_message)
        return jsonify({'reply': bot_reply})
    except Exception as error:
        return jsonify({'reply': 'Failed to connect'})

def generate_response(user_input):
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
    app.run(debug=True)
