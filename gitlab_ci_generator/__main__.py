import argparse
import logging
import os

from dotenv import dotenv_values, load_dotenv

from .gitlab_variables import GitlabVariables
from .log_util import setup_logger

log = None


def main():
    parser = argparse.ArgumentParser(
        prog="gitlab_ci_generator",
        description="Generates .gitlab-ci.yml for dynamic pipelines",
    )

    parser.add_argument("-f", "--config-file", required=True, help="Pipeline configuration file")
    parser.add_argument(
        "-o",
        "--output-file",
        default="generated-gitlabci.yml",
        help="Output YAML file name (default: %(default)s)",
    )
    parser.add_argument("-e", "--external-config-dir", help="External configuration directory")
    parser.add_argument("-c", "--color", action="store_true", help="Colorize the output")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output for debugging")
    args = parser.parse_args()
    setup_logger(args.verbose, args.color)

    ci = True if os.environ.get("GITLAB_CI") else False

    global log
    log = logging.getLogger(__name__)
    log.info(
        f"generate pipline ci={ci} configFile={args.config_file} output={args.output_file} external-config-dir={args.external_config_dir}"
    )

    load_env_in_local_mode(ci)
    gl_vars = GitlabVariables()


def load_env_in_local_mode(ci: bool):
    if ci:
        return
    dot_env_path = os.path.join(os.getcwd(), ".env")
    env_vars = dotenv_values(dotenv_path=dot_env_path)
    load_dotenv(dotenv_path=dot_env_path, verbose=True)
    log.info(f"loading {len(env_vars.keys())} env variables from {dot_env_path}")
    log.debug(f"loaded to env {env_vars}")


if __name__ == "__main__":
    main()
