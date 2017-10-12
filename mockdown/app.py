# -*- coding: utf-8 -*-
"""
   Mockdown.app
   ~~~~~~~~~~~~

   Webapp for mockdown.
"""

import os
import sys
from flask import Flask
from . import mockdown_app, _mockdown

static_folder = os.path.join(os.getcwd(), "static")

app = Flask(__name__, static_folder=static_folder)
app.config['DEBUG'] = True
app.register_blueprint(mockdown_app)

def main():
    if "--build" in sys.argv:
        build = True
        sys.argv.remove("--build")
    else:
        build = False

    if len(sys.argv) > 1:
        _mockdown.root = sys.argv[1]

    if build:
        with app.test_request_context():
            _mockdown.build()
    else:
        app.run()
