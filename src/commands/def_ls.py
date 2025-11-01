import logging
import os
import stat
from datetime import datetime

import typer

logger = logging.getLogger(__name__)


def ls(args):
    meta = False  # содержит ли -l
    if "-l" in args:
        meta = True
        args.remove("-l")
        if len(args) == 0:
            args.append(".")

    """Если пустой ввод - добывить точку"""
    if args[0] == "":
        args[0] = "."

    for i in range(len(args)):
        path = args[i]

        """заменить точку на текущую директорию"""
        if path == ".":
            path = os.getcwd()

        if not meta:  # ls
            typer.echo(f"\nls '{path}'")
            try:
                files = os.listdir(path)

                for file in files:
                    full_path = os.path.join(path, file)

                    if os.path.isdir(full_path):  # если является директорией
                        if len(str(file).split()) > 1:  # содержит пробел
                            file = typer.style(f"'{file}'", fg=typer.colors.BLUE)
                            typer.echo(f"{file}/")
                        else:  # не содержит пробел
                            file = typer.style(f"{file}", fg=typer.colors.BLUE)
                            typer.echo(f"{file}/")
                    else:  # если не является директорией
                        if len(str(file).split()) > 1:  # содержит пробел
                            typer.echo(f"'{file}'")
                        else:  # не содержит пробел
                            typer.echo(f"{file}")
            except FileNotFoundError as e:
                typer.echo(
                    typer.style(
                        "Произошла ошибка. Папка не найдена", fg=typer.colors.RED
                    )
                )
                logger.error(e)
                continue
            except NotADirectoryError as e:  # файл а не папка
                typer.echo(
                    typer.style(
                        "Произошла ошибка. Функция ls только для директорий",
                        fg=typer.colors.RED,
                    )
                )
                logger.error(e)
                continue
            except UserWarning as e:  # ошибки пользователя
                typer.echo(e, err=True)
                logger.error("Ошибка пользователя {e}")
                continue
            except OSError as e:
                typer.echo(
                    typer.style("Ошибка операционной системы", fg=typer.colors.RED)
                )
                logger.error("Ошибка операционной системы {e}")
                continue
            except Exception as e:  # ошибки Exception
                typer.echo(
                    typer.style("Произошла непредвиденная ошибка", fg=typer.colors.RED)
                )
                logger.error("Произошла непредвиденная ошибка {e}")
                continue

        else:  # ls -l
            typer.echo(f"\nls -l '{path}'")

            try:
                files = os.listdir(path)

                for file in files:
                    full_path = os.path.join(path, file)
                    stat_info = os.stat(full_path)

                    # Права доступа
                    permissions = stat.filemode(stat_info.st_mode)

                    # Размер
                    size = stat_info.st_size

                    # Время модификации
                    mtime = datetime.fromtimestamp(stat_info.st_mtime).strftime(
                        "%Y-%m-%d %H:%M"
                    )

                    # Тип и имя
                    if os.path.isdir(full_path):  # если является директорией
                        if len(str(file).split()) > 1:  # содержит пробел
                            file = typer.style(f"'{file}'", fg=typer.colors.BLUE)
                            file = typer.style(f"{file}/")
                        else:  # не содержит пробел
                            file = typer.style(f"{file}", fg=typer.colors.BLUE)
                            file = typer.style(f"{file}/")
                    else:  # если является файлом
                        if len(str(file).split()) > 1:  # содержит пробел
                            file = typer.style(f"'{file}'")
                        else:  # не содержит пробел
                            file = typer.style(f"{file}")

                    print(
                        f"{permissions} {stat_info.st_nlink:>2} {size:>8} {mtime} {file}"
                    )

            except FileNotFoundError as e:  # файл не найден
                typer.echo(
                    typer.style(
                        "Произошла ошибка. Папка не найдена", fg=typer.colors.RED
                    )
                )
                logger.error("Произошла ошибка. Папка не найдена {e}")
                continue
            except NotADirectoryError as e:  # файл а не папка
                typer.echo(
                    typer.style(
                        "Произошла ошибка. Функция ls только для директорий",
                        fg=typer.colors.RED,
                    )
                )
                logger.error(e)
                continue
            except UserWarning as e:  # ошибки пользователя
                typer.echo(e, err=True)
                logger.error(e)
                continue
            except OSError as e:  # ошибки ОС
                typer.echo(
                    typer.style("Ошибка операционной системы", fg=typer.colors.RED)
                )
                logger.error("Ошибка операционной системы {e}")
                continue
            except Exception as e:  # ошибки Exception
                typer.echo(
                    typer.style("Произошла непредвиденная ошибка", fg=typer.colors.RED)
                )
                logger.error("Произошла непредвиденная ошибка {e}")
                continue
