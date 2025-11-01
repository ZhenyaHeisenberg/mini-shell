import logging
import os

import typer

from commands.def_cat import cat
from commands.def_cd import cd
from commands.def_cp import cp
from commands.def_grep import grep
from commands.def_ls import ls
from commands.def_mv import mv
from commands.def_rm import rm
from commands.def_tar import tar
from commands.def_untar import untar
from commands.def_unzip import unzip
from commands.def_zip import zip
from common.config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def main():
    typer.echo("Добро пожаловать в mini_shell")
    typer.echo("Введите 'exit' для выхода")

    while True:
        current_dir = os.getcwd()
        user_input = input(f"\n{current_dir}$ ").strip()  # Текущая папка

        if user_input.lower() == "exit":  # Выход из программы
            print("До свидания!")
            break

        if not user_input:
            continue

        # Разбиваем ввод на команду и аргументы
        logger.info(user_input)
        parts = user_input.split(" ")
        command = parts[0]

        argument = " ".join(parts[1:])

        flag = 0

        for i in range(len(argument) - argument.count("'") - argument.count('"')):
            if argument[i] == "'" or argument[i] == '"':
                flag += 1
                argument = str(argument[:i]) + str(argument[i + 1 :])

            if flag % 2 == 0:
                if argument[i] == " ":
                    argument = str(argument[:i]) + "$" + str(argument[i + 1 :])
            elif flag % 2 == 1:
                continue

        argument = argument.replace("'", "")
        argument = argument.replace('"', "")

        args = argument.split("$")

        execute_command(command, args)  # выполнить команду


def execute_command(command, args):
    try:
        match command:
            case "ls":
                ls(args)
            case "cd":
                cd(args)
            case "cat":
                cat(args)
            case "cp":
                cp(args)
            case "mv":
                mv(args)
            case "rm":
                rm(args)
            case "zip":
                zip(args)
            case "unzip":
                unzip(args)
            case "tar":
                tar(args)
            case "untar":
                untar(args)
            case "grep":
                grep(args)
            case _:
                print(f"Неизвестная команда: {command}")

    except FileNotFoundError as e:
        print(f"Файл не найден: {e}")
    except PermissionError as e:
        print(f"Нет прав доступа: {e}")
    except OSError as e:
        print(f"Ошибка OS: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")  # Непредвиденная ошибка


if __name__ == "__main__":
    main()
