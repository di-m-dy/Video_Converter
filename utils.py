"""
en: This file contains functions that are used to work with files and directories.
ru: В этом файле содержатся функции, которые используются для работы с файлами и каталогами.
"""
import os
import subprocess


def get_ffprobe_path(path=None) -> str:
    """
    en: This function is used to get the path to the ffprobe file.
        This function is also used to check if the ffprobe file exists.
    ru: Эта функция используется для получения пути к файлу ffprobe.
        Эта функция также используется для проверки существования файла ffprobe.

    :param path: path to the ffprobe / путь к ffprobe
    :return: real working path or raise FileNotFoundError / реальный рабочий путь или вызов исключения FileNotFoundError
    """
    type_os = os.name
    if not path:
        if type_os == 'posix' or type_os == 'mac':
            path = subprocess.getoutput('which ffprobe')
        elif type_os == 'nt':
            path = subprocess.getoutput('for %i in (ffprobe.exe) do @echo %~fi')
        else:
            raise FileNotFoundError('OS not supported')

    if type_os == 'posix' or type_os == 'mac':
        if subprocess.getoutput(f"{path} -version").startswith('ffprobe version'):
            return path
        else:
            raise FileNotFoundError('ffprobe not found')
    elif type_os == 'nt':
        if subprocess.getoutput(f"{path} -version").startswith('ffprobe version'):
            return path
        else:
            raise FileNotFoundError('ffprobe not found')
    else:
        raise FileNotFoundError('OS not supported')


def get_ffmpeg_path(path=None) -> str:
    """
    en: This function is used to get the path to the ffmpeg file.
        This function is also used to check if the ffmpeg file exists.
    ru: Эта функция используется для получения пути к файлу ffmpeg.
        Эта функция также используется для проверки существования файла ffmpeg.
    :param path: path to the ffmpeg / путь к ffmpeg
    :return: real working path or raise FileNotFoundError / реальный рабочий путь или вызов исключения FileNotFoundError
    """
    type_os = os.name
    if not path:
        if type_os == 'posix' or type_os == 'mac':
            path = subprocess.getoutput('which ffmpeg')
        elif type_os == 'nt':
            path = subprocess.getoutput('for %i in (ffmpeg.exe) do @echo %~fi')
        else:
            raise FileNotFoundError('OS not supported')

    if type_os == 'posix' or type_os == 'mac':
        if subprocess.getoutput(f"{path} -version").startswith('ffmpeg version'):
            return path
        else:
            raise FileNotFoundError('ffmpeg not found')
    elif type_os == 'nt':
        if subprocess.getoutput(f"{path} -version").startswith('ffmpeg version'):
            return path
        else:
            raise FileNotFoundError('ffmpeg not found')
    else:
        raise FileNotFoundError('OS not supported')


def file_exists(path):
    """
    en: This function is used to check if the file exists.
    ru: Эта функция используется для проверки существования файла.
    :param path: path to the file / путь к файлу
    :return: bool
    """
    return os.path.exists(path)


def new_dir(path, name_dir):
    """
    en: This function is used to create a new directory.
    ru: Эта функция используется для создания нового каталога.
    :param path: path to the file / путь к файлу
    :param name_dir: name of the new directory / имя нового каталога
    """
    path_dir = os.path.join(os.path.dirname(path), name_dir)
    if not os.path.exists(path_dir):
        os.mkdir(path_dir)


def change_filename(path, dir_path='', _type=None):
    """
    en: This function is used to change the file name.
        For case if the file already exists, the function will add a number to the file name.
    ru: Эта функция используется для изменения имени файла.
        В случае, если файл уже существует, функция добавит к имени файла номер.
    :param path: path to the file / путь к файлу
    :param dir_path: path to the directory / путь к каталогу
    :param _type: type of the file / тип файла
    :return: path with new file name / путь с новым именем файла
    """
    filename_list = os.path.split(path)
    file_path = filename_list[0]
    filename = filename_list[1].split('.')
    f_name = filename[0]
    f_type = filename[1]

    if dir_path:
        dir_path = os.path.join(file_path, dir_path)
    else:
        dir_path = file_path

    check_list_dir = [i.replace(f'.{i.split(".")[-1]}', "") for i in os.listdir(dir_path)]
    if check_list_dir:
        temp_list = [int(i.split('_convert_')[1]) for i in check_list_dir if f'{f_name}_convert_' in i]
        if temp_list:
            max_index = max(temp_list)
            new_f_name = f'{f_name.split("_convert_")[0]}_convert_{max_index + 1}'
        else:
            new_f_name = f'{f_name}_convert_1'
    else:
        new_f_name = f'{f_name}_convert_1'

    if _type:
        new_f_type = _type.replace(' ', '_')
    else:
        new_f_type = f_type.replace(' ', '_')

    return os.path.join(dir_path, f'{new_f_name}.{new_f_type}')


def is_video(path):
    """
    en: This function is used to check if the file is a video.
    ru: Эта функция используется для проверки, является ли файл видео.
    :param path: path to the file / путь к файлу
    :return: bool
    """
    type_list = ['mov', 'MOV', 'mp4', 'mpeg4', 'avi', 'mkv']
    _type = path.split('.')[-1]
    return _type in type_list
