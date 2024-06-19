"""
en: This file contains the configuration of the application.
ru: В этом файле содержится конфигурация приложения.
"""
# en: path to the ffmpeg file
# ru: путь к файлу ffmpeg
FFMPEG_PATH = None
FFPROBE_PATH = None

# en: dirname for the folder where the converted files will be stored
# ru: имя папки для хранения сконвертированных файлов
DONE_FOLDER_NAME = 'CONVERT_DONE'

# en: text for message boxes
# ru: текст для message box-ов
WARNING_TEXT_FFMPEG = 'FFMPEG not found'
WARNING_TITLE_OPEN = 'Warning'
WARNING_TEXT_OPEN = 'It is not a video file. Try to choose another one'
WARNING_TEXT_EMPTY = 'File not selected'
WARNING_DONE = 'Success'
