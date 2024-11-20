import logging
import os
import re
from enum import Enum


class PipelineType(Enum):
    Main = "main"
    Feature = "feature"
    Hotfix = "hotfix"
    Bugfix = "bugfix"
    MergeRequest = "merge_request"
    Tag = "tag"


# https://docs.gitlab.com/ee/ci/variables/predefined_variables.html
class GitlabVariables:
    log = logging.getLogger(__name__)
    # The full commit message
    ci_commit_message: str
    # The branch or tag name for which project is built.
    ci_commit_ref_name: str
    # The commit revision the project is built for.
    ci_commit_sha: str
    # The commit tag name. Available only in pipelines for tags.
    ci_commit_tag: str
    # How the pipeline was triggered. The value can be one of
    # https://docs.gitlab.com/ee/ci/jobs/job_rules.html#ci_pipeline_source-predefined-variable
    ci_pipeline_source: str

    # Predefined variables for merge request pipelines
    ci_merge_request_id: str

    pipeline_type: PipelineType

    def __init__(self):
        self.ci_commit_message = os.environ.get("CI_COMMIT_MESSAGE")
        self.ci_commit_ref_name = os.environ.get("CI_COMMIT_REF_NAME")
        self.ci_commit_sha = os.environ.get("CI_COMMIT_SHA")
        self.ci_commit_tag = os.environ.get("CI_COMMIT_TAG")
        self.ci_pipeline_source = os.environ.get("CI_PIPELINE_SOURCE")

        self.ci_merge_request_id = os.environ.get("CI_MERGE_REQUEST_ID")
        self.pipeline_type = self.infer_pipeline_type()
        self.log.debug(f"gitlab vars {self.__dict__}")

    def infer_pipeline_type(self) -> PipelineType:
        if self.ci_commit_tag:
            return PipelineType.Tag
        if self.ci_merge_request_id:
            return PipelineType.MergeRequest

        branch_prefix_pipeline_type = {
            r"^(release/|main|master)": PipelineType.Main,
            r"^feature/": PipelineType.Feature,
            r"^hotfix/": PipelineType.Hotfix,
            r"^bugfix/": PipelineType.Bugfix,
        }
        for regex, pipe_type in branch_prefix_pipeline_type.items():
            if re.match(regex, self.ci_commit_ref_name):
                return pipe_type
        raise ValueError(f"could not infer pipeline type for {self.ci_commit_ref_name}")
