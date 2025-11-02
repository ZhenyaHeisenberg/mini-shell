import os
import sys
from unittest.mock import patch

from pyfakefs.fake_filesystem import FakeFilesystem

from src.commands.def_rm import rm

# Добавляем путь к src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_rm_empty_args():
    with patch('typer.echo') as mock_echo:
        rm([])
        mock_echo.assert_called_with("Укажите имя файла или папки для удаления")




def test_rm_right_args_dir(fs: FakeFilesystem): #удаление каталога
    fs.create_dir("test_dir")
    fs.create_file("test_dir/file1.txt")
    with patch('builtins.input', return_value='y'): #вместо input() сразу возвращаем значение 'y'
        rm(["-r", "test_dir"])
        files = os.listdir('.')
        finded = False
        for file in files:
            if "test_dir" in file:
                finded = True
        assert not finded #Директории не должно быть


def test_rm_right_args_file(fs: FakeFilesystem): #удаление файла
    fs.create_file("test_file.txt")
    rm(["test_file.txt"])
    files = os.listdir('.')
    finded = False
    for file in files:
        if "test_dir" in file:
            finded = True
    assert not finded #Директории не должно быть


def test_rm_FileNotFoundError():
    with patch('src.commands.def_rm.logger') as mock_logger: #вместо реального удаления записываем потенциальный результат
        rm(["test_file.txt"])
        error = str(mock_logger.error.call_args)
        assert "Не удается найти указанный файл" in error


def test_rm_PermissionError(fs: FakeFilesystem):
    fs.create_dir("test_dir")
    with patch('src.commands.def_rm.logger') as mock_logger:
        with patch('os.remove', side_effect=PermissionError("Отказано в доступе")):
            rm(["test_dir"])
            error = str(mock_logger.error.call_args)
            assert "Отказано в доступе" in error


def test_rm_Exception_dir(fs: FakeFilesystem):

    fs.create_dir("test_dir")

    with patch('src.commands.def_rm.logger') as mock_logger:
        with patch('shutil.rmtree', side_effect=Exception("Произошла непредвиденная ошибка")):
            rm(["-r", "test_dir"])

            error = str(mock_logger.error.call_args)

            assert "Произошла непредвиденная ошибка" in error





# python -m pytest tests/test_rm.py -v
# python -m pytest --cov=src --cov-report=term-missing
