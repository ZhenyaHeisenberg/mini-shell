import os
import sys
from unittest.mock import patch

from pyfakefs.fake_filesystem import FakeFilesystem

from src.commands.def_grep import grep

# Добавляем путь к src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_grep_dir(fs: FakeFilesystem):
    fs.create_dir("test_dir")
    fs.create_file("test_dir/test_file", contents="test text")
    with patch('src.commands.def_grep.logger') as mock_logger:
        grep(["test text", "test_dir"])
        error = str(mock_logger.error.call_args)
        assert "Попытка применения grep к диектории" in error



"""def test_grep_file(fs: FakeFilesystem):
    fs.create_file("test_file.txt", contents="test text 1\ntest text 2\n\ntest text 3")
    with patch('src.commands.def_grep.typer.echo') as mock_echo:
        grep(["test text 3", "test_file.txt"])
        #output = [str(mock_echo.call_args_list)] #Список всех выводов typer.echo
        finded = False
        for line in mock_echo.call_args_list:
            if "'test_file.txt' line 4: test text 3" in str(line):
                finded = True
        assert finded"""


def test_grep_recursive_dir(fs: FakeFilesystem):
    fs.create_dir("test_dir")
    fs.create_file("test_dir/test_file1", contents="test text")
    fs.create_file("test_dir/test_file2", contents="other text")
    with patch('src.commands.def_grep.typer.echo') as mock_echo:
        grep(["-r", "test text", "test_dir"])
        output = str(mock_echo.call_args_list) #Список всех выводов typer.echo
        assert "'test_file1' line 1: test text" in output


def test_grep_FileNotFoundError(fs: FakeFilesystem):
    with patch('src.commands.def_grep.logger') as mock_logger:
        with patch('os.listdir', side_effect=FileNotFoundError("Произошла ошибка. Файл не найден")):
            grep(["-r", "test text", "test_dir"])
            error = str(mock_logger.error.call_args)
            assert "Произошла ошибка. Файл не найден" in error


def test_grep_PermissionError(fs: FakeFilesystem):
    with patch('src.commands.def_grep.logger') as mock_logger:
        with patch('os.listdir', side_effect=PermissionError("Нет прав доступа")):
            grep(["-r", "test text", "test_dir"])
            error = str(mock_logger.error.call_args)
            assert "Нет прав доступа" in error


def test_grep_OSError(fs: FakeFilesystem):
    with patch('src.commands.def_grep.logger') as mock_logger:
        with patch('os.listdir', side_effect=OSError("Ошибка операционной системы")):
            grep(["-r", "test text", "test_dir"])
            error = str(mock_logger.error.call_args)
            assert "Ошибка операционной системы" in error


def test_grep_Exception(fs: FakeFilesystem):
    with patch('src.commands.def_grep.logger') as mock_logger:
        with patch('os.listdir', side_effect=Exception("Произошла непредвиденная ошибка")):
            grep(["-r", "test text", "test_dir"])
            error = str(mock_logger.error.call_args)
            assert "Произошла непредвиденная ошибка" in error


def test_grep_more_than_two_arguments(fs: FakeFilesystem):
    fs.create_dir("test_dir")
    fs.create_file("test_dir/test_file1", contents="test text")
    fs.create_file("test_dir/test_file2", contents="other text")
    with patch('src.commands.def_grep.logger') as mock_logger:
        grep(["-r", "test text", "test text2", "test_dir"]) #Не 2 аргумента
        error = str(mock_logger.error.call_args)
        assert "Неверное колличество аргументов" in error


def test_grep_less_than_two_arguments(fs: FakeFilesystem):
    fs.create_dir("test_dir")
    fs.create_file("test_dir/test_file1", contents="test text")
    fs.create_file("test_dir/test_file2", contents="other text")
    with patch('src.commands.def_grep.logger') as mock_logger:
        grep(["-r", "test_dir"]) #Не 2 аргумента
        error = str(mock_logger.error.call_args)
        assert "Неверное колличество аргументов" in error

"""def test_grep_UnicodeDecodeError(fs: FakeFilesystem):
    binary_data = b'\xff\xfe\x00\x01\x02\x03\x04\x05'
    fs.create_dir("test_dir")
    fs.create_file("test_dir/test_file", contents=binary_data)
    with patch('src.commands.def_grep.logger') as mock_logger:
        grep(["test text", "test_dir"])
        error = str(mock_logger.error.call_args)
        assert "Пропущен бинарный файл" in error"""


"""def test_grep_dir(fs: FakeFilesystem):
    fs.create_dir("test_dir")
    fs.create_file("test_dir/test_file.txt")
    fs.create_dir("test_new_dir")
    grep(["-r", "test_dir", "test_new_dir"])
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


def test_grep_file(fs: FakeFilesystem):
    fs.create_dir("test_dir")
    fs.create_file("test_dir/test_file1.txt", contents="test text")
    grep(["test_dir/test_file1.txt", "test_dir/test_file2.txt"])
    assert os.path.exists("test_dir/test_file2.txt")
    with open("test_dir/test_file2.txt") as text:
        assert text.read() == "test text"""











# python -m pytest tests/test_grep.py -v
# python -m pytest --cov=src --cov-report=term-missing
