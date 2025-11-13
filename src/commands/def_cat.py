import logging
import os

import typer

logger = logging.getLogger(__name__)

def cat(args: list[str]) -> str:
    if args == []:
        typer.echo(typer.style("Укажите имя файла", fg=typer.colors.RED))
        logger.error("Имя файла не указано")
        return None

    for i in range(len(args)):
        filename = args[i]

        typer.echo(f"\nls '{filename}'")

        if os.path.isdir(filename):
            typer.echo(typer.style("Произошла ошибка. Функция 'cat' только для файлов",fg=typer.colors.RED,))
            logger.error("Попытка применения cat директории")
            return None

        try:
            with open(filename, encoding="utf-8") as file:
                content = file.read()
                typer.echo(content)
                logger.info(f"Успешное открытие файла '{filename}'")

        except FileNotFoundError as e:
            typer.echo(typer.style("Произошла ошибка. Файл не найден", fg=typer.colors.RED))
            logger.error("Произошла ошибка. Файл не найден '{e}'")
            continue

        except PermissionError as e:
            typer.echo(typer.style("Нет прав доступа", fg=typer.colors.RED))
            logger.error("Нет прав доступа '{e}'")

