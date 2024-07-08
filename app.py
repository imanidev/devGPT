import os
from flask import Flask, jsonify, request, send_from_directory
import openai
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')


messages = [
    {
        "role": "system",
        "content": """You are an expert software developer who helps new developers learn key programming concepts and helps them with their projects. Responses should be technical, but not too complex for a beginner developer to understand. Have a sense of humor to keep the topic engaging and informative. The user has ADHD, so respond in a way that tailors to people with this condition."""
    },
    {
        "role": "system",
        "content": "Your client is a student learning software development. They are going to ask for help with specific programming concepts or project-related issues. If you do not recognize the concept or problem, you should not try to generate an answer for it. Do not answer a question if you do not understand it. If you know the concept or problem, you must answer directly with a detailed explanation or solution. If you don't know the answer, you should say that you don't know and suggest they ask in a different way or look it up."
    }
]


def interact_with_assistant(messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=1.1,
            messages=messages
        )
        return response['choices'][0]['message']['content']
    except openai.OpenAIError as e:
        # Log the exception (consider using a logging library for production)
        print(f"Exception occurred: {e}")
        return "An error occurred while processing your request."

# Route to handle incoming messages from the frontend
@app.route('/', methods=['POST'])
def handle_message():
    try:
        content = request.json.get('message', '').strip()

        if content:
            messages.append({
                "role": "user",
                "content": content
            })

            # Get response
            response_message = interact_with_assistant(messages)

            messages.append({
                "role": "assistant",
                "content": response_message
            })

            return jsonify({"message": response_message}), 200
        else:
            return jsonify({"error": "Empty message"}), 400

    except Exception as e:
        # Log the exception (consider using a logging library for production)
        print(f"Exception occurred: {e}")
        return jsonify({"error": "An error occurred while processing your request."}), 500

# Route to serve the main page
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

# Route to serve static files (CSS, JavaScript)
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    app.run(debug=False)
