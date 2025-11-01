import logging
import os
import shutil  # для операций с файлами

import typer

from common.config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def rm(args):
    if not args:
        print("Укажите имя файла или папки для удаления")
        return

    for i in range(len(args)):
        path = args[i]

        try:
            if os.path.isdir(path):
                # Удаляем папку с содержимым
                shutil.rmtree(path)
                typer.echo(typer.style("Папка удалена", fg=typer.colors.GREEN))
                logger.info(f"Папка удалена: '{path}'")
            else:
                # Удаляем файл
                os.remove(path)
                typer.echo(typer.style("Файл удален", fg=typer.colors.GREEN))
                logger.info(f"Файл удалён: '{path}'")

        except FileNotFoundError as e:
            typer.echo(typer.style("Файл или папка не найдена", fg=typer.colors.RED))
            logger.error(e)
            return

        except PermissionError as e:
            typer.echo(typer.style("Отказано в доступе", fg=typer.colors.RED))
            logger.error(e)
            return

        except Exception as e:
            typer.echo(typer.style("Произошла непредвиденная ошибка", fg=typer.colors.RED))
            logger.error(e)
            return
