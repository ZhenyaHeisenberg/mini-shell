import logging
import os

import typer

from common.config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def mv(args):
    if len(args) != 2:
        typer.echo(typer.style("Использование: mv <источник> <цель>", fg=typer.colors.RED))
        logger.error("ERROR: Неверное колличество аргументов")
        return

    path1, path2 = args[0], args[1]

    try:
        # прроверяем, существует ли path1
        if not os.path.exists(path1):
            typer.echo(
                typer.style("Произошла ошибка. Папка не найдена", fg=typer.colors.RED)
            )
            logger.error(f"ERROR: '{path1}' не существует")
            return

        # если path2 существует, перемещаем в неё
        if os.path.isdir(path2):
            filename = os.path.basename(path1)
            path2 = os.path.join(path2, filename)

            typer.echo(
                typer.style(
                    f"Файл успешно перемещён: {path1} → {path2}", fg=typer.colors.GREEN
                )
            )
            logger.info(f"Файл перемещён: '{path1}' -> '{path2}'")

        os.rename(path1, path2)  # переименовываем
        typer.echo(typer.style(f"Файл успешно переименован: {path1} → {path2}", fg=typer.colors.GREEN))
        logger.info(f"Файл переименован: '{path1}' -> '{path2}'")

    except PermissionError as e:
        typer.echo(typer.style("Нет прав доступа", fg=typer.colors.RED))
        logger.error(e)

    except OSError as e:
        typer.echo(typer.style("Ошибка операционной системы", fg=typer.colors.RED))
        logger.error(e)

    except Exception as e:
        typer.echo(typer.style("Произошла непредвиденная ошибка", fg=typer.colors.RED))
        logger.error(e)
