# -*- coding: UTF-8 -*-

import logging

from distutils.util import strtobool

from .common import app_config, command

logger = logging.getLogger(__name__)

@command
def migrate():
    """
    migrate database
    """
    from .models import migrate as models_migrate
    models_migrate()

@command
def serve(port=8080, host='127.0.0.1', debug=None, server='cherrypy'):
    """
    run web server

    server=wsgiref,cherrypy,paste
    debug='0' or '1' defaults to 1 if log-level==debug
    """
    from .web import run, app
    if debug is None:
        debug = app_config.is_debug
    else:
        debug = bool(strtobool(debug))
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    run(app, server=server, host=host, port=port, reloader=debug, debug=debug)
