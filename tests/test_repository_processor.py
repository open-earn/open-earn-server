from pathlib import Path


def test_get_project(earn_file):
    assert isinstance(earn_file, Path)
