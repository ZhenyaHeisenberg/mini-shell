import logging
import shutil  # для операций с файлами

import typer

logger = logging.getLogger(__name__)


def zip(args: list[str]) ->  None | str:
    if not args:
        typer.echo("Укажите имя файла или папки для архивирования")
        logger.error("Имя файла или директории не указано")
        return None

    for i in range(len(args)):
        path = args[i]

        try:
            # архивируем в zip
            shutil.make_archive(path, "zip", path)
            typer.echo(typer.style("Успешная архивация", fg=typer.colors.GREEN))
            logger.info("Успешная архивация")

        except FileNotFoundError as e:
            typer.echo(typer.style("Файл не найден", fg=typer.colors.RED))
            logger.error("Файл не найден: {e}")
            return None

        except PermissionError as e:
            typer.echo(typer.style("Отказано в доступе", fg=typer.colors.RED))
            logger.error("Отказано в доступе: {e}")
            return None

        except Exception as e:
            typer.echo(typer.style("Произошла непредвиденная ошибка", fg=typer.colors.RED))
            logger.error("Произошла непредвиденная ошибка: {e}")
            return None
