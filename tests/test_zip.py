import os
import sys
from unittest.mock import patch

from pyfakefs.fake_filesystem import FakeFilesystem

from src.commands.def_zip import zip

# Добавляем путь к src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_zip_empty_args():

    with patch('typer.echo') as mock_echo:

        zip([])


        mock_echo.assert_called_with("Укажите имя файла или папки для архивирования")


def test_zip_right_args(fs: FakeFilesystem):

    fs.create_dir("test_dir")

    zip(["test_dir"])

    files = os.listdir('.')

    finded = False

    for file in files:
        if "test_dir.zip" in file:
            finded = True
    assert finded


def test_zip_FileNotFoundError(fs: FakeFilesystem):

    with patch('src.commands.def_zip.logger') as mock_logger:

        zip(["test_dir"])

        error = str(mock_logger.error.call_args)

        assert "Файл не найден" in error


def test_zip_PermissionError(fs: FakeFilesystem):

    fs.create_dir("test_dir")

    with patch('src.commands.def_zip.logger') as mock_logger:
        with patch('shutil.make_archive', side_effect=PermissionError("Отказано в доступе")):
            zip(["test_dir"])

            error = str(mock_logger.error.call_args)

            assert "Отказано в доступе" in error


def test_zip_Exception(fs: FakeFilesystem):

    fs.create_dir("test_dir")

    with patch('src.commands.def_zip.logger') as mock_logger:
        with patch('shutil.make_archive', side_effect=Exception("Произошла непредвиденная ошибка")):
            zip(["test_dir"])

            error = str(mock_logger.error.call_args)

            assert "Произошла непредвиденная ошибка" in error




# python -m pytest tests/test_zip.py -v
# python -m pytest --cov=src --cov-report=term-missing
