import logging

import yaml


def yaml_safe_load(file_path: str) -> dict:
    log = logging.getLogger(__name__)
    try:
        log.debug(f"loading yaml file {file_path}")
        with open(file_path, "r") as file:
            content = yaml.safe_load(file)
            if content is None:
                log.error(f"file {file_path} is empty or invalid.")
                exit(1)
            return content
    except Exception as e:
        log.error(f"Failed to load {file_path}: " + str(e))
        exit(1)


# https://stackoverflow.com/questions/25108581/python-yaml-dump-bad-indentation
class FixIndentationDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(FixIndentationDumper, self).increase_indent(flow, False)


def yaml_dump(obj: dict) -> str:
    return yaml.dump(obj, Dumper=FixIndentationDumper, default_flow_style=False, sort_keys=False, width=200)
