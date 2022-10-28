from pathlib import Path
from normalize import normalize
import sys
import time
import shutil


#Списки файлів
text_file = []
audio_file = []
video_file = []
photo_file = []
archives_file = []
others_file = []
folders = []
set_suffix_known = set()
set_suffix_unknown = set()


def sorter(path): # функція сортування файлів

    for i in path.iterdir(): # ітерація по файлах та папках за вказаним шляхом

        if i.is_dir(): # якщо папка то заходимо
            if i.name not in ("archives", "video", "audio", "documents", "images", "other"):
                folders.append(i.name)
                sorter(path / i)  # Рекурсія

        if i.is_file(): # якщо файл перевіряємо розширення та додаємо інформацію до списків
            path_file = path / i
            format_files = path_file.suffix

            if format_files in (".txt", ".doc", ".docx", ".pdf", ".pptx", ".xlsx"):  # перевірка текстових файлів

                text_file.append(path_file.name)
                set_suffix_known.add(path_file.suffix)
                move_file(path_file, PATH / "documents")

            elif format_files in (".jpeg", ".jpg", ".png", ".svg"):  # перевірка файлів зображень

                photo_file.append(path_file.name)
                set_suffix_known.add(path_file.suffix)
                move_file(path_file, PATH / "images")

            elif format_files in (".avi", ".mp4", ".mov", ".mkv"):  # перевірка файлів відео

                video_file.append(path_file.name)
                set_suffix_known.add(path_file.suffix)
                move_file(path_file, PATH / "video")

            elif format_files in (".mp3", ".ogg", ".wav", ".amr"):  # перевірка аудіо файлів

                audio_file.append(path_file.name)
                set_suffix_known.add(path_file.suffix)
                move_file(path_file, PATH / "audio")

            elif format_files in (".zip", ".gz", ".tar"):  # перевірка архівів

                archives_file.append(path_file.name)
                set_suffix_known.add(path_file.suffix)
                move_archive(path_file, PATH / "archives")

            elif format_files: # перевірка інших нам невідомих файлів

                others_file.append(path_file.name)
                set_suffix_unknown.add(path_file.suffix)
                move_file(path_file, PATH / "others")

    for i in path.iterdir():  # ітерація по файлах та папках за вказаним шляхом
        if i.is_dir():  # якщо папка то заходимо
            if i.name not in ("archives", "video", "audio", "documents", "images", "others"):  # якщо не папка то видаляємо
                delete_folders(Path(i))  # видаляємо папку
    return None


def move_file(filename: Path, target_folder: Path):  # функція переміщення файлів
    target_folder.mkdir(exist_ok=True, parents=True)
    normalize_name = filename.stem
    filename.replace(target_folder / (normalize(normalize_name) + "_" + str(time.time()) + filename.suffix))


def move_archive(filename: Path, target_folder: Path):  # функція розпакування архівів
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / (normalize(filename.name.replace(filename.suffix, '') + "_" + str(time.time())))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(filename.resolve()),
                              str(folder_for_file.resolve()))
    except shutil.ReadError:
        print(f"Це не архів {filename}!")
        folder_for_file.rmdir()
        return None
    filename.unlink()


def delete_folders(folder: Path):  # функція для видалення папок
    try:
        folder.rmdir()
    except OSError:
        print(f"Помилка видалення папки {folder}")


def func_path():
    global PATH
    try:
        PATH = sys.argv[1]
    except IndexError:
        print("Введіть валідний шлях до папки")
    else:
        PATH = Path(PATH)
        print(f"Старт в папці: {PATH.resolve()}")
        sorter(PATH.resolve())


if __name__ == "__main__":
    func_path()

    print(f"""Текстові файли: \n\n{text_file}")
    \n\nФайли архівів: \n\n{archives_file}
    \n\nАудіо файли: \n\n{audio_file}
    \n\nВідео файли: \n\n{video_file}
    \n\nФайли зображень: \n\n{photo_file}
    \n\nНевідомі файли: \n\n{others_file}
    \n\nУсі відомі розширення: \n\n{set_suffix_known}
    \n\nУсі невідомі розширення: \n\n{set_suffix_unknown}
    \n\nУсі папки: \n\n{folders}""")


# TODO: запускаємо:  python3 sort.py `назва_папки_для_сортування`
