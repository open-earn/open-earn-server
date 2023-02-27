import pytest
import shutil
from src.repository_processor import RepositoryProcessor, RepositoryQualifier
from antidote import world, instanceOf
from pathlib import Path

EARN_SAMPLES_PROJECTS = [
    "https://github.com/open-earn/example-calculator",
]
EARN_SAMPLES_PROJECTS_IDS = [
    url.rsplit("/", maxsplit=1)[-1] for url in EARN_SAMPLES_PROJECTS
]


@pytest.fixture(params=EARN_SAMPLES_PROJECTS, ids=EARN_SAMPLES_PROJECTS_IDS)
def project_url(request) -> str:
    return request.param


@pytest.fixture
def earn_file(project_url: str) -> Path:
    if "github" in project_url:
        instance = world[
            instanceOf(RepositoryProcessor).single(
                qualified_by=RepositoryQualifier.github
            )
        ]
    else:
        raise Exception()

    file = instance.get_earn_file_from_url(project_url)
    yield file

    file_folder = file.parent
    shutil.rmtree(file_folder.absolute().as_posix(), ignore_errors=True)
