import logging
import os
import shutil  # для операций с файлами

import typer

logger = logging.getLogger(__name__)


def rm(args):
    if not args:
        typer.echo("Укажите имя файла или папки для удаления")
        logger.info("Укажите имя файла или папки для удаления")
        return

    if "-r" in args:
        recursive = True
        args.remove("-r")
    else:
        recursive = False

    for i in range(len(args)):
        path = args[i]

        try:
            if recursive:
            #if os.path.isdir(path):
                #Запрашиваем подтверждение
                typer.echo(typer.style(f"Вы уверены, что хотите удалить каталог '{path}' вместе со всем содержимым? (y/n)", fg=typer.colors.YELLOW))
                verification = input()

                if verification.lower() == "y": #Удаляем папку с содержимым

                    shutil.rmtree(path)
                    typer.echo(typer.style("Папка удалена", fg=typer.colors.GREEN))
                    logger.info(f"Папка удалена: '{path}'")
                return None
            else:
                # Удаляем файл
                os.remove(path)
                typer.echo(typer.style("Файл удален", fg=typer.colors.GREEN))
                logger.info(f"Файл удалён: '{path}'")

        except FileNotFoundError as e:
            typer.echo(typer.style("Файл или папка не найдена", fg=typer.colors.RED))
            logger.error(e)
            return

        except NotADirectoryError as e:
            typer.echo(typer.style("Флаг '-r' только для удаления директорий", fg=typer.colors.RED))
            logger.error(f"Флаг '-r' только для удаления директорий '{e}'")
            return

        except IsADirectoryError as e:
            typer.echo(typer.style("Для удаления каталога используйте флаг '-r'", fg=typer.colors.RED))
            logger.error(e)
            return

        except PermissionError as e:
            typer.echo(typer.style("Отказано в доступе", fg=typer.colors.RED))
            typer.echo("Подсказка: используйте флаг '-r' для удаления каталогов ")
            logger.error(e)
            return

        except Exception as e:
            typer.echo(typer.style("Произошла непредвиденная ошибка", fg=typer.colors.RED))
            logger.error(f"Произошла непредвиденная ошибка '{e}'")
            return
