import logging
import os
import shutil  # для операций с файлами

import typer

logger = logging.getLogger(__name__)


def cp(args: list[str]) ->  None | str:
    recursive = False
    if "-r" in args:
        recursive = True
        args.remove("-r")

    if len(args) == 2:
        path1, path2 = args[0], args[1]

        if os.path.exists(path2) and not os.path.isdir(path2): # Путь2 - только папка
            typer.echo(typer.style("Копирование в файл невозможно", fg=typer.colors.RED))
            logger.error("Копирование в файл невозможно")
            return None

        try:
            if recursive:  # есть -r
                if os.path.exists(path2):  # если путь существует
                    new_path = os.path.join(path2, os.path.basename(path1))  # path2+последняя часть path1
                    shutil.copytree(path1, new_path)  # копировать в новый, созданный путь
                    typer.echo(typer.style("Папка успешно скопирована", fg=typer.colors.GREEN))
                    logger.info("Успешное копирование папки из '{path1}' в '{path2}'")

                else:  # если пути не существует
                    shutil.copytree(path1, path2)
                    typer.echo(typer.style("Папка успешно скопирована", fg=typer.colors.GREEN))
                    logger.info("Успешное копирование папки из '{path1}' в '{path2}'")

            else:  # нет -r
                if (os.path.isdir(path1) and os.listdir(path1) == []): #Копирование пустой директории без -r
                    new_path = os.path.join(path2, os.path.basename(path1))  # path2+последняя часть path1
                    shutil.copytree(path1, new_path)  # копировать в новый, созданный путь
                    typer.echo(typer.style("Папка успешно скопирована", fg=typer.colors.GREEN))
                    logger.info("Успешное копирование папки из '{path1}' в '{path2}'")

                elif (os.path.isdir(path1) and os.listdir(path1) != []):
                    logger.error("Попытка копирования непустой дериктории без '-r'")
                    typer.echo(typer.style("Произошла ошибка. Используйте 'cp -r' для копирования непустых папок ",fg=typer.colors.RED,))

                else:
                    shutil.copy2(path1, path2)  # copy2 для сохранения метаданных
                    typer.echo(typer.style(f"Файл скопирован: {path1} -> {path2}",fg=typer.colors.GREEN))
                    logger.info("Успешный копирование из '{path1}' в '{path2}'")

        except PermissionError as e:
            logger.error(f"Ошибка доступа '{e}'")
            typer.echo(
                typer.style(
                    "Ошибка доступа",
                    fg=typer.colors.RED,
                )
            )

        except FileNotFoundError as e:
            logger.error(f"Произошла ошибка. Файл не найден '{e}'")
            typer.echo(typer.style("Произошла ошибка. Файл не найден", fg=typer.colors.RED))

        except FileExistsError as e:
            logger.error("Произошла ошибка. Элемент с таким названием уже существует '{e}'")
            typer.echo(typer.style("Произошла ошибка. Элемент с таким названием уже существует",fg=typer.colors.RED,))

        except UserWarning as e:  # ошибки пользователя
            typer.echo(e, err=True)
            logger.error(f"Пользовательская ошибка '{e}'")

        except Exception as e:  # ошибки Exception
            typer.echo(typer.style("Произошла непредвиденная ошибка", fg=typer.colors.RED))
            logger.error(f"Произошла непредвиденная ошибка '{e}'")

    else:
        typer.echo("Использование: cp <исходный_файл> <целевой_файл>")
        logger.error("ERROR: Неверное колличество аргументов")
