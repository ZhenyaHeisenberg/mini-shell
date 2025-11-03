import os
import sys
from unittest.mock import patch

from pyfakefs.fake_filesystem import FakeFilesystem

from src.commands.def_mv import mv

# Добавляем путь к src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_mv_more_then_two_args(fs: FakeFilesystem):
    with patch('src.commands.def_mv.logger') as mock_logger:
        fs.create_file("test_file.txt")
        fs.create_dir("test_dir1")
        fs.create_dir("test_dir2")
        mv(["test_file.txt", "test_dir1", "test_dir2"])
        error = str(mock_logger.error.call_args)
        assert "ERROR: Неверное колличество аргументов" in error


def test_mv_less_then_two_args(fs: FakeFilesystem):
    with patch('src.commands.def_mv.logger') as mock_logger:
        fs.create_file("test_file.txt")
        mv(["test_file.txt"])
        error = str(mock_logger.error.call_args)
        assert "ERROR: Неверное колличество аргументов" in error


def test_mv_from_None(fs: FakeFilesystem):
    fs.create_dir("test_dir")
    with patch('src.commands.def_mv.logger') as mock_logger:
        mv(["test_file.txt", "test_dir"])
        error = str(mock_logger.error.call_args)
        assert "ERROR: 'test_file.txt' не существует" in error


def test_mv_to_None(fs: FakeFilesystem): #Переименование
    fs.create_dir("test_dir")
    with patch('src.commands.def_mv.logger') as mock_logger:
        mv(["test_dir", "test_new_dir"])
        error = str(mock_logger.info.call_args)
        assert "Файл переименован: 'test_dir' -> 'test_new_dir'" in error


def test_mv_PermissionError(fs: FakeFilesystem):
    fs.create_dir("test_dir1")
    fs.create_dir("test_dir2")
    with patch('src.commands.def_mv.logger') as mock_logger:
        with patch('os.rename', side_effect=PermissionError("Нет прав доступа")):
            mv(["test_dir1", "test_dir2"])
            error = str(mock_logger.error.call_args)
            assert "Нет прав доступа" in error



def test_mvOSError(fs: FakeFilesystem):
    fs.create_dir("test_dir1")
    fs.create_dir("test_dir2")
    with patch('src.commands.def_mv.logger') as mock_logger:
        with patch('os.rename', side_effect=OSError("Ошибка операционной системы")):
            mv(["test_dir1", "test_dir2"])
            error = str(mock_logger.error.call_args)
            assert "Ошибка операционной системы" in error


def test_Exception(fs: FakeFilesystem):
    fs.create_dir("test_dir1")
    fs.create_dir("test_dir2")
    with patch('src.commands.def_mv.logger') as mock_logger:
        with patch('os.rename', side_effect=Exception("Ошибка операционной системы")):
            mv(["test_dir1", "test_dir2"])
            error = str(mock_logger.error.call_args)
            assert "Произошла непредвиденная ошибка" in error


# python -m pytest tests/test_mv.py -v
# python -m pytest --cov=src --cov-report=term-missing



