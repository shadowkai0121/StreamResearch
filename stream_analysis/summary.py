import os
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
from stream_analysis.env_ import Env_
import tiktoken  # 用於計算 tokens

class Summary:
    client = OpenAI(api_key=os.getenv('GPT_API_KEY'))
    _env: Env_
    _messages: str
    _prompt: str
    response = None
    model = "gpt-4o-mini"
    max_tokens = 512  # API回應的max_tokens設定
    token_limit = 82400

    def __init__(self, env_: Env_, messages: str) -> None:
        self._env = env_
        self._messages = messages
        with open('./prompt/summary.txt', 'r', encoding='utf8') as f:
            self._prompt = f.read().strip()

    def _split_messages(self, text: str) -> list:
        """
        使用 tiktoken 計算並分割文本成符合 token 限制的批次。
        """
        encoding = tiktoken.encoding_for_model(self.model)
        tokens = encoding.encode(text)

        # 計算有多少批次，每批次 token 的長度限制為 (token_limit - max_tokens)，保留一些空間給 response
        batches = []
        for i in range(0, len(tokens), self.token_limit - self.max_tokens):
            batch_tokens = tokens[i:i + self.token_limit - self.max_tokens]
            batch_text = encoding.decode(batch_tokens)
            batches.append(batch_text)

        return batches

    def get(self) -> ChatCompletion:
        """
        將大型文本分批處理，並將每個回應串聯起來。
        """
        if not self._env.has_summary:
            self.response = 'No Summary'
            return self.response
        messages_batches = self._split_messages(self._messages)
        all_responses = []

        # 逐批發送請求並收集回應
        for batch in messages_batches:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._prompt
                    },
                    {
                        "role": "user",
                        "content": batch
                    }
                ],
                max_tokens=self.max_tokens,
            )
            all_responses.append(response.choices[0].message.content)

        # 合併所有批次的回應成一個字符串
        self.response = "\n".join(all_responses)
        return self.response

    def getContent(self) -> str:
        if self.response is not None:
            return self.response
        else:
            return self.get()

