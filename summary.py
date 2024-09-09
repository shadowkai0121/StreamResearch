import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

apikey = os.getenv('GPT_API_KEY')

client = OpenAI(api_key=apikey)

with open('data/≪ENigmatic Recollection≫ ...they found me/01-33_01-49_chat.csv', 'r', encoding='utf8') as f:
    messages = f.read().strip()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": '''
You will be provided with youtube chat messages, and your task is to summarize the message as follows:

-Overall summary of discussion
-Situation (the chat's sentiment and the liver is doing what)
'''.strip()
        },
        {
            "role": "user",
            "content": messages
        }
    ],
    max_tokens=512,
)
with open('res.json', 'w', encoding='utf8') as f:
    f.write(response.to_json())
