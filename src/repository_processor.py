from abc import abstractmethod
from antidote import interface, implements, injectable, world
from pathlib import Path
from pydantic import HttpUrl
from pydantic.dataclasses import dataclass
import shutil
from git.repo import Repo
from enum import Enum, auto


class RepositoryQualifier(Enum):
    github = auto()


@injectable
@dataclass(frozen=True)
class RepositorySettings:
    earn_filename: str = "earn"


@injectable
@interface
class RepositoryProcessor:
    @abstractmethod
    def get_earn_file_from_url(self, url: HttpUrl) -> Path:
        ...

    @abstractmethod
    def __get_earn_file_path(self, folder: Path) -> Path:
        ...


@implements(RepositoryProcessor).when(qualified_by=RepositoryQualifier.github)
class GithubRepositoryProcessorImpl(RepositoryProcessor):
    __root_folder = Path(".github-projects")

    def __init__(
        self,
        *,
        earn_filename: str = world[RepositorySettings].earn_filename,
    ) -> None:
        self.__root_folder.mkdir(parents=True, exist_ok=True)
        self.__earn_filename = earn_filename

    def get_earn_file_from_url(self, url: HttpUrl, *, override: bool = True) -> Path:
        name = url.rsplit("/", maxsplit=1)[-1]
        project_folder = self.__root_folder.joinpath(name)

        if project_folder.exists() and override:
            shutil.rmtree(project_folder.absolute().as_posix())
        Repo.clone_from(
            url,
            self.__root_folder.joinpath(name).absolute().as_posix(),
        )

        return self.__get_earn_file_path(project_folder)

    def __get_earn_file_path(self, folder: Path) -> Path:
        for file in folder.glob("earn.*"):
            if file.is_file():
                filename = file.name.rsplit(".", maxsplit=1)[0]
                if filename == self.__earn_filename:
                    return file

        raise FileNotFoundError("Earn file not found!")
