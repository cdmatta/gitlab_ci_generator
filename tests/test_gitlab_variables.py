import pytest

from gitlab_ci_generator.gitlab_variables import GitlabVariables, PipelineType


@pytest.mark.parametrize(
    "env,expected_pipeline_type",
    [
        ({}, PipelineType.Main),
        ({"CI_MERGE_REQUEST_ID": "123456"}, PipelineType.MergeRequest),
        ({"CI_COMMIT_REF_NAME": "feature/some-feature"}, PipelineType.Feature),
        ({"CI_COMMIT_REF_NAME": "bugfix/some-bug"}, PipelineType.Bugfix),
        ({"CI_COMMIT_REF_NAME": "hotfix/some-hotfix"}, PipelineType.Hotfix),
        ({"CI_COMMIT_TAG": "v1.0.0"}, PipelineType.Tag),
    ],
)
def test_gitlab_variables_object_initialized_correctly(
    monkeypatch, env: dict[str, str], expected_pipeline_type: PipelineType
):
    basic_env = {
        "CI_COMMIT_REF_NAME": "main",
        "CI_COMMIT_SHA": "45aacd9b",
        "CI_COMMIT_MESSAGE": "feat: work in progress",
        "CI_PIPELINE_SOURCE": "commit",
    }
    basic_env.update(env)

    for k, v in basic_env.items():
        monkeypatch.setenv(k, v)
    gl = GitlabVariables()
    assert gl.infer_pipeline_type() == expected_pipeline_type


def test_gitlab_variables_initialized_fails_for_unknown_branch_prefix(monkeypatch):
    env = {
        "CI_COMMIT_REF_NAME": "draft/some-draft",
        "CI_COMMIT_SHA": "45aacd9b",
        "CI_COMMIT_MESSAGE": "feat: work in progress",
        "CI_PIPELINE_SOURCE": "commit",
    }
    for k, v in env.items():
        monkeypatch.setenv(k, v)
    with pytest.raises(ValueError) as pytest_wrapped_e:
        GitlabVariables()
    assert pytest_wrapped_e.type == ValueError
    assert "could not infer pipeline type for draft/some-draft" in str(pytest_wrapped_e.value)
