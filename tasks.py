import pathlib
import subprocess
from importlib.metadata import version

from invoke import task

ROOT = pathlib.Path(__file__).parent.resolve().as_posix()
VERSION = version("gitlab_ci_generator")


@task
def clean(context):
    cmd = [
        "rm",
        "-rf",
        f"{ROOT}/dist",
        f"{ROOT}/build",
        f"{ROOT}/*.egg-info",
        f"{ROOT}/.env",
        f"{ROOT}/htmlcov",
        f"{ROOT}/results",
        f"{ROOT}/.coverage",
        f"{ROOT}/.pytest_cache",
        f"{ROOT}/pytest.log",
    ]
    subprocess.run(" ".join(cmd), shell=True, check=False)


@task
def gen(context):
    cmd = [
        "gitlab_ci_generator",
    ]
    context.run(" ".join(cmd), pty=True)
