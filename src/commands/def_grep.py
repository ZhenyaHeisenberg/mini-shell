import logging
import os

import typer

from common.config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def grep(args):
    typer.echo(f"\ngrep {' '.join(args)}\n")

    if "-r" in args:
        recursive = True
        args.remove("-r")
    else:
        recursive = False

    if "-i" in args:
        low = True
        args.remove("-i")
    else:
        low = False

    pattern = str(args[0])
    path = str(args[1])

    if low:
        pattern = pattern.lower()

    """заменить точку на текущую директорию"""
    if path == ".":
        path = os.getcwd()

    try:
        if not recursive:  # grep
            typer.echo(f"\ngrep '{path}'")

            if os.path.isdir(path):
                typer.echo(
                    typer.style(
                        "Для рекурсивного поиска в директории используйте grep -r",
                        fg=typer.colors.RED,
                    )
                )
                logger.error("Попытка применения grep к диектории")
                return

            with open(path, encoding="utf-8") as file:
                content = file.read()
                finded = False

                for line_num, line in enumerate(content.splitlines(), 1):
                    if low:
                        line = line.lower()  # Если -i

                    if pattern in line:
                        typer.echo(f"line {line_num}: {line}")
                        finded = True
                if not finded:
                    typer.echo("Совпадений не найдено")

        else:
            files = os.listdir(path)

            for file_name in files:
                full_path = os.path.join(path, file_name)

                if not os.path.isdir(full_path):
                    try:
                        with open(full_path, encoding="utf-8") as file:
                            content = file.read()
                            finded = False

                            for line_num, line in enumerate(content.splitlines(), 1):
                                if low:
                                    line = line.lower()  # Если -i

                                if pattern in line:
                                    typer.echo(f"'{file_name}' line {line_num}: {line}")
                                    finded = True
                    except UnicodeDecodeError:
                        # Пропускаем бинарные файлы
                        logger.debug(f"Пропущен бинарный файл: {full_path}")
                        continue
                    except PermissionError:
                        # Пропускаем файлы без доступа
                        logger.debug(f"Нет доступа к файлу: {full_path}")
                        continue
            if not finded:
                typer.echo("Совпадений не найдено")

    except FileNotFoundError as e:
        typer.echo(typer.style("Произошла ошибка. Файл не найден", fg=typer.colors.RED))
        logger.error(e)
    except PermissionError as e:
        typer.echo(typer.style("Нет прав доступа", fg=typer.colors.RED))
        logger.error(e)
    except OSError as e:
        typer.echo(typer.style("Ошибка операционной системы", fg=typer.colors.RED))
        logger.error(e)
    except Exception as e:
        typer.echo(typer.style(f"Произошла непредвиденная ошибка: {str(e)}", fg=typer.colors.RED))
        logger.error(f"Необработанное исключение: {str(e)}")
