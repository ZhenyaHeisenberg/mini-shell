import os
import sys
from unittest.mock import patch

from pyfakefs.fake_filesystem import FakeFilesystem

from src.commands.def_cat import cat

# Добавляем путь к src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_cat_empty_args():
    with patch('src.commands.def_cat.logger') as mock_logger:
        cat([])
        error = str(mock_logger.error.call_args)
        assert "Имя файла не указано" in error


def test_cat_dir(fs: FakeFilesystem):
    fs.create_dir("test_dir")
    with patch('src.commands.def_cat.logger') as mock_logger:
        cat(["test_dir"])
        error = str(mock_logger.error.call_args)
        assert "Попытка применения cat директории" in error


def test_cat_file(fs: FakeFilesystem):
    fs.create_file("test_file.txt", contents="test text")
    with patch('src.commands.def_cat.typer.echo') as mock_echo:
        cat(["test_file.txt"])
        output = str(mock_echo.call_args_list)
        assert "test text" in output


def test_cat_FileNotFoundError():
    with patch('src.commands.def_cat.logger') as mock_logger:
        cat(["test_dir"])
        error = str(mock_logger.error.call_args)
        assert "Произошла ошибка. Файл не найден" in error


def test_cat_PermissionError(fs: FakeFilesystem):
    fs.create_file("test_file.txt", contents="test text", st_mode=0o000)
    with patch('src.commands.def_cat.logger') as mock_logger:
        cat(["test_file.txt"])
        error = str(mock_logger.error.call_args)
        assert "Нет прав доступа" in error






# python -m pytest tests/test_cat.py -v
# python -m pytest --cov=src --cov-report=term-missing
