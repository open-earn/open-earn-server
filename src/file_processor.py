from abc import abstractmethod
from antidote import interface, implements, injectable
from pathlib import Path
from .dto import Task, EarnFile
import yaml


@injectable
@interface
class FileProcessor:
    @abstractmethod
    def __parse_file(self, path: Path) -> EarnFile:
        ...

    @abstractmethod
    def get_tasks_from_file(self, path: Path) -> list[Task]:
        ...


@implements(FileProcessor).when(qualified_by=["yaml", "yml"])
class YamlFileProcessorImpl(FileProcessor):
    def __parse_file(self, path: Path) -> EarnFile:
        file_content = path.read_text()
        content_dict = yaml.safe_load(file_content)
        return EarnFile.parse_obj(content_dict)

    def get_tasks_from_file(self, path: Path) -> list[Task]:
        return self.__parse_file(path).tasks


@implements(FileProcessor).when(qualified_by=["json"])
class JsonFileProcessorImpl(FileProcessor):
    def __parse_file(self, path: Path) -> EarnFile:
        file_content = path.read_bytes()
        return EarnFile.parse_raw(file_content)

    def get_tasks_from_file(self, path: Path) -> list[Task]:
        return self.__parse_file(path).tasks
