# -*- coding: utf-8 -*-
"""
   Mocker
   ~~~~~~

   Tool to simplify creating HTML mockups.
"""
from flask import Flask, render_template, make_response, abort
from jinja2 import Template, FileSystemLoader, Environment
import os
import glob
import yaml

app = Flask(__name__)
app.config['DEBUG'] = True

@app.context_processor
def helpers():
    return {
        'basename': os.path.basename
    }

loader = FileSystemLoader(".")
env = Environment(loader=loader)

@app.route("/")
@app.route("/<path:path>")
def mock(path=""):
    if not os.path.exists(path or "."):
        abort(404)

    elif os.path.isdir(path or "."):
        return mock_index(path)
    elif path.endswith(".html"):
        return mock_html(path)
    else:
        abort(404)

def mock_index(path):
    if path == "." or path == "":
        dirname = ""
    else:
        dirname = path + "/"

    parent = os.path.dirname(path)
    # TODO: generalize to work with windows as well
    dirs = glob.glob(dirname + "*/")
    # convert a/b/ to a/b
    dirs = [os.path.normpath(d) for d in dirs]

    htmlfiles = glob.glob(dirname + "*.html")
    return render_template("index.html", path=dirname, parent=parent, dirs=dirs, htmlfiles=htmlfiles)

def mock_html(path):
    t = env.get_template(path)
    arguments = read_arguments(path)
    html = t.render(**arguments)
    response = make_response(html)
    return response

def replace_ext(path, new_ext):
    """Returns a new path after replacing the current extension in the path with new extension provided.
    """
    root, ext = os.path.splitext(path)
    return root + new_ext

def read_arguments(html_path):
    yaml_path = replace_ext(html_path, ".yml")
    if not os.path.exists(yaml_path):
        return {}
    return yaml.safe_load(open(yaml_path))

def main():
    app.run()
