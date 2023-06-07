from flask import Flask,request, render_template, send_from_directory
from config import Config
from resources.v1 import bp_v1
from extensions import init_extensions
from middleware import init_middleware


def register_static(app):

    @app.route('/')
    def index():
        return send_from_directory('static', 'index.html')

    @app.route('/assets/<path:filename>')
    def assets(filename):
        return send_from_directory('static/assets', filename)

    @app.route('/favicon.<string:ext>')
    def favicon(ext):
        return send_from_directory('static', f'favicon.{ext}', mimetype='image/vnd.microsoft.icon')


def create_app(config_map=None):
    # create and configure the app
    app = Flask(__name__,
                instance_relative_config=True,
                static_folder='static',
                template_folder='static')
    if config_map:
        app.config.from_mapping(config_map)
    app.config.from_object(Config)
    # 注册蓝图
    app.register_blueprint(bp_v1)
    register_static(app)
    # 初始化扩展
    init_extensions(app)
    # 初始化中间件
    init_middleware(app)

    return app


