import json
from flask import Response
from flask_restful import Resource, reqparse
from common import response
from extensions import limiter, chatgpt
from config import Config


class ClientConfig(Resource):

    def post(self):
        usage = chatgpt.get_usage()
        data = {
            "apiModel": Config.OPENAI_API_MODEL,
            "reverseProxy": "-",
            "timeoutMs": Config.OPENAI_TIME_OUT,
            "socksProxy": Config.SOCKS_PROXY or '-',
            "httpsProxy": "-",
            "usage": usage
        }
        return response.ok_with_data(data)


class Session(Resource):

    def post(self):
        if not Config.AUTH_SECRET_KEY:
            return response.fail()
        data = {
            'auth': True,
            'model': "ChatGPTAPI"
        }
        return response.ok_with_data(data)


class Verify(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str)
        kwargs = parser.parse_args()
        token = kwargs['token']
        if not token or token != Config.AUTH_SECRET_KEY:
            return response.fail_with_msg('无效的访问密码')
        return response.ok()


class ChatProcess(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('prompt', type=str)
        parser.add_argument('systemMessage', type=str)
        parser.add_argument('model', type=str)
        parser.add_argument('options', type=dict, location='json')
        parser.add_argument('messages', type=list, location='json')
        kwargs = parser.parse_args()

        messages = kwargs['messages']
        if len(messages) > 7:
            messages = messages[-7:]

        # https://betterprogramming.pub/openai-sse-sever-side-events-streaming-api-733b8ec32897
        def stream_completion():
            resp = chatgpt.chat_completion(messages=messages, model=kwargs['model'], stream=True)
            data = {
                'role': 'assistant',
                'id': '',
                'text': '',
            }
            for chunk in resp:
                data['id'] = chunk['id']
                delta = chunk['choices'][0]['delta']
                if delta.get('content'):
                    data['delta'] = delta['content']
                    data['text'] += delta['content']
                data['detail'] = chunk
                yield json.dumps(data, ensure_ascii=False) + '\n'

        return Response(stream_completion(), mimetype='application/octet-stream')
