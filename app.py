from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    print("⚠️ WARNING: GOOGLE_API_KEY not found!")

genai.configure(api_key=api_key)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        max_tokens = int(data.get('max_tokens', 800))

        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        model = genai.GenerativeModel(
            'gemini-3.5-flash',
            system_instruction="You are a friendly, encouraging AI Study Assistant. Be clear, educational, and motivating."
        )

        response = model.generate_content(
            user_message,
            generation_config={
                "max_output_tokens": max_tokens,
                "temperature": 0.7
            }
        )

        return jsonify({'response': response.text})
    
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower():
            error_msg = "⏳ Quota exceeded. Please wait 1 minute and try again."
        return jsonify({'error': error_msg}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=False)
