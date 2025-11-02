import os
import shutil
import sys
from unittest.mock import patch

from pyfakefs.fake_filesystem import FakeFilesystem

from src.commands.def_cp import cp

# Добавляем путь к src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_cp_empty_args():
    with patch("typer.echo") as mock_echo:
        cp([])

        mock_echo.assert_called_with("Использование: cp <исходный_файл> <целевой_файл>")


def test_cp_dir(fs: FakeFilesystem):
    fs.create_dir("test_dir")
    fs.create_file("test_dir/test_file.txt")
    fs.create_dir("test_new_dir")
    cp(["-r", "test_dir", "test_new_dir"])
    shutil.rmtree("test_dir")

    files_dir1 = os.listdir('test_new_dir')
    finded1 = False
    for file_dir1 in files_dir1:
        if "test_dir" in file_dir1:
            finded1 = True
    assert finded1 #В каталоге test_new_dir появился каталог test_new_dir/test_dir

    files_dir2 = os.listdir('test_new_dir/test_dir')
    finded2 = False
    for file_dir2 in files_dir2:
        if "test_file.txt" in file_dir2:
            finded2 = True
    assert finded2 #В каталоге test_new_dir/test_dir появился файл test_file.txt


def test_cp_file(fs: FakeFilesystem):
    fs.create_dir("test_dir")
    fs.create_file("test_dir/test_file1.txt", contents="test text")
    cp(["test_dir/test_file1.txt", "test_dir/test_file2.txt"])
    assert os.path.exists("test_dir/test_file2.txt")
    with open("test_dir/test_file2.txt") as text:
        assert text.read() == "test text"


def test_cp_recursive_to_file(fs: FakeFilesystem):
    fs.create_file("test_file_from")
    fs.create_dir("test_dir_from")
    fs.create_file("test_file_to")

    with patch('src.commands.def_cp.logger') as mock_logger:
        cp(["-r", "test_file_from", "test_file_to"])
        error = str(mock_logger.error.call_args)
        assert "Копирование в файл невозможно" in error

        cp(["-r", "test_dir_from", "test_file_to"])
        error = str(mock_logger.error.call_args)
        assert "Копирование в файл невозможно" in error


def test_cp_to_new(fs: FakeFilesystem):
    fs.create_file("test_file_from")
    fs.create_dir("test_dir_from")

    cp(["test_file_from", "test_file_to"]) #file to file
    assert os.path.exists("test_file_to")

    cp(["-r", "test_dir_from", "test_dir_to"]) #dir to dir
    assert os.path.exists("test_dir_to")


def test_ls_PermissionError(fs: FakeFilesystem):
    fs.create_dir("test_dir")
    fs.create_dir("test_new_dir")
    with patch('src.commands.def_cp.logger') as mock_logger:
        with patch('os.listdir', side_effect=PermissionError("Ошибка доступа")):
            cp(["test_dir", "test_new_dir"])
            error = str(mock_logger.error.call_args)
            assert "Ошибка доступа" in error


def test_ls_FileNotFoundError(fs: FakeFilesystem):
    fs.create_dir("test_dir")
    fs.create_dir("test_new_dir")
    with patch('src.commands.def_cp.logger') as mock_logger:
        with patch('os.listdir', side_effect=FileNotFoundError("Произошла ошибка. Файл не найден")):
            cp(["test_dir", "test_new_dir"])
            error = str(mock_logger.error.call_args)
            assert "Произошла ошибка. Файл не найден" in error


def test_cp_FileExistsError(fs: FakeFilesystem):
    fs.create_dir("test_dir")
    fs.create_dir("test_dir/test_subdir")
    fs.create_dir("test_subdir")
    with patch('src.commands.def_cp.logger') as mock_logger:
        cp(["-r", "test_subdir", "test_dir"]) #file to file
        error = str(mock_logger.error.call_args)
        assert "Произошла ошибка. Элемент с таким названием уже существует" in error


"""def test_cp_right_args_dir(fs: FakeFilesystem): #удаление каталога
    fs.create_dir("test_dir")
    fs.create_file("test_dir/file1.txt")
    with patch('builtins.input', return_value='y'): #вместо input() сразу возвращаем значение 'y'
        cp(["-r", "test_dir"])
        files = os.listdir('.')
        finded = False
        for file in files:
            if "test_dir" in file:
                finded = True
        assert not finded #Директории не должно быть


def test_cp_right_args_file(fs: FakeFilesystem): #удаление файла
    fs.create_file("test_file.txt")
    cp(["test_file.txt"])
    files = os.listdir('.')
    finded = False
    for file in files:
        if "test_dir" in file:
            finded = True
    assert not finded #Директории не должно быть


def test_cp_FileNotFoundError():
    with patch('src.commands.def_cp.logger') as mock_logger: #вместо реального удаления записываем потенциальный результат
        cp(["test_file.txt"])
        error = str(mock_logger.error.call_args)
        assert "Не удается найти указанный файл" in error


def test_cp_PecpissionError(fs: FakeFilesystem):
    fs.create_dir("test_dir")
    with patch('src.commands.def_cp.logger') as mock_logger:
        with patch('os.remove', side_effect=PermissionError("Отказано в доступе")):
            cp(["test_dir"])
            error = str(mock_logger.error.call_args)
            assert "Отказано в доступе" in error


def test_cp_Exception_dir(fs: FakeFilesystem):

    fs.create_dir("test_dir")

    with patch('src.commands.def_cp.logger') as mock_logger:
        with patch('shutil.cptree', side_effect=Exception("Произошла непредвиденная ошибка")):
            cp(["-r", "test_dir"])

            error = str(mock_logger.error.call_args)

            assert "Произошла непредвиденная ошибка" in error"""





# python -m pytest tests/test_cp.py -v
# python -m pytest --cov=src --cov-report=term-missing
