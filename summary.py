import os
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
from env_ import Env_

class Summary:
    client = OpenAI(api_key=os.getenv('GPT_API_KEY'))
    _env: Env_
    _messages: str
    response = None

    def __init__(self, env_: Env_, messages: str) -> None:
        self._env = env_
        self._messages = messages

    def get(self) -> ChatCompletion:
        response = self.client.chat.completions.create(
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
                    "content": self._messages
                }
            ],
            max_tokens=512,
        )
        self.response = response
        return self.response

    def getContent(self) -> str:
        if self.response is not None:
            return self.response.choices[0].message.content
        else:
            return self.get().choices[0].message.content
# with open('res.json', 'w', encoding='utf8') as f:
#     f.write(response.to_json())
