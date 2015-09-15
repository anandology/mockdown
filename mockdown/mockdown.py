import hashlib
import pathlib
import yaml
from faker import Faker
from StringIO import StringIO
from jinja2 import Template, FileSystemLoader, Environment

class Mockdown:
    def __init__(self, root):
        self.set_root(root)

    def set_root(self, root):
        self.root = root
        self._env = None

    def _get_env(self):
        if self._env is None:
            loader = FileSystemLoader(self.root)
            self._env = Environment(loader=loader)
        return self._env

    def render_template(self, path):
        """Renders a user template from given path.

        The arguments will be read from the YAML file with same basename.
        It is considered that the path is relative to the Mockdown root.
        """
        kwargs = self.read_arguments(path)
        return self._render_template(path, **kwargs)

    def _render_template(self, path, **kwargs):
        """Renders a user template from given path.
        It is considered that the path is relative to the Mockdown root.
        """
        env = self._get_env()
        t = env.get_template(path)
        return t.render(**kwargs)

    def read_arguments(self, html_path):
        """Reads arguments for rendering template at specified path.
        """
        yaml_path = self._with_suffix(html_path, ".yml")
        yaml_text = self.read_yaml_file(yaml_path)
        return yaml.safe_load(StringIO(yaml_text))

    def read_yaml_file(self, path):
        if not self.exists(path):
            return '{}'

        # Pass the yaml text through jinja to make it possible to include fake data
        fake = Faker()
        # generate a seed from the filename so that we always get the same data
        fake.seed(self._generate_seed(str(path)))
        yaml_text = self._render_template(path, fake=fake)
        return yaml_text

    def _generate_seed(self, seed_text):
        """Generates unique integer seed from given text.
        """
        return int(hashlib.md5(seed_text).hexdigest(), 16) % 10000

    def get_relative_path(self, path):
        """Returns the path relative to the Mockdown root for the given path.

        Path can be a string or a Path object. The return value will always be a string.
        """
        if isinstance(path, basestring):
            path = pathlib.Path(path)

        rpath = path.relative_to(self.root)
        return str(rpath)

    def exists(self, path):
        """Returns True if the given path relative to Mockdown root exists.
        """
        return pathlib.Path(self.root, path).exists()

    def is_dir(self, path):
        return pathlib.Path(self.root, path).is_dir()

    def _with_suffix(self, path, suffix):
        """Returns a new path as string after replacing the suffix in the path with given suffix.
        """
        return str(pathlib.Path(path).with_suffix(suffix))
