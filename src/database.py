from abc import abstractmethod
from pydantic import HttpUrl
from typing import Iterable
from antidote import injectable, implements, interface
from .dto import Task


@injectable
@interface
class Database:
    @abstractmethod
    def add_repository(self, repository: HttpUrl, tasks: list[Task]) -> None:
        ...

    @abstractmethod
    def get_tasks_iter(self, repository: HttpUrl) -> Iterable[Task]:
        ...

    @abstractmethod
    def get_task(self, repository: HttpUrl, task_name: str) -> Task:
        ...

    @abstractmethod
    def remove_repository(self, repository: HttpUrl) -> None:
        ...

    @abstractmethod
    def remove_task(self, repository: HttpUrl, task_name: str) -> None:
        ...


@implements(Database).as_default
class DictDatabaseImpl(Database):
    __tasks: dict[HttpUrl, list[Task]] = {}

    def add_repository(self, repository: HttpUrl, tasks: list[Task]) -> None:
        self.__tasks[repository] = tasks

    def get_tasks_iter(self, repository: HttpUrl) -> Iterable[Task]:
        for task in self.__tasks[repository]:
            yield task

    def get_task(self, repository: HttpUrl, task_name: str) -> Task:
        for task in self.get_tasks_iter(repository):
            if task.name == task_name:
                return task

        raise ValueError("Task not found by name: " + task_name)

    def remove_repository(self, repository: HttpUrl) -> None:
        self.__tasks.pop(repository)

    def remove_task(self, repository: HttpUrl, task_name: str) -> None:
        task_index = None
        for index, task in enumerate(self.get_tasks_iter(repository)):
            if task.name == task_name:
                task_index = index
                break

        if not task_index:
            raise ValueError("Task not found by name: " + task_name)

        self.__tasks[repository].pop(task_index)
