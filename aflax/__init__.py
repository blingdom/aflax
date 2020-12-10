#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (
    unicode_literals,
    print_function
    )

import os
import credentials

from config import (app_config)
from flask import (
    Flask,
    request,
    render_template
    )
from flask_mail import (Mail)
from flask_socketio import (SocketIO)

mail = Mail()
socketio = SocketIO()


def create_app(config_name):
    # Create App
    if os.getenv('FLASK_CONFIG') == "production":
        app = Flask(__name__)
        app.config.update(
            SECRET_KEY=os.getenv('SECRET_KEY')
        )

    else:
        app = Flask(
            __name__,
            instance_relative_config=True
            )
        app.config.from_object(app_config[config_name])
        app.config.from_pyfile('config.py')
        app.config['SECRET_KEY'] = credentials.FLASKSECRET

    # instantiate Mail App
    mail.init_app(app)

    # instantiate SocketIO
    # socketio.init_app(app)

    from .website import webview as web_blueprint
    app.register_blueprint(web_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .media import media as media_blueprint
    app.register_blueprint(media_blueprint)

    from .asterisk import asterisk as astx_blueprint
    app.register_blueprint(astx_blueprint)

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        from aflax.models import webnalysis

        if request.endpoint != 'static':
            ipadd = request.environ.get(
                'HTTP_X_REAL_IP',
                request.remote_addr
                )
            if ipadd in ['127.0.0.1', 'localhost']:
                pass
            else:
                webnalysis.indexcreate({
                    "access": request.endpoint,
                    "method": "404",
                    "ipadd": ipadd
                    })
        return render_template('errors/404.html'), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return render_template('errors/500.html'), 450

    @app.errorhandler(500)
    def internal_server_error(error):
        from aflax.models import webnalysis

        if request.endpoint != 'static':
            ipadd = request.environ.get(
                'HTTP_X_REAL_IP',
                request.remote_addr
                )
            if ipadd in ['127.0.0.1', 'localhost']:
                pass
            else:
                webnalysis.indexcreate({
                    "access": request.endpoint,
                    "method": "500",
                    "ipadd": ipadd
                    })
        return render_template('errors/500.html'), 500

    return app
