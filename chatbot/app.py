# from flask import Flask, request, jsonify, render_template
# from chatbot.chat import chat_with_gpt

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/chat', methods=['POST'])
# def chat():
#     prompt = request.json.get('prompt')
#     response = chat_with_gpt(prompt)
#     return jsonify({'response': response})

# if __name__ == '__main__':
#     app.run(debug=True)
