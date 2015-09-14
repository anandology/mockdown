# -*- coding: utf-8 -*-
"""
   Mocker
   ~~~~~~

   Tool to simplify creating HTML mockups.
"""
import os
import glob
import hashlib
from StringIO import StringIO

from flask import Flask, render_template, make_response, abort
from jinja2 import Template, FileSystemLoader, Environment
from faker import Faker
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
    elif path.endswith(".yml"):
        return mock_yaml(path)
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
    arguments = read_arguments(path)
    html = render_mock_template(path, **arguments)
    response = make_response(html)
    return response

def mock_yaml(path):
    yaml_text = read_yaml_file(path)
    response = make_response(yaml_text)
    response.headers['Content-Type'] = 'text/yaml'
    return response


def render_mock_template(path, **kwargs):
    t = env.get_template(path)
    return t.render(**kwargs)

def replace_ext(path, new_ext):
    """Returns a new path after replacing the current extension in the path with new extension provided.
    """
    root, ext = os.path.splitext(path)
    return root + new_ext

def generate_unique_number(text):
    """Generate unique number from a text.
    """
    return int(hashlib.md5(text).hexdigest(), 16) % 10000

def read_arguments(html_path):
    yaml_path = replace_ext(html_path, ".yml")
    yaml_text = read_yaml_file(yaml_path)
    return yaml.safe_load(StringIO(yaml_text))

def read_yaml_file(yaml_path):
    if not os.path.exists(yaml_path):
        return '{}'

    # Pass the yaml text through jinja to make it possible to include fake data
    fake = Faker()
    # generate a seed from the filename so that we always get the same data
    fake.seed(generate_unique_number(yaml_path))
    yaml_text = render_mock_template(yaml_path, fake=fake)
    return yaml_text

def main():
    app.run()
