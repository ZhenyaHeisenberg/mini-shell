import logging
import shutil  # для операций с файлами

import typer

logger = logging.getLogger(__name__)


def untar(args: list[str]) ->  None | str:
    if not args:
        print("Укажите имя файла или папки для удаления")
        return None

    for i in range(len(args)):
        path = args[i]

        try:
            if ".tar" in path:
                # Разархивация
                shutil.unpack_archive(path)
                typer.echo(typer.style("Файл распакован", fg=typer.colors.GREEN))
                logger.info("Успешная распаковка")
            else:
                typer.echo("Распаковка неархива невозможна")
                logger.info("Попытка распаковки неархива")
                return None

        except FileNotFoundError as e:
            typer.echo(typer.style("Папка не найдена", fg=typer.colors.RED))
            logger.error(e)
            return None

        except PermissionError as e:
            typer.echo(typer.style("Отказано в доступе", fg=typer.colors.RED))
            logger.error(e)
            return None

        except Exception as e:
            typer.echo(typer.style("Произошла непредвиденная ошибка", fg=typer.colors.RED))
            logger.error(e)
            return None
