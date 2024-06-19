"""
en: This module is used to convert video files to a lower resolution.
ru: Этот модуль используется для конвертации видеофайлов в более низкое разрешение.
"""
import subprocess
import json


class VideoConverter:
    """
    en: This class is used to convert video files to a lower resolution or other format.
    ru: Этот класс используется для конвертации видеофайлов в более низкое разрешение или другой формат.

    :param ffmpeg_path: path to the ffmpeg / путь к ffmpeg
    :param ffprobe_path: path to the ffprobe / путь к ffprobe
    :param path: path to the video file / путь к видеофайлу
    :param rotate: flag to rotate video / флаг для поворота видео
    """
    def __init__(self, ffmpeg_path: str, ffprobe_path: str, path: str, rotate=False):
        self.ffmpeg = ffmpeg_path
        self.ffprobe = ffprobe_path
        self.path = path
        self.rotate = rotate
        size = self.check_size()
        self.width = size['width']
        self.height = size['height']

    def convert(self, name: str, compress=1):
        """
        en: This method is used to convert a video file.
        ru: Этот метод используется для конвертации видеофайла.
        :param name: new file name / новое имя файла
        :param compress: compression ratio / коэффициент сжатия
        """
        new_width = int(self.width // compress)
        new_height = int(self.height // compress)
        # check if the video needs to be rotated
        if self.rotate:
            new_width, new_height = new_height, new_width
        # start ffmpeg
        subprocess.check_output(
            f'{self.ffmpeg} '
            '-i '
            f'"{self.path}" '
            '-s '
            f'{new_width + (new_width % 2 != 0)}x{new_height + (new_height % 2 != 0)} '
            f'"{name}"',
            stderr=subprocess.STDOUT,
            shell=True
        )

    def check_size(self):
        """
        en: This method is used to check the size of the video.
        ru: Этот метод используется для проверки размера видео.
        :return: dict with video width and height / словарь с шириной и высотой видео
        """
        data = subprocess.check_output(
            f'{self.ffprobe} '
            '-hide_banner '
            '-v '
            'quiet '
            '-print_format '
            'json '
            '-select_streams '
            'v:0 '
            '-show_streams '
            f'"{self.path}"',
            stderr=subprocess.STDOUT,
            shell=True
        )
        result = json.loads(data)
        width = result['streams'][0]['width']
        height = result['streams'][0]['height']

        return {'width': width, 'height': height}
