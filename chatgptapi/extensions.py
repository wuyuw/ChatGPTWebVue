
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from client.chatgpt import ChatgptClient

limiter = Limiter(get_remote_address)
chatgpt = ChatgptClient()


def init_extensions(app):
    limiter.init_app(app)
    chatgpt.init_app(app)
