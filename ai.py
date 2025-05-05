



from openai import OpenAI
from dotenv import load_dotenv
import os

starter = "You are a 20 Questions game host. Wait for the user's yes/no questions and respond accordingly. Only say 'Ask your first question' once at the start."


model = "gpt-4.1"

# Load environment variables from the .env file
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print(api_key)

class ai_object:

  def __init__(self):
    self.client = OpenAI(api_key=api_key)
    self.conversation  = [
      {"role": "system", "content": "You are a game chat bot. Keep responses very simple."},
      {"role": "user", "content": starter}, 
    ]

  def reset(self):
    self.conversation = [
      {"role": "system", "content": "You are a game chat bot. Keep responses very simple."},
      {"role": "user", "content": starter}, 
    ]

  def ai_start_chat(self):
    response = self.client.responses.create(
    model=model,
    input=self.conversation
    )
    self.conversation.append({"role": "assistant", "content": response.output_text})
    return response.output_text

  def ai_chat(self, prompt):
    self.conversation.append({"role": "user", "content": prompt})
    response = self.client.responses.create(
    model=model,
    input=self.conversation
    )
    self.conversation.append({"role": "assistant", "content": response.output_text})
    return response.output_text
