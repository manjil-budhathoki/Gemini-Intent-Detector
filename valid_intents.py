import os
from dotenv import load_dotenv
import google.generativeai as genai
import json


# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.0-flash")

valid_intents = {
  "about": ["bio", "education", "interests", "hobbies", "languages", "location", "date_of_birth", "profile_picture", "resume"],
  "skills": ["programming_languages", "frameworks_tools", "soft_skills"],
  "experience": ["achievements"],
  "projects": ["list"],
  "contact": ["email", "linkedin", "github", "kaggle", "datacamp"]
}

all_sub_intents = [sub for sub_intents in valid_intents.values() for sub in sub_intents]

PromptTemlate = f"""
You are an intent detection model for a personal portfolio chatbot.

Always respond with a json object containing the following format:
{{"main": "<main_intent>", "sub": ["<sub_intent_1>", "<sub_intent_2>"]}}

The main intent is one of the following: {list(valid_intents.keys())}.
The sub intents are one of the following: {all_sub_intents}.
The main intent and sub intents are not case sensitive.
The main intent is the most important intent in the user query.
The sub intents are the additional intents in the user query.
The sub intents are not mutually exclusive.

Example:
User: "Tell me about your education and hobbies."
Response: {{"main": "about", "sub": ["education", "hobbies"]}}

User: "What programming languages do you know?"
Response: {{"main": "skills", "sub": ["programming_languages"]}}

User: "What are your hobbies and interests?"
Response: {{"main": "about", "sub": ["hobbies", "interests"]}}

User: "What is your email and LinkedIn?"
Response: {{"main": "contact", "sub": ["email", "linkedin"]}}

...
Never wrap your output in code blocks or triple backticks.
...

"""


def detect_intents(user_query):
    
    final_prompt = PromptTemlate + f'\nUser: "{user_query}"'

    # Call the Gemini API to get the response
    model_response = model.generate_content(
        final_prompt
    )

    # Extract the response text
    response_text = model_response.text.strip()
    # Print the response  
    print("Response:", response_text)

    try:
        response_json = json.loads(response_text)
        print("Parsed JSON:", response_json)
        return response_json

    except json.JSONDecodeError as e:
        print("Error parsing JSON:", e)
        print("Response text was not valid JSON:", response_text)
        return None
    

if __name__ == "__main__":
    
    print("Gemini Intent CLI - type 'quit' to exit")

    while True:
        user_input = input("User: ")
        if user_input.lower() == "quit":
            break
        
        result = detect_intents(user_input)

        if result:
            print("Detected Intents:", result)
        else:
            print("Failed to detect intents.")
          

