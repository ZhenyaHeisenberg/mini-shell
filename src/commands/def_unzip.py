import logging
import shutil  # для операций с файлами

import typer

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
                typer.echo(typer.style("Файл распакован", fg=typer.colors.GREEN))
                logger.info("Успешная распаковка")
            else:
                typer.echo("Распаковка неархива невозможна")
                logger.error("Попытка распаковки неархива")
                return

        except FileNotFoundError as e:
            typer.echo(typer.style("Файл не найден", fg=typer.colors.RED))
            logger.error("Файл не найден", e)
            return

        except PermissionError as e:
            typer.echo(typer.style("Отказано в доступе", fg=typer.colors.RED))
            logger.error("Отказано в доступе", e)
            return

        except Exception as e:
            typer.echo(typer.style("Произошла непредвиденная ошибка", fg=typer.colors.RED))
            logger.error("Произошла непредвиденная ошибка", e)
            return


