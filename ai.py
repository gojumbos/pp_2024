import copy
import re

from openai import OpenAI
from dotenv import load_dotenv
import os
from random import randint

SYSTEM = ("You are a 20 Questions game host. Wait for the user's yes/no questions and respond accordingly. "
           "Only say 'Ask your first question' once at the start. Tell me the answer you have in mind as your "
          "first response inside curly brackets like: {hedgehog}, but don't say 'hedgehog', say the object "
          "you are thinking of. Do not tell me the answer unless I say something "
          "like 'I give up' or 'just tell me'. If the question limit of 20 is reached, reveal the answer. I will "
          "feed you the current question count as well. ")


model = "gpt-4.1"

# Load environment variables from the .env file
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
# print(api_key)

class ChatManager:
  """
    A very information-insecure implementation chat isolation
    Avoiding using actual cookie implementations for user anonymity
  """
  def __init__(self):
    self.all_ais_dict = {}
    self.last_call_time = None
    # an ai is a chat

  async def add_chat(self):
    global_id = randint(0,1000)
    while global_id in self.all_ais_dict:
      global_id = randint(0,1000)
    ai = AIObject(global_id=global_id)
    # ai.ai_start_chat()
    self.all_ais_dict[ai.my_id] = ai
    return ai.my_id

  async def start_chat(self, global_id):
    # start chat after adding ai
    ai = self.all_ais_dict[int(global_id)]
    return await ai.ai_start_chat()

  async def get_convo(self, global_id):
    # get ai given its global id

    return self.all_ais_dict[int(global_id)].conversation

  async def send_chat(self, global_id, user_message):
    return await self.all_ais_dict[int(global_id)].ai_chat(user_message)

  async def remove_chat(self, ai):
    del self.all_ais_dict[ai.my_id]

  async def clear_all_chats(self):
    # reset all after time period elapsed
    self.all_ais_dict = {}

  async def chat_count(self):
    return len(self.all_ais_dict)


CONVO_STUB = [
      {"role": "system", "content": "You are a game chat bot. Keep responses very simple."},
      {"role": "user", "content": SYSTEM},
    ]

class AIObject:

  def __init__(self, global_id):
    self.client = OpenAI(api_key=api_key)
    self.conversation = copy.deepcopy(CONVO_STUB)
    self.question_ctr = 1
    self.my_id = global_id
    self.solution = None

  async def incr_ctr(self):
    self.question_ctr += 1

  async def question_limit_hit(self):
    return self.question_ctr == 20

  async def reset(self):
    self.conversation = CONVO_STUB
    self.question_ctr = 0

  async def ai_start_chat(self):
    response = self.client.responses.create(
      model=model,
      input=self.conversation
    )
    solution = re.findall(r'{(.*?)}', response.output_text)
    self.solution = solution
    text = re.sub(r'{.*?}', '', response.output_text)
    self.conversation.append({"role": "assistant", "content": response.output_text})
    await self.incr_ctr()
    return text

  async def ai_chat(self, prompt):
    prompt = prompt + f' <System: Question number {self.question_ctr}>'
    self.conversation.append({"role": "user", "content": prompt})
    response = self.client.responses.create(
      model=model,
      input=self.conversation
    )
    self.conversation.append({"role": "assistant", "content": response.output_text})
    await self.incr_ctr()
    return response.output_text
