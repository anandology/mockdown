# -*- coding: utf-8 -*-
from mockdown.mockdown import Mockdown

class TestMockdown:
    def test_exists(self, tmpdir):
        m = Mockdown(tmpdir.strpath)
        assert m.exists("a.txt") is False

        tmpdir.join("a.txt").write("hello")
        assert m.exists("a.txt") is True

    def read_yaml_file(self, tmpdir):
        m = Mockdown(tmpdir.strpath)
        assert m.read_yaml_file("a.yml") == {}

        tmpdir.join("a.yml").write("name: Alice")
        assert m.read_yaml_file("a.yml") == {"name": "Alice"}

    def test_read_arguments(self, tmpdir):
        m = Mockdown(tmpdir.strpath)
        assert m.read_arguments("a.html") == {}

        tmpdir.join("a.yml").write("name: Alice")
        assert m.read_arguments("a.html") == {"name": "Alice"}

    def test_render_template(self, tmpdir):
        m = Mockdown(tmpdir.strpath)
        tmpdir.join("a.html").write("Hello {{name}}")
        tmpdir.join("a.yml").write("name: Alice")
        assert m.render_template("a.html") == "Hello Alice"

    def test_fake(self, tmpdir, monkeypatch):
        m = Mockdown(tmpdir.strpath)

        class FakeFake:
            def name(self):
                return "fake-name"
            def email(self):
                return "fake-email"

        monkeypatch.setattr(m, "get_fake", lambda filename: FakeFake())
        tmpdir.join("a.yml").write("name: {{fake.name()}}")
        assert m.read_yaml_file("a.yml") == {"name": "fake-name"}

    def test_includes(self, tmpdir):
        m = Mockdown(tmpdir.strpath)
        tmpdir.join("a.yml").write("x: 1\ny: 2\n")
        tmpdir.join("b.yml").write(
            "z: 3\n" +
            "_includes:\n" +
            "  - 'a.yml'\n")
        assert m.read_yaml_file("b.yml") == {"x": 1, "y": 2, "z": 3}

    def test_include_overwrites(self, tmpdir):
        m = Mockdown(tmpdir.strpath)
        tmpdir.join("a.yml").write("x: 1\ny: 2\n")
        tmpdir.join("b.yml").write(
            "x: 3\n" +
            "_includes:\n" +
            "  - 'a.yml'\n")
        assert m.read_yaml_file("b.yml") == {"x": 3, "y": 2}

