from pathlib import Path
from antidote import world, instanceOf
from src.file_processor import FileProcessor, Task


def test_process_file(earn_file: Path):
    extension = earn_file.name.rsplit(".", maxsplit=1)[-1]
    processor = world[instanceOf(FileProcessor).single(qualified_by=extension)]

    tasks = processor.get_tasks_from_file(earn_file)
    assert all([isinstance(item, Task) for item in tasks])
