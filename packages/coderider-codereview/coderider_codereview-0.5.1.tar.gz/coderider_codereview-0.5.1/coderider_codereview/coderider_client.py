import json
import requests
from furl import furl

from coderider_codereview import configs


class CoderiderClient:

    def __init__(self):
        self.jwt = None
        self._host = configs.CR_SERVER_HOST
        self._bot_token = configs.CR_AI_BOT_TOKEN
        self._timeout = configs.CR_LLM_TIMEOUT

    def login(self):
        url = furl(self._host).join("api/v1/auth/jwt").url
        headers = {
            "Content-Type": "application/json",
            "PRIVATE-TOKEN": self._bot_token
        }
        response = requests.post(url, headers=headers)
        self.jwt = response.json()
        return self

    def chat_completions(self, messages: list):
        url = furl(self._host).join("api/v1/llm/v1/chat/completions").url
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.jwt['token']}"
        }
        data = {
            "stream": False,
            "model": configs.CR_LLM_MODEL,
            "messages": messages
        }

        if configs.CR_DEBUG:
            print(f"Request Chat completions to: {url}\n")
            print(data)
            print("\n\n-----\n\n")

        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response.json()


if __name__ == '__main__':
    client = CoderiderClient()
    client.login()
    messages = [
        {
            "role": "system",
            "content": "You are an intelligent assistant."
        },
        {
            "role": "user",
            "content": "Introduce GitLab in one sentence."
        }
    ]
    resp = client.chat_completions(messages)
    content = resp["choices"][0]["message"]["content"]
