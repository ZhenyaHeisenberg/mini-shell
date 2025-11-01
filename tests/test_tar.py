import os
import sys
from unittest.mock import patch

from pyfakefs.fake_filesystem import FakeFilesystem

from src.commands.def_tar import tar

# Добавляем путь к src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_tar_empty_args():

    with patch('typer.echo') as mock_echo:

        tar([])


        mock_echo.assert_called_with("Укажите имя файла или папки для архивирования")


def test_tar_right_args(fs: FakeFilesystem):

    fs.create_dir("test_dir")
    fs.create_file("test_dir/file1.txt")

    tar(["test_dir"])

    assert os.path.exists("test_dir.tar")


def test_tar_FileNotFoundError(fs: FakeFilesystem):

    with patch('src.commands.def_tar.logger') as mock_logger:

        tar(["test_dir"])

        error = str(mock_logger.error.call_args)

        assert "Файл не найден" in error


def test_tar_PermissionError(fs: FakeFilesystem):

    fs.create_dir("test_dir")

    with patch('src.commands.def_tar.logger') as mock_logger:
        with patch('shutil.make_archive', side_effect=PermissionError("Отказано в доступе")):
            tar(["test_dir"])

            error = str(mock_logger.error.call_args)

            assert "Отказано в доступе" in error


def test_tar_Exception(fs: FakeFilesystem):

    fs.create_dir("test_dir")

    with patch('src.commands.def_tar.logger') as mock_logger:
        with patch('shutil.make_archive', side_effect=Exception("Произошла непредвиденная ошибка")):
            tar(["test_dir"])

            error = str(mock_logger.error.call_args)

            assert "Произошла непредвиденная ошибка" in error




# python -m pytest tests/test_tar.py -v
# python -m pytest --cov=src --cov-report=term-missing
