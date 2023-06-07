import unittest
from datetime import date
from chatgpt import ChatgptClient
from config import Config


class TestChatgpt(unittest.TestCase):

    def setUp(self) -> None:
        self.chatgpt = ChatgptClient(openai_key=Config.OPENAI_API_KEY,
                                     base_url=Config.OPENAI_BASE_URL,
                                     api_model='gpt-3.5-turbo',
                                     socks_proxy='http://127.0.0.1:51837')

    @unittest.skip
    def test_chat_completion(self):
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Knock knock."},
            {"role": "assistant", "content": "Who's there?"},
            {"role": "user", "content": "Orange."},
        ]
        resp = self.chatgpt.chat_completion(messages=messages, model='gpt-3.5-turbo')
        print(resp)

    @unittest.skip
    def test_chat_completion_stream(self):
        system_message = f"""
        You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible.
        Knowledge cutoff: 2021-09-01
        Current date: {date.today().strftime('%Y-%m-%d')}
        """
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": "flask响应结果流式返回"},
        ]
        resp = self.chatgpt.chat_completion(messages=messages, model='gpt-3.5-turbo', stream=True)
        for chunk in resp:
            print(chunk)

    @unittest.skip
    def test_get_usage(self):
        usage = self.chatgpt.get_usage()
        print(usage)

