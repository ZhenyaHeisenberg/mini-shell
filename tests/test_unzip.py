import os
import sys
from unittest.mock import patch

from pyfakefs.fake_filesystem import FakeFilesystem

from src.commands.def_unzip import unzip

# Добавляем путь к src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_unzip_not_a_zip(fs: FakeFilesystem):

    fs.create_dir("test_dir")


    with patch('typer.echo') as mock_echo:

        unzip(["test_dir"])


        mock_echo.assert_called_with("Распаковка неархива невозможна")



"""def test_unzip_right_args(fs: FakeFilesystem):

    fs.create_dir("test_dir")


    with fs.open("test_dir.zip", 'wb') as f:

        unzip([f])


        finded = False

        for file in f:
            if "test_dir" in file and os.path.isdir(file):
                finded = True
        assert finded"""







def test_unzip_FileNotFoundError(fs: FakeFilesystem):

    fs.create_dir("test_dir")

    with patch('src.commands.def_unzip.logger') as mock_logger:
        with patch('shutil.unpack_archive', side_effect=FileNotFoundError("Файл не найден")):
            unzip(["test_dir.zip"])

            error = str(mock_logger.error.call_args)

            assert "Файл не найден" in error


def test_unzip_PermissionError(fs: FakeFilesystem):

    fs.create_dir("test_dir")

    with patch('src.commands.def_unzip.logger') as mock_logger:
        with patch('shutil.unpack_archive', side_effect=PermissionError("Отказано в доступе")):
            unzip(["test_dir.zip"])

            error = str(mock_logger.error.call_args)

            assert "Отказано в доступе" in error


def test_unzip_Exception(fs: FakeFilesystem):

    fs.create_dir("test_dir")

    with patch('src.commands.def_unzip.logger') as mock_logger:
        with patch('shutil.unpack_archive', side_effect=Exception("Произошла непредвиденная ошибка")):
            unzip(["test_dir.zip"])

            error = str(mock_logger.error.call_args)

            assert "Произошла непредвиденная ошибка" in error




# python -m pytest tests/test_unzip.py -v
# python -m pytest --cov=src --cov-report=term-missing
