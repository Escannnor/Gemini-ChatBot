from .gemini_api import generate_response
import logging
from .gemini_api import generate_response

def chat_with_gpt(prompt):
    return generate_response(prompt)



logging.basicConfig(level=logging.INFO)

def chat_with_gpt(prompt):
    try:
        response = generate_response(prompt)
        logging.info(f"Prompt: {prompt} | Response: {response}")
        return response
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return f"An error occurred: {str(e)}"

