import os
from pathlib import Path
from unittest.mock import patch

from _pytest.fixtures import fixture

from argus.backend.cli import sync_models
from argus.backend.db import ScyllaCluster
from argus.backend.service.client_service import ClientService
from argus.backend.service.release_manager import ReleaseManagerService
from argus.backend.util.config import Config
import logging
os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = '1'
logging.getLogger('cassandra').setLevel(logging.WARNING)
logging.getLogger('cassandra.connection').setLevel(logging.WARNING)
logging.getLogger('cassandra.pool').setLevel(logging.WARNING)
logging.getLogger('cassandra.cluster').setLevel(logging.WARNING)

def truncate_all_tables(session):
    for table in session.cluster.metadata.keyspaces[session.keyspace].tables:
        session.execute(f"TRUNCATE {table}")


@fixture(autouse=True, scope='session')
def argus_db():
    Config.CONFIG_PATHS = [Path(__file__).parent / "argus_web.test.yaml"]
    config = Config.load_yaml_config()
    database = ScyllaCluster.get(config)
    session = database.cluster.connect(keyspace=config["SCYLLA_KEYSPACE_NAME"])
    ScyllaCluster.get_session = lambda: session  # monkey patching to escape need for flask app context

    sync_models()
    truncate_all_tables(database.session)
    yield database
    database.shutdown()


@fixture(autouse=True, scope='session')
def release_manager_service(argus_db):
    return ReleaseManagerService()

@fixture(autouse=True, scope='session')
def client_service(argus_db):
    return ClientService()
