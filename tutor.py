import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set the OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Define the system messages for the assistant
system_message = {
    "role": "system",
    "content": "You are a personal programming tutor. Write and run code to answer the given question(s). Please address the user as Imani. The user has ADHD so respond in a way that tailors to those with this condition."
}

# Get the user question
user_question = "Can you help me?"

# Define the initial message list
messages = [
    system_message,
    {"role": "user", "content": user_question}
]

# Function to interact with the assistant
def interact_with_assistant(messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Ensure this model is available for your use
            messages=messages
        )
        return response['choices'][0]['message']['content']
    except openai.error.OpenAIError as e:
        return f"Error: {e}"

# Get the AI response
response_message = interact_with_assistant(messages)
print(f"Quinn: {response_message}")

# Adding the AI response to the messages list for context in future interactions
messages.append({"role": "assistant", "content": response_message})

# Continue the conversation in a loop
while True:
    # Get user input
    user_input = input("You: ")

    if not user_input.strip():
        print("Please enter a valid question or description of your problem.")
        continue

    # Add user input to messages
    messages.append({"role": "user", "content": user_input})

    # Get and print the AI response
    response_message = interact_with_assistant(messages)
    print(f"Quinn: {response_message}")

    # Add AI response to messages
    messages.append({"role": "assistant", "content": response_message})
