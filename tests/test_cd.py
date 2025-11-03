import os
import sys
from unittest.mock import patch

from pyfakefs.fake_filesystem import FakeFilesystem

from src.commands.def_cd import cd

# Добавляем путь к src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def test_cd_NotADirectoryError(fs: FakeFilesystem):
    fs.create_file("test_file.txt")
    with patch('src.commands.def_cd.logger') as mock_logger:
        cd(["test_file.txt"])
        error = str(mock_logger.error.call_args)
        assert "Попытка применения cd не для директории" in error


def test_cd_right_args(fs: FakeFilesystem):
    fs.create_dir("test_dir1")
    fs.create_dir("test_dir1/test_dir2")
    old_dir = os.getcwd()
    cd(["test_dir1/test_dir2"])
    new_dir = os.getcwd()
    assert (old_dir != new_dir) and ("test_dir2" in new_dir)


"""def test_cd_FileNotFoundError(fs: FakeFilesystem):
    with patch('src.commands.def_cd.logger') as mock_logger:
        cd(["test_dir"])
        error = str(mock_logger.error.call_args)
        assert "Произошла ошибка. Папка не найдена" in error"""


def test_ls_OSError(fs: FakeFilesystem):
    fs.create_dir("test_dir")
    with patch('src.commands.def_cd.logger') as mock_logger:
        with patch('os.chdir', side_effect=OSError("Ошибка операционной системы")):
            cd(["test_dir"])
            error = str(mock_logger.error.call_args)
            assert "Ошибка операционной системы" in error


def test_ls_Exception(fs: FakeFilesystem):
    fs.create_dir("test_dir")
    with patch('src.commands.def_cd.logger') as mock_logger:
        with patch('os.chdir', side_effect=Exception("Ошибка операционной системы")):
            cd(["test_dir"])
            error = str(mock_logger.error.call_args)
            assert "Ошибка операционной системы" in error


def test_cd_more_than_one_arg(fs: FakeFilesystem):
    fs.create_dir("test_dir1")
    fs.create_dir("test_dir2")
    with patch('src.commands.def_cd.logger') as mock_logger:
        cd(["test_dir1", "test_dir2"])
        error = str(mock_logger.error.call_args)
        assert "Произошла ошибка. Слишком много аргументов" in error


def test_cd_to_home(fs: FakeFilesystem):
    fs.create_dir("test_dir")
    home_dir = os.path.expanduser("~") #Запомнили домашнуюю директорию

    cd(["~"]) #Вернулись в домашнюю
    dir1 = os.getcwd()
    cd([""]) #Вернулись в домашнюю
    dir2 = os.getcwd()
    assert (home_dir == dir1 == dir2 == os.getcwd())



# python -m pytest tests/test_cd.py -v
# python -m pytest --cov=src --cov-report=term-missing
