import logging
import uuid
from dataclasses import asdict
from typing import Optional, Dict

from _pytest.fixtures import fixture

from argus.backend.plugins.sct.testrun import SCTTestRunSubmissionRequest
from argus.client.generic_result import GenericResultTable, ColumnMetadata, ResultType, ValidationRule

LOGGER = logging.getLogger(__name__)

@fixture(autouse=True, scope='session')
def release(release_manager_service):
    return release_manager_service.create_release("best_results", "best_results", False)


@fixture(autouse=True, scope='session')
def group(release_manager_service, release):
    return release_manager_service.create_group("br_group", "best_results", build_system_id="best_results", release_id=str(release.id))

def get_fake_test_run(
    schema_version: str = "1.0.0",
    run_id: str = str(uuid.uuid4()),
    job_name: str = "default_job_name",
    job_url: str = "http://example.com",
    started_by: str = "default_user",
    commit_id: str = "default_commit_id",
    sct_config: dict | None = None,
    origin_url: str | None = None,
    branch_name: str | None = "main",
    runner_public_ip: str | None = None,
    runner_private_ip: str | None = None
) -> tuple[str, dict]:
    return "scylla-cluster-tests", asdict(SCTTestRunSubmissionRequest(
        schema_version=schema_version,
        run_id=run_id,
        job_name=job_name,
        job_url=job_url,
        started_by=started_by,
        commit_id=commit_id,
        sct_config=sct_config,
        origin_url=origin_url,
        branch_name=branch_name,
        runner_public_ip=runner_public_ip,
        runner_private_ip=runner_private_ip
    ))

class SampleTable(GenericResultTable):
    class Meta:
        name = "Test Table Name"
        description = "Test Table Description"
        Columns = [ColumnMetadata(name="float col name", unit="ms", type=ResultType.FLOAT, higher_is_better=False),
                   ColumnMetadata(name="int col name", unit="ms", type=ResultType.INTEGER, higher_is_better=False),
                   ColumnMetadata(name="duration col name", unit="s", type=ResultType.DURATION, higher_is_better=False),
                   ColumnMetadata(name="non tracked col name", unit="", type=ResultType.FLOAT),
                   ColumnMetadata(name="text col name", unit="", type=ResultType.TEXT),
                   ]
        ValidationRules = {"float col name": ValidationRule(best_abs=4),
                           "int col name": ValidationRule(best_pct=50, best_abs=5),
                           "duration col name": ValidationRule(fixed_limit=590)
                           }

def test_argus_tracks_best_result(release_manager_service, client_service, release, group):
    test = release_manager_service.create_test('track_best_result', 'track_best_result', 'track_best_result', 'track_best_result',
                                               group_id=str(group.id), release_id=str(release.id), plugin_name='sct')
    print(test)
    LOGGER.warning(f"available plugins: {client_service.PLUGINS}")
    client_service.submit_run(*get_fake_test_run())
    assert test
