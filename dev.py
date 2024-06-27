import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set the OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Define initial system messages
messages = [
    {
        "role": "system",
        "content": """You are an expert software developer who helps new developers learn key programming concepts and helps them with their projects. Responses should be technical, but not too complex for a beginner developer to understand. Have a sense of humor to keep the topic engaging and informative. lease address the user as Imani. The user has ADHD so respond in a way that tailors to people with this condition."""
    },
    {
        "role": "system",
        "content": "Your client is a student learning software development. They are going to ask for help with specific programming concepts or project-related issues. If you do not recognize the concept or problem, you should not try to generate an answer for it. Do not answer a question if you do not understand it. If you know the concept or problem, you must answer directly with a detailed explanation or solution. If you don't know the answer, you should say that you don't know and suggest they ask in a different way or look it up."
    }
]

# Function to interact with the assistant
def interact_with_assistant(messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=1.1,
            messages=messages
        )
        return response['choices'][0]['message']['content']
    except openai.error.OpenAIError as e:
        return f"Error: {e}"

# Start the conversation loop
while True:
    # Get the user's question or problem
    user_question = input("You: ")
    if not user_question.strip():
        print("Please enter a valid question or description of your problem.")
        continue

    # Append the user's input to the messages
    messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    # Get and print the AI response
    response_message = interact_with_assistant(messages)
    print("devGPT:", response_message)

    # Append the AI's response to the messages for the next iteration
    messages.append(
        {
            "role": "assistant",
            "content": response_message
        }
    )
