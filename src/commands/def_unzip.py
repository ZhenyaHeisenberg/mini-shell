import logging
import shutil  # для операций с файлами

import typer

from common.config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def unzip(args):
    if not args:
        print("Укажите имя файла или папки для удаления")
        return

    for i in range(len(args)):
        path = args[i]

        try:
            if ".zip" in path:
                # Разархивация
                shutil.unpack_archive(path)
                typer.echo(typer.style("Файл разархивирован", fg=typer.colors.GREEN))
                logger.info("Успешная архивация")
            else:
                typer.echo(
                    typer.style("Разрхивация неархива невозможна", fg=typer.colors.RED)
                )
                logger.info("Попытка архивации не директории")
                return

        except FileNotFoundError as e:
            typer.echo(typer.style("Папка не найдена", fg=typer.colors.RED))
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
