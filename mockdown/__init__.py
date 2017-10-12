# -*- coding: utf-8 -*-
"""
   Mockdown
   ~~~~~~~~

   Tool to simplify creating HTML mockups.
"""
from flask import Blueprint, render_template, abort, redirect, url_for
import yaml
import pathlib
from .mockdown import Mockdown

mockdown_app = Blueprint("mockdown", __name__,
                         template_folder="templates")

_mockdown = Mockdown(root=".")

def mockdown_url_for(endpoint, **kwargs):
    if endpoint == 'static':
        return url_for('static', **kwargs)
    else:
        return url_for('.mock', path=endpoint + ".html")

_mockdown.template_globals['url_for'] = mockdown_url_for

@mockdown_app.route("/")
@mockdown_app.route("/<path:path>")
def mock(path=""):
    if not _mockdown.exists(path):
        abort(404)
    elif _mockdown.is_dir(path):
        return mock_index(path)
    elif path.endswith(".html"):
        return _mockdown.render_template(path)
    elif path.endswith(".yml"):
        data = _mockdown.read_yaml_file(path)
        return yaml.dump(data)
    else:
        print("aborting...")
        abort(404)

def mock_index(path):
    if path and not path.endswith("/"):
        return redirect("/" + path + "/")

    root = pathlib.Path(_mockdown.root).name
    pathobj = pathlib.Path(_mockdown.root, path)
    subdirs = [p.name for p in pathobj.iterdir() if p.is_dir()]
    filenames = [f.name for f in pathobj.glob("*.html")]
    return render_template("index.html", root=root, path=path, subdirs=subdirs, filenames=filenames)

