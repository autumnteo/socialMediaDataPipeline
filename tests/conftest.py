import os
from typing import Generator

import pytest

from socialMediaPipeline.db_manager import setup_db_schema, teardown_db_schema
from socialMediaPipeline.utils.db import DatabaseConnection


@pytest.fixture(scope='session', autouse=True)
def mock_social_posts_table(session_mocker) -> Generator:
    session_mocker.patch(
        "socialMediaPipeline.schema_manager.db_factory",
        return_value=DatabaseConnection(db_file="data/test.db"),
    )
    session_mocker.patch(
        "metadata.db_factory",
        return_value=DatabaseConnection(db_file="data/test.db"),
    )
    setup_db_schema()
    yield
    teardown_db_schema()
    os.remove("data/test.db")
