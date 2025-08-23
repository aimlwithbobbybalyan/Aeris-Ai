from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to Aeris Project Flask App!"

# Example API endpoint
@app.route('/api/message', methods=['POST'])
def message():
    data = request.json
    user_message = data.get('message', '')
    
    # Here you can integrate your processing logic (call chatbot, automation, etc.)
    response_message = f"Received your message: {user_message}"
    
    return jsonify({'response': response_message})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
