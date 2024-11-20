import argparse
import logging

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

    global log
    log = logging.getLogger(__name__)
    log.info("todo...")


if __name__ == "__main__":
    main()
