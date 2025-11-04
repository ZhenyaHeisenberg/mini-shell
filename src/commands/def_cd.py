import logging
import os

import typer

logger = logging.getLogger(__name__)


def cd(args: list[str]) ->  None | str:
    old_directory = os.getcwd() #Изначально

    if args != [""] and args != ["~"]:
        path = args[0]
        if len(args) == 1:
            if not os.path.isdir(path):
                typer.echo(typer.style("Произошла ошибка. Функция 'cd' только для директорий", fg=typer.colors.RED,))
                logger.error("Попытка применения cd не для директории")
                return None

            try:
                os.chdir(path)  #Перейти в path
                new_directory = os.getcwd() #Оказались
                logger.info(f"Успешный переход из '{old_directory}' в '{new_directory}'")

            except OSError as e:
                typer.echo(typer.style("Ошибка операционной системы", fg=typer.colors.RED))
                logger.error(f"Ошибка операционной системы '{e}'")

            except Exception as e:
                typer.echo(typer.style("Произошла непредвиденная ошибка", fg=typer.colors.RED))
                logger.error(f"Произошла непредвиденная ошибка '{e}'")
        else:
            typer.echo(typer.style("Произошла ошибка. Слишком много аргументов", fg=typer.colors.RED))
            logger.error("Произошла ошибка. Слишком много аргументов")
    else:
        home_dir = os.path.expanduser("~")  # Если не указана папка - перейти в домашнюю для всех ОС
        os.chdir(home_dir)
        new_directory = os.getcwd()
        logger.info(f"Успешный переход из '{old_directory}' в '{new_directory}'")
