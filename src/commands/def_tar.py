import logging
import shutil  # для операций с файлами

import typer

from common.config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def tar(args):
    if not args:
        print("Укажите имя файла или папки для удаления")
        return

    for i in range(len(args)):
        path = args[i]

        try:
            # архивируем в zip
            shutil.make_archive(path, "tar", path)
            typer.echo(typer.style("Успешная архивация", fg=typer.colors.GREEN))
            logger.info("Успешная архивация")

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
