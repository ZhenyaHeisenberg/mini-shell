import logging
import os

import typer

logger = logging.getLogger(__name__)


def parse_grep_args(args: list[str]) -> tuple[bool, bool, str, str] | None:
    """Парсинг аргументов для grep команды"""
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

    if len(args) == 2:
        pattern = str(args[0])
        path = str(args[1])

        if low:
            pattern = pattern.lower()

        # Заменить точку на текущую директорию
        if path == ".":
            path = os.getcwd()

        return recursive, low, pattern, path
    else:
        return None


def grep(args: list[str]) -> str:
    typer.echo(f"\ngrep {' '.join(args)}\n")

    parsed_args = parse_grep_args(args)

    if parsed_args is None:
        typer.echo(typer.style("Использование: grep <flag> <flag> <строка> <путь к файлу/директории>",fg=typer.colors.RED,))
        logger.error("Неверное колличество аргументов")
        return None

    else:
        recursive, low, pattern, path = parsed_args

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
                    return None

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
                finded = False

                for file_name in files:
                    full_path = os.path.join(path, file_name)

                    if not os.path.isdir(full_path):
                        try:
                            with open(full_path, encoding="utf-8") as file:
                                content = file.read()


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
            logger.error(f"Произошла непредвиденная ошибка '{e}'")
