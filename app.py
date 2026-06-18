from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configure Gemini
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    print("⚠️  WARNING: GOOGLE_API_KEY not found in environment variables!")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        prompt = f"""You are a friendly, encouraging, and highly knowledgeable AI Study Assistant.
        Help students with studies. Be clear, educational, and motivating.
        
        User: {user_message}
        
        Respond helpfully and naturally."""

        response = model.generate_content(prompt)
        return jsonify({'response': response.text})
    
    except Exception as e:
        error_msg = str(e)
        if "API key" in error_msg.lower():
            error_msg = "Missing or invalid Gemini API key. Please check your .env file."
        return jsonify({'error': error_msg}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=False)