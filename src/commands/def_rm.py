import logging
import os
import shutil  # для операций с файлами

import typer

logger = logging.getLogger(__name__)


def rm(args: list[str]) ->  None | str:
    if not args:
        typer.echo("Укажите имя файла или папки для удаления")
        logger.info("Укажите имя файла или папки для удаления")
        return None

    if "-r" in args:
        recursive = True
        args.remove("-r")
    else:
        recursive = False

    for i in range(len(args)):
        path = args[i]

        try:
            if recursive:
                full_path = os.path.abspath(path) #получаем абсолютный путь
                if full_path == os.path.abspath('/') or full_path == os.path.abspath('\\'): #является корневым каталогом
                    typer.echo(typer.style("Удаление корневого каталога запрещено", fg=typer.colors.RED))
                    logger.error(f"Попытка удаления корневого каталога: '{full_path}'")
                    return None

                if path == ".." or full_path in os.getcwd():
                    typer.echo(typer.style("Удаление родительского каталога запрещено", fg=typer.colors.RED))
                    logger.error(f"Попытка удаления родительского каталога: '{full_path}'")
                    return None
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
            return None

        except NotADirectoryError as e:
            typer.echo(typer.style("Флаг '-r' только для удаления директорий", fg=typer.colors.RED))
            logger.error(f"Флаг '-r' только для удаления директорий '{e}'")
            return None

        except IsADirectoryError as e:
            typer.echo(typer.style("Для удаления каталога используйте флаг '-r'", fg=typer.colors.RED))
            logger.error(e)
            return None

        except PermissionError as e:
            typer.echo(typer.style("Отказано в доступе", fg=typer.colors.RED))
            typer.echo("Подсказка: используйте флаг '-r' для удаления каталогов ")
            logger.error(e)
            return None

        except Exception as e:
            typer.echo(typer.style("Произошла непредвиденная ошибка", fg=typer.colors.RED))
            logger.error(f"Произошла непредвиденная ошибка '{e}'")
            return None
