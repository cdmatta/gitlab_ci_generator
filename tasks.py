import pathlib
import subprocess
from importlib.metadata import version

from invoke import task

ROOT = pathlib.Path(__file__).parent.resolve().as_posix()
VERSION = version("gitlab_ci_generator")


gitlab_vars = {
    # These are available in Gitlab CI/CD environment
    "CI_COMMIT_REF_NAME": "main",
    "CI_COMMIT_SHA": "45aacd9b",
    "CI_COMMIT_MESSAGE": "feat: work in progress",
    "CI_PIPELINE_SOURCE": "commit",
}


def write_dict_to_env_file():
    txt = "\n".join("%s=%s" % (str(k), str(v)) for (k, v) in gitlab_vars.items())
    with open(f"{ROOT}/.env", "w") as f:
        f.write(txt)


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
        f"{ROOT}/generated-gitlabci.yml",
    ]
    subprocess.run(" ".join(cmd), shell=True, check=False)


@task(pre=[clean])
def tests(context):
    cmd = [
        "pytest",
        f"{ROOT}/tests",
    ]
    subprocess.run(" ".join(cmd), shell=True, check=True)


@task
def local_env_main(context):
    write_dict_to_env_file()


@task
def local_env_merge_request(context):
    gitlab_vars["CI_MERGE_REQUEST_ID"] = "123456"
    write_dict_to_env_file()


@task
def local_env_feature(context):
    gitlab_vars["CI_COMMIT_REF_NAME"] = "feature/some-feature"
    write_dict_to_env_file()


@task
def local_env_bugfix(context):
    gitlab_vars["CI_COMMIT_REF_NAME"] = "bugfix/some-bug"
    write_dict_to_env_file()


@task
def local_env_hotfix(context):
    gitlab_vars["CI_COMMIT_REF_NAME"] = "hotfix/some-hotfix"
    write_dict_to_env_file()


@task
def local_env_tag(context):
    gitlab_vars["CI_COMMIT_TAG"] = "v1.0.0"
    write_dict_to_env_file()


@task
def gen(context, verbose=False, color=False):
    env_file = f"{ROOT}/.env"
    if not pathlib.Path(env_file).exists():
        print("Generating .env file for pipelineType: main")
        context.run("invoke local-env-main")

    cmd = [
        "gitlab_ci_generator",
        "-f",
        f"{ROOT}/config.yml",
        "-v" if verbose else "",
        "-c" if color else "",
    ]
    context.run(" ".join(cmd), pty=True)
