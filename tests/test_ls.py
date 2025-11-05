import os
import sys
from unittest.mock import patch

from pyfakefs.fake_filesystem import FakeFilesystem

from src.commands.def_ls import ls

# Добавляем путь к src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))



def test_ls_FileNotFoundError():
    with patch('src.commands.def_ls.logger') as mock_logger:
        ls(["test_dir"])
        error = str(mock_logger.error.call_args)
        assert "Произошла ошибка. Папка не найдена" in error


def test_ls_meta_FileNotFoundError():
    with patch('src.commands.def_ls.logger') as mock_logger:
        ls(["-l", "test_dir"])
        error = str(mock_logger.error.call_args)
        assert "Произошла ошибка. Папка не найдена" in error


def test_ls_NotADirectoryError(fs: FakeFilesystem):
    fs.create_file("test_dir")
    with patch('src.commands.def_ls.logger') as mock_logger:
        ls(["test_dir"])
        error = str(mock_logger.error.call_args)
        assert "Применение ls к файлу" in error


def test_ls_meta_NotADirectoryError(fs: FakeFilesystem):
    fs.create_file("test_dir")
    with patch('src.commands.def_ls.logger') as mock_logger:
        ls(["-l", "test_dir"])
        error = str(mock_logger.error.call_args)
        assert "Применение ls к файлу" in error

def test_ls_UserWarning(fs: FakeFilesystem):
    fs.create_dir("test_dir")
    with patch('src.commands.def_ls.logger') as mock_logger:
        with patch('os.listdir', side_effect=UserWarning("Ошибка пользователя")):
            ls(["test_dir"])
            error = str(mock_logger.error.call_args)
            assert "Ошибка пользователя" in error


def test_ls_meta_UserWarning(fs: FakeFilesystem):
    fs.create_dir("test_dir")
    with patch('src.commands.def_ls.logger') as mock_logger:
        with patch('os.listdir', side_effect=UserWarning("Ошибка пользователя")):
            ls(["-l", "test_dir"])
            error = str(mock_logger.error.call_args)
            assert "Ошибка пользователя" in error


def test_ls_OSError(fs: FakeFilesystem):
    fs.create_dir("test_dir")
    with patch('src.commands.def_ls.logger') as mock_logger:
        with patch('os.listdir', side_effect=OSError("Ошибка операционной системы")):
            ls(["test_dir"])
            error = str(mock_logger.error.call_args)
            assert "Ошибка операционной системы" in error


def test_ls_meta_OSError(fs: FakeFilesystem):
    fs.create_dir("test_dir")
    with patch('src.commands.def_ls.logger') as mock_logger:
        with patch('os.listdir', side_effect=OSError("Ошибка операционной системы")):
            ls(["-s", "test_dir"])
            error = str(mock_logger.error.call_args)
            assert "Ошибка операционной системы" in error


def test_ls_Exception(fs: FakeFilesystem):
    fs.create_dir("test_dir")
    with patch('src.commands.def_ls.logger') as mock_logger:
        with patch('os.listdir', side_effect=Exception("Произошла непредвиденная ошибка")):
            ls(["test_dir"])
            error = str(mock_logger.error.call_args)
            assert "Произошла непредвиденная ошибка" in error


def test_ls_meta_Exception(fs: FakeFilesystem):
    fs.create_dir("test_dir")
    with patch('src.commands.def_ls.logger') as mock_logger:
        with patch('os.listdir', side_effect=Exception("Произошла непредвиденная ошибка")):
            ls(["-l", "test_dir"])
            error = str(mock_logger.error.call_args)
            assert "Произошла непредвиденная ошибка" in error

# python -m pytest tests/test_ls.py -v
# python -m pytest --cov=src --cov-report=term-missing
