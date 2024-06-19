"""
en: This is a simple video converter GUI application.
ru: Это простое графическое приложение для конвертации видео.
"""
import threading

import customtkinter as ctk
from tkinter import filedialog, messagebox
import ffmpeg
import utils
import config


class MainWindow(ctk.CTk):
    """
    en: This is the main window of the application.
    ru: Это главное окно приложения.
    """
    def __init__(self):
        super().__init__()
        self.configure_main_window()
        self.create_widgets()
        self.withdraw()
        self.pre_win = None
        self.start_pre()
        self.after(20000, self.close_pre)

        # init variables
        self.type_dict = {0: 'mp4', 1: 'mov', 2: 'mkv'}
        self.compress_dict = {0: 1, 1: 1.5, 2: 2, 3: 3}
        self.file_name = ''
        self.file_type = self.type_dict[0]
        self.file_compress = self.compress_dict[0]
        self.switch_state = False
        self.convert_win = None
        self.done_win = None

        # init variables for converting
        self.filepath = ''
        self.thread = threading.Thread(target=self.convert_video)
        self.is_running = False
        self.new_type = None
        self.compress = None
        self.new_file = None

    def convert_video(self):
        """
        en: This method is used to convert the video.
        ru: Этот метод используется для конвертации видео.
        """
        # flag for checking the conversion process
        self.is_running = True
        try:
            video = ffmpeg.VideoConverter(
                utils.get_ffmpeg_path(config.FFMPEG_PATH),
                utils.get_ffprobe_path(config.FFPROBE_PATH),
                self.filepath.replace('"', '\\"'),
                self.switch_state
            )
            video.convert(self.new_file.replace('"', '\\"'), float(self.compress))
            self.is_running = False
        except FileNotFoundError as e:
            m = messagebox.showerror(config.WARNING_TITLE_OPEN, f"Error: {e}")
            if m:
                self.destroy()

    def check(self):
        """
        en: This method is used to check the conversion process.
        ru: Этот метод используется для проверки процесса конвертации.
        """
        if self.is_running:
            self.after(1000, self.check)
        else:
            self.close_convert()
            self.start_done()

    def run_function(self):
        """
        en: This method is used to run the conversion process.
        ru: Этот метод используется для запуска процесса конвертации.
        """
        if utils.file_exists(self.filepath):
            if utils.is_video(self.filepath):
                utils.new_dir(self.filepath, config.DONE_FOLDER_NAME)
                self.new_file = utils.change_filename(self.filepath, config.DONE_FOLDER_NAME, self.file_type)
                self.new_type = self.file_type
                self.compress = self.file_compress
                self.thread.start()
                self.start_convert()
                self.check()
            else:
                m = messagebox.showerror(config.WARNING_TITLE_OPEN, config.WARNING_TEXT_OPEN)
                if m:
                    self.deiconify()
        else:
            m = messagebox.showerror(config.WARNING_TITLE_OPEN, config.WARNING_TEXT_EMPTY)
            if m:
                self.deiconify()

    def configure_main_window(self):
        """
        en: This method is used to configure the main window.
        ru: Этот метод используется для настройки главного окна.
        """
        self.title('Main_Window')
        self.geometry(f'600x400+{self.winfo_screenwidth() // 2 - 300}+{self.winfo_screenheight() // 2 - 200}')
        self.minsize(600, 400)
        self.maxsize(600, 400)

    def create_widgets(self):
        """
        en: This method is used to create widgets.
        ru: Этот метод используется для создания виджетов.
        """
        self.create_background_frames()
        self.create_title_label()
        self.create_file_group()
        self.create_type_group()
        self.create_compress_group()
        self.create_convert_button()
        self.create_switcher_group()

    def create_background_frames(self):
        """
        en: This method is used to create background frames.
        ru: Этот метод используется для создания фоновых фреймов.
        """
        self.frame_bg = ctk.CTkFrame(master=self, fg_color="#242424", width=600, height=400)
        self.frame_bg.place(x=0, y=0)
        self.frame = ctk.CTkFrame(
            master=self,
            fg_color='#0B92BC',
            bg_color="#242424",
            width=200,
            height=364,
            corner_radius=8
        )
        self.frame.place(x=12, y=14)

    def create_title_label(self):
        """
        en: This method is used to create the title label.
        ru: Этот метод используется для создания заголовка.
        """
        self.title_label = ctk.CTkLabel(
            master=self,
            text='VC',
            width=25,
            height=24,
            fg_color='#0B92BC',
            bg_color='#0B92BC',
            text_color='#ffffff',
            justify='left',
            font=('roboto', 20, 'bold')
        )
        self.title_label.place(x=16, y=16)

    def create_file_group(self):
        """
        en: This method is used to create the file group.
        ru: Этот метод используется для создания секции file.
        """
        self.create_file_frames()
        self.file_text_label = ctk.CTkLabel(
            master=self,
            text='select_file',
            text_color='#ffffff',
            bg_color='#329FC2',
            width=75, height=19,
            justify='left',
            anchor='w'
        )
        self.file_text_label.place(x=39, y=91)
        self.file_sep_label = ctk.CTkLabel(
            master=self,
            text='-->',
            bg_color='#329FC2',
            text_color='#ffffff',
            width=30,
            height=19,
            justify='right',
            anchor='e'
        )
        self.file_sep_label.place(x=180, y=91)
        self.file_button = ctk.CTkButton(
            master=self,
            width=147,
            height=25,
            text_color='#0B92BC',
            border_color='#0B92BC',
            border_width=1,
            bg_color='#464646',
            fg_color='#464646',
            hover_color='#575757',
            text='... file',
            anchor='e',
            command=self.press_file
        )
        self.file_button.place(x=403, y=87)
        self.file_button_state = 0

    def create_file_frames(self):
        """
        en: This method is used to create file frames.
        ru: Этот метод используется для создания фреймов file.
        """
        self.file_frame_1 = ctk.CTkFrame(
            master=self,
            bg_color='#0B92BC',
            fg_color='#329FC2',
            width=183,
            height=48,
            corner_radius=8
        )
        self.file_frame_1.place(x=29, y=76)
        self.file_frame_2 = ctk.CTkFrame(
            master=self,
            fg_color='#464646',
            bg_color="#242424",
            width=359,
            height=48,
            corner_radius=8
        )
        self.file_frame_2.place(x=212, y=76)
        self.file_frame_2_1 = ctk.CTkFrame(
            master=self,
            fg_color='#464646',
            width=10,
            height=48,
            corner_radius=0
        )
        self.file_frame_2_1.place(x=212, y=76)
        self.file_frame_1_1 = ctk.CTkFrame(
            master=self,
            bg_color='#0B92BC',
            fg_color='#329FC2',
            width=10,
            height=48,
            corner_radius=0
        )
        self.file_frame_1_1.place(x=202, y=76)

    def create_type_group(self):
        """
        en: This method is used to create the type group.
        ru: Этот метод используется для создания секции type.
        """
        self.create_type_frames()
        self.type_text_label = ctk.CTkLabel(
            master=self,
            text='to_type',
            text_color='#ffffff',
            bg_color='#329FC2',
            width=75,
            height=19,
            justify='left',
            anchor='w'
        )
        self.type_text_label.place(x=39, y=172)
        self.type_sep_label = ctk.CTkLabel(
            master=self,
            text='-->',
            text_color='#ffffff',
            bg_color='#329FC2',
            width=30,
            height=19,
            justify='right',
            anchor='e'
        )
        self.type_sep_label.place(x=180, y=172)
        self.create_type_buttons()

    def create_type_frames(self):
        """
        en: This method is used to create type frames.
        ru: Этот метод используется для создания фреймов type.
        """
        self.type_frame_1 = ctk.CTkFrame(
            master=self,
            bg_color='#0B92BC',
            fg_color='#329FC2',
            width=183,
            height=48,
            corner_radius=8
        )
        self.type_frame_1.place(x=29, y=157)
        self.type_frame_2 = ctk.CTkFrame(
            master=self,
            fg_color='#464646',
            bg_color="#242424",
            width=359,
            height=48,
            corner_radius=8
        )
        self.type_frame_2.place(x=212, y=157)
        self.type_frame_2_1 = ctk.CTkFrame(master=self, fg_color='#464646', width=10, height=48, corner_radius=0)
        self.type_frame_2_1.place(x=212, y=157)
        self.type_frame_1_1 = ctk.CTkFrame(
            master=self,
            bg_color='#0B92BC',
            fg_color='#329FC2',
            width=10,
            height=48,
            corner_radius=0
        )
        self.type_frame_1_1.place(x=202, y=157)

    def create_type_buttons(self):
        """
        en: This method is used to create type buttons.
        ru: Этот метод используется для создания кнопок type.
        """
        self.mp4_button = ctk.CTkButton(
            master=self,
            width=80,
            height=25,
            text_color='#0B92BC',
            border_color='#0B92BC',
            border_width=1,
            bg_color='#464646',
            fg_color='#464646',
            hover_color='#575757',
            text='mp4',
            anchor='center',
            command=self.press_mp4
        )
        self.mp4_button.place(x=275, y=168)
        self.mov_button = ctk.CTkButton(
            master=self,
            width=80,
            height=25,
            text_color='#0B92BC',
            border_color='#0B92BC',
            border_width=1,
            bg_color='#464646',
            fg_color='#464646',
            hover_color='#575757',
            text='mov',
            anchor='center',
            command=self.press_mov
        )
        self.mov_button.place(x=372, y=168)
        self.mkv_button = ctk.CTkButton(
            master=self,
            width=80,
            height=25,
            text_color='#0B92BC',
            border_color='#0B92BC',
            border_width=1,
            bg_color='#464646',
            fg_color='#464646',
            hover_color='#575757',
            text='mkv',
            anchor='center',
            command=self.press_mkv
        )
        self.mkv_button.place(x=469, y=168)
        self.select_type = 0

    def create_compress_group(self):
        """
        en: This method is used to create the compress group.
        ru: Этот метод используется для создания секции compress.
        """
        self.create_compress_frames()
        self.compress_text_label = ctk.CTkLabel(
            master=self,
            text='compress_to',
            text_color='#ffffff',
            bg_color='#329FC2',
            width=75,
            height=19,
            justify='left',
            anchor='w'
        )
        self.compress_text_label.place(x=39, y=253)
        self.compress_sep_label = ctk.CTkLabel(
            master=self,
            text='-->',
            text_color='#ffffff',
            bg_color='#329FC2',
            width=30,
            height=19,
            justify='right',
            anchor='e'
        )
        self.compress_sep_label.place(x=180, y=253)
        self.create_compress_buttons()

    def create_compress_frames(self):
        """
        en: This method is used to create compress frames.
        ru: Этот метод используется для создания фреймов compress.
        """
        self.compress_frame_1 = ctk.CTkFrame(
            master=self,
            bg_color='#0B92BC',
            fg_color='#329FC2',
            width=183,
            height=48,
            corner_radius=8
        )
        self.compress_frame_1.place(x=29, y=238)
        self.compress_frame_2 = ctk.CTkFrame(
            master=self,
            fg_color='#464646',
            bg_color="#242424",
            width=359,
            height=48,
            corner_radius=8
        )
        self.compress_frame_2.place(x=212, y=238)
        self.compress_frame_2_1 = ctk.CTkFrame(
            master=self,
            fg_color='#464646',
            width=10,
            height=48,
            corner_radius=0
        )
        self.compress_frame_2_1.place(x=212, y=238)
        self.compress_frame_1_1 = ctk.CTkFrame(
            master=self,
            bg_color='#0B92BC',
            fg_color='#329FC2',
            width=10,
            height=48,
            corner_radius=0
        )
        self.compress_frame_1_1.place(x=202, y=238)

    def create_compress_buttons(self):
        """
        en: This method is used to create compress buttons.
        ru: Этот метод используется для создания кнопок compress.
        """
        self.to_1_button = ctk.CTkButton(
            master=self,
            width=60,
            height=25,
            text_color='#0B92BC',
            border_color='#0B92BC',
            border_width=1,
            bg_color='#464646',
            fg_color='#464646',
            hover_color='#575757',
            text='1',
            anchor='center',
            command=self.press_to_1
        )
        self.to_1_button.place(x=262, y=249)
        self.to_1p5_button = ctk.CTkButton(
            master=self,
            width=60,
            height=25,
            text_color='#0B92BC',
            border_color='#0B92BC',
            border_width=1,
            bg_color='#464646',
            fg_color='#464646',
            hover_color='#575757',
            text='/1.5',
            anchor='center',
            command=self.press_to_1p5
        )
        self.to_1p5_button.place(x=338, y=249)
        self.to_2_button = ctk.CTkButton(
            master=self,
            width=60,
            height=25,
            text_color='#0B92BC',
            border_color='#0B92BC',
            border_width=1,
            bg_color='#464646',
            fg_color='#464646',
            hover_color='#575757',
            text='/2',
            anchor='center',
            command=self.press_to_2
        )
        self.to_2_button.place(x=414, y=249)
        self.to_3_button = ctk.CTkButton(
            master=self,
            width=60,
            height=25,
            text_color='#0B92BC',
            border_color='#0B92BC',
            border_width=1,
            bg_color='#464646',
            fg_color='#464646',
            hover_color='#575757',
            text='/3',
            anchor='center',
            command=self.press_to_3
        )
        self.to_3_button.place(x=490, y=249)

    def create_convert_button(self):
        """
        en: This method is used to create the convert button.
        ru: Этот метод используется для создания кнопки convert.
        """
        self.convert_button = ctk.CTkButton(
            master=self,
            width=173,
            height=47,
            text_color='#FFFFFF',
            border_color='#FFFFFF',
            border_width=2,
            bg_color='#0B92BC',
            fg_color='#329FC2',
            hover_color='#43AFD3',
            text='CONVERT',
            font=('roboto', 13, 'bold'),
            anchor='w',
            command=self.press_convert
        )
        self.convert_button.place(x=30, y=318)

    def create_switcher_group(self):
        """
        en: This method is used to create the switcher group.
        ru: Этот метод используется для создания секции switcher.
        """
        self.switch_text_label = ctk.CTkLabel(
            master=self,
            text='rotate',
            text_color='#ffffff',
            bg_color="#242424",
            font=('roboto', 11),
            width=75,
            height=19,
            justify='left',
            anchor='w'
        )
        self.switch_text_label.place(x=495, y=312)
        self.switcher = ctk.CTkSwitch(
            master=self,
            fg_color='#464646',
            bg_color="#242424",
            text='',
            width=15,
            progress_color='#329FC2',
            command=self.press_switch
        )
        self.switcher.place(x=534, y=310)
        self.switch_state = 0

    def start_pre(self):
        """
        en: This method is used to start the start app window.
        ru: Этот метод используется для запуска загрузочного окна.
        :return:
        """
        self.pre_win = ctk.CTkToplevel()
        self.pre_win.geometry(f'600x400+{self.winfo_screenwidth() // 2 - 300}+{self.winfo_screenheight() // 2 - 200}')
        self.pre_win.minsize(600, 400)
        self.pre_win.maxsize(600, 400)
        self.pre_win.title('PreLoad_Window')
        frame_bg = ctk.CTkFrame(master=self.pre_win, fg_color="#242424", width=600, height=400)
        frame_bg.place(x=0, y=0)
        frame_1 = ctk.CTkFrame(
            master=self.pre_win,
            fg_color='#0B92BC',
            bg_color="#242424",
            width=265,
            height=65,
            corner_radius=8
        )
        frame_1.place(x=116, y=168)
        text_title = ctk.CTkLabel(
            master=self.pre_win,
            text='Video\nConverter',
            text_color='#ffffff',
            width=81,
            height=48,
            fg_color='#0B92BC',
            bg_color='#0B92BC',
            justify='left',
            font=('roboto', 20, 'bold')
        )
        text_title.place(x=136, y=172)
        text_author = ctk.CTkLabel(
            master=self.pre_win,
            text='by di-m-dy',
            text_color='#aaaaaa',
            bg_color='#242424',
            width=20,
            height=12,
            justify='left',
            font=('roboto', 8)
        )
        text_author.place(x=332, y=234)

    def close_pre(self):
        """
        en: This method is used to close the start app window.
        ru: Этот метод используется для закрытия загрузочного окна.
        """
        self.pre_win.destroy()
        self.deiconify()

    def start_convert(self):
        """
        en: This method is used to start the convert window.
        ru: Этот метод используется для запуска окна конвертации.
        """
        self.convert_win = ctk.CTkToplevel()
        self.convert_win.geometry(
            f'600x400+{self.winfo_screenwidth() // 2 - 300}+{self.winfo_screenheight() // 2 - 200}'
        )
        self.convert_win.minsize(600, 400)
        self.convert_win.maxsize(600, 400)
        self.convert_win.title('Convert_Window')
        convert_frame = ctk.CTkFrame(
            master=self.convert_win,
            width=261,
            height=25,
            corner_radius=8,
            border_width=1,
            fg_color='transparent',
            border_color='#0B92BC'
        )
        convert_frame.place(x=118, y=175)
        label_convert = ctk.CTkLabel(
            master=self.convert_win,
            text='video_is_converting',
            text_color='#0B92BC',
            width=100,
            height=16,
            anchor='w'
        )
        label_convert.place(x=125, y=176)

    def close_convert(self):
        """
        en: This method is used to close the convert window.
        ru: Этот метод используется для закрытия окна конвертации.
        :return:
        """
        self.convert_win.withdraw()

    def start_done(self):
        """
        en: This method is used to start the done window.
        ru: Этот метод используется для запуска окна завершения.
        """
        self.done_win = ctk.CTkToplevel()
        self.done_win.protocol('WM_DELETE_WINDOW', self.close_done)
        self.done_win.geometry(f'600x400+{self.winfo_screenwidth() // 2 - 300}+{self.winfo_screenheight() // 2 - 200}')
        self.done_win.minsize(600, 400)
        self.done_win.maxsize(600, 400)
        self.done_win.title('Done_Window')
        self.close_convert()
        done_frame = ctk.CTkFrame(
            master=self.done_win,
            width=261,
            height=25,
            corner_radius=8,
            border_width=1,
            fg_color='#0B92BC',
            border_color='#0B92BC'
        )
        done_frame.place(x=118, y=175)
        label_done = ctk.CTkLabel(
            master=self.done_win,
            text='DONE: ',
            text_color='#FFFFFF',
            bg_color='#0B92BC',
            width=100,
            height=16,
            anchor='w',
            font=('roboto', 14, 'bold')
        )
        label_done.place(x=125, y=176)
        label_done_2 = ctk.CTkLabel(
            master=self.done_win,
            text='file_is_ready: ',
            text_color='#FFFFFF',
            bg_color='#0B92BC',
            width=100,
            height=16,
            anchor='w',
            font=('roboto', 12)
        )
        label_done_2.place(x=175, y=178)

    def close_done(self):
        """
        en: This method is used to close the done window.
        ru: Этот метод используется для закрытия окна завершения.
        """
        self.done_win.destroy()
        self.destroy()

    def press_file(self):
        """
        en: This method is used to press the file button.
        ru: Этот метод используется для нажатия кнопки file.
        :return:
        """
        self.filepath = filedialog.askopenfilename()
        if self.filepath:
            self.file_button.configure(text='file_is_ready')
            self.enable_status_button(self.file_button)
        else:
            self.file_button.configure(text='... file')
            self.disable_status_button(self.file_button)

    def press_mkv(self):
        """
        en: This method is used to press the mkv button.
        ru: Этот метод используется для нажатия кнопки mkv.
        """
        self.enable_status_button(self.mkv_button)
        for button in [self.mov_button, self.mp4_button]:
            self.disable_status_button(button)
        self.file_type = self.type_dict[2]

    def press_mov(self):
        """
        en: This method is used to press the mov button.
        ru: Этот метод используется для нажатия кнопки mov.
        """
        self.enable_status_button(self.mov_button)
        for button in [self.mkv_button, self.mp4_button]:
            self.disable_status_button(button)
        self.file_type = self.type_dict[1]

    def press_mp4(self):
        """
        en: This method is used to press the mp4 button.
        ru: Этот метод используется для нажатия кнопки mp4.
        """
        self.enable_status_button(self.mp4_button)
        for button in [self.mkv_button, self.mov_button]:
            self.disable_status_button(button)
        self.file_type = self.type_dict[0]

    def press_to_3(self):
        """
        en: This method is used to press the 3 button.
        ru: Этот метод используется для нажатия кнопки 3.
        """
        self.enable_status_button(self.to_3_button)
        for button in [self.to_1_button, self.to_1p5_button, self.to_2_button]:
            self.disable_status_button(button)
        self.file_compress = self.compress_dict[3]

    def press_to_2(self):
        """
        en: This method is used to press the 2 button.
        ru: Этот метод используется для нажатия кнопки 2.
        """
        self.enable_status_button(self.to_2_button)
        for button in [self.to_1_button, self.to_1p5_button, self.to_3_button]:
            self.disable_status_button(button)
        self.file_compress = self.compress_dict[2]

    def press_to_1p5(self):
        """
        en: This method is used to press the 1.5 button.
        ru: Этот метод используется для нажатия кнопки 1.5.
        :return:
        """
        self.enable_status_button(self.to_1p5_button)
        for button in [self.to_1_button, self.to_3_button, self.to_2_button]:
            self.disable_status_button(button)
        self.file_compress = self.compress_dict[1]

    def press_to_1(self):
        """
        en: This method is used to press the 1 button.
        ru: Этот метод используется для нажатия кнопки 1.
        :return:
        """
        self.enable_status_button(self.to_1_button)
        for button in [self.to_3_button, self.to_2_button, self.to_1p5_button]:
            self.disable_status_button(button)
        self.file_compress = self.compress_dict[0]

    def press_switch(self):
        """
        en: This method is used to press the switch button.
        ru: Этот метод используется для нажатия кнопки switch.
        """
        self.switch_state = bool(1 - self.switch_state)

    def press_convert(self):
        """
        en: This method is used to press the convert button.
        ru: Этот метод используется для нажатия кнопки convert.
        :return:
        """
        self.withdraw()
        self.run_function()

    @staticmethod
    def enable_status_button(button: ctk.CTkButton):
        """
        en: This method is used to enable the status button.
        ru: Этот метод используется для активации кнопки статуса.
        """
        button.configure(fg_color='#0B92BC', text_color='#FFFFFF', hover_color='#0B92BC')

    @staticmethod
    def disable_status_button(button: ctk.CTkButton):
        """
        en: This method is used to disable the status button.
        ru: Этот метод используется для деактивации кнопки статуса.
        """
        button.configure(fg_color='#464646', text_color='#0B92BC', hover_color='#575757')


app = MainWindow()

if __name__ == '__main__':
    app.mainloop()
