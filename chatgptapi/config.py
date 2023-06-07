import os
from dotenv import load_dotenv

# 读取配置至环境变量
load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'chatgptapi'
    AUTH_SECRET_KEY = os.getenv('AUTH_SECRET_KEY')
    RATE_LIMIT = os.getenv('RATE_LIMIT')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL') or 'https://api.openai.com'
    OPENAI_API_MODEL = os.getenv('OPENAI_API_MODEL') or 'gpt-3.5-turbo'
    SOCKS_PROXY = os.getenv('SOCKS_PROXY')
    HTTPS_PROXY = os.getenv('HTTPS_PROXY')
    OPENAI_TIME_OUT = os.getenv('OPENAI_TIME_OUT') or 60


