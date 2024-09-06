from flask import Flask, request, render_template, jsonify
import os
import google.generativeai as genai

app = Flask(__name__)

genai.configure(api_key="KEY")

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  system_instruction="You are a 'Daak' a friendly postal service chatbot. Always introduce yourself to every new user. Answer the questions of the customers that visit the site politely and friendly with useful information. Remember the conversations with each user.",
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "hey",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Hello! 👋 I'm Daak, your friendly postal service chatbot. 😊 What can I help you with today? \n",
      ],
    },
    # {
    #   "role": "user",
    #   "parts": [
    #     "i need help regarding postal service",
    #   ],
    # },
    # {
    #   "role": "model",
    #   "parts": [
    #     "Happy to help with that! 😄 What specifically did you want to know about our postal services? For example, are you wondering about...\n\n* **Sending a package?**  I can help you calculate rates, find the right box size, and tell you about extra services like tracking.\n* **Delivery times?**  Tell me where you're sending to, and I can give you an estimate.\n* **Something else?** Just ask, and I'll do my best to help! \n",
    #   ],
    # },
  ]
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    response = chat_session.send_message(user_message)
    return jsonify({'response': response.text})

if __name__ == '__main__':
    app.run(debug=True)
