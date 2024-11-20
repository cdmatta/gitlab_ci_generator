import pytest

from gitlab_ci_generator.yaml_utils import yaml_dump, yaml_safe_load


def test_yaml_safe_load_sysexits_on_missing_file(tmp_path):
    unknown = tmp_path / "unknown.yml"
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        yaml_safe_load(unknown)
    assert pytest_wrapped_e.type == SystemExit


def test_yaml_safe_load_sysexits_on_empty_file(tmp_path):
    empty = tmp_path / "empty.yml"
    empty.write_text("", encoding="utf-8")
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        yaml_safe_load(empty)
    assert pytest_wrapped_e.type == SystemExit


def test_yaml_safe_load_sysexits_on_invalid_yml_file(tmp_path):
    jinja_text = """
{% if LEVEL2_ENV == 'cn' %}
image: $ECR_CN_REGISTRY/{{ BASE_DOCKER_IMAGE }}
{% else %}
"""
    invalid = tmp_path / "invalid.yml"
    invalid.write_text(jinja_text, encoding="utf-8")
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        yaml_safe_load(invalid)
    assert pytest_wrapped_e.type == SystemExit


def test_yaml_safe_loads_valid_yaml(tmp_path):
    valid = tmp_path / "valid.yml"
    valid.write_text("hello: world", encoding="utf-8")
    assert yaml_safe_load(valid) == {"hello": "world"}


def test_yaml_dump_for_bad_indentation():
    foo = {
        "name": "foo",
        "my_list": [{"foo": "test", "bar": "test2"}, {"foo": "test3", "bar": "test4"}],
        "hello": "world",
    }
    expected = """
name: foo
my_list:
  - foo: test
    bar: test2
  - foo: test3
    bar: test4
hello: world
""".lstrip()
    assert yaml_dump(foo) == expected


def test_yaml_dump_for_width():
    """
    This is required as some shell commands can be long.
    Thus we have kept a safe limit of 200 characters.
    """
    long_string = "abcdefghijklmnopqrstuvwxyz" * 7
    foo = {
        "script": [f"echo {long_string}"],
    }
    expected = """
script:
  - echo abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz
""".lstrip()
    assert yaml_dump(foo) == expected
