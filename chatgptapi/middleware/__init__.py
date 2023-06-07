from .auth import auth_middleware


def init_middleware(app):
    auth_middleware(app)
