from flask import request
from common import response
from config import Config

UNAUTH_URLS = [
    '/',
    '/favicon.<string:ext>',
    '/assets/<path:filename>',
    '/api/session',
    '/api/verify'
]


def auth_middleware(app):
    @app.before_request
    def auth():
        if request.url_rule.rule in UNAUTH_URLS:
            return
        if "Authorization" not in request.headers:
            return response.unauth()
        token = request.headers["Authorization"].split(" ")[1]
        if token != Config.AUTH_SECRET_KEY:
            return response.unauth()
