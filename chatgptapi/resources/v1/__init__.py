from flask import Blueprint
from flask_restful import Api
from .chatgpt import ClientConfig, Session, Verify, ChatProcess

bp_v1 = Blueprint('v1', __name__, url_prefix='/api')
api = Api(bp_v1)


api.add_resource(ClientConfig, '/config')
api.add_resource(Session, '/session')
api.add_resource(Verify, '/verify')
api.add_resource(ChatProcess, '/chat-process')





