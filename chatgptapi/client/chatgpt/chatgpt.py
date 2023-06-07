import os
import calendar
from datetime import date
import logging
import requests
import openai

logger = logging.getLogger(__name__)


class OpenAIException(Exception):
    pass


class ChatgptClient(object):

    def __init__(self, openai_key='', base_url='', api_model='', socks_proxy='', timeout=0):
        self.base_url = base_url
        self.openai_key = openai_key
        self.api_model = api_model
        self.socks_proxy = socks_proxy
        self.timeout = timeout
        openai.api_key = self.openai_key
        if socks_proxy:
            openai.proxy = socks_proxy

    def init_app(self, app):
        if not app.extensions.get('chatgpt'):
            self.openai_key = app.config.get('OPENAI_API_KEY')
            self.base_url = app.config.get('OPENAI_BASE_URL')
            self.api_model = app.config.get('OPENAI_API_MODEL')
            self.socks_proxy = app.config.get('SOCKS_PROXY')
            self.timeout = app.config.get('OPENAI_TIME_OUT')
            if not self.openai_key:
                raise OpenAIException('OpenAI API Key 未设置')
            openai.api_key = self.openai_key
            if self.socks_proxy:
                openai.proxy = self.socks_proxy
            app.extensions["chatgpt"] = self

    def chat_completion(self, messages, model="", stream=False):
        print(messages)
        response = openai.ChatCompletion.create(
            model=model or self.api_model,
            messages=messages,
            temperature=0.8,
            timeout=self.timeout,
            stream=stream
        )
        logger.info(messages)
        return response

    def get_usage(self):
        month_first_day = date.today().replace(day=1)
        month_days = calendar.monthrange(month_first_day.year, month_first_day.month)[1]
        month_last_day = date.today().replace(day=month_days)
        url_usage = f'{self.base_url}/v1/dashboard/billing/usage?start_date={month_first_day}&end_date={month_last_day}'
        headers = {
            'Authorization': f'Bearer {self.openai_key}',
            'Content-Type': 'application/json',
        }
        proxies = {
            'http': self.socks_proxy,
            'https': self.socks_proxy
        }
        resp = requests.get(url_usage, headers=headers, proxies=proxies)
        data = resp.json()
        if not resp.ok:
            raise OpenAIException(data['error']['message'])
        usage = round(data['total_usage'] / 100, 2)
        return f'${usage}'

