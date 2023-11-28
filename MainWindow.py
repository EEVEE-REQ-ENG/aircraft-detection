from tkinter import *
from tkinter import filedialog

from PIL import Image, ImageTk

from components.RoundedButton import *


class MainWindow:

    # ----------------

    def __init__(self, main):
        # Window setup
        main.minsize(1000, 700)
        main.resizable(False, False)
        main.title("Aircraft detection")
        icon = ImageTk.PhotoImage(file="resources/icon.ico")
        main.iconphoto(False, icon)

        # Environment setup
        self.path = ""

        # create canvas for image
        self.__make_canvas(main)

        # images
        default_path = "resources/default-image.jpg"
        img = Image.open(default_path)
        img = img.resize((self.__canvasWidth, self.__canvasHeight))
        self.image = ImageTk.PhotoImage(img)

        # set first image on canvas
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor='nw', image=self.image)

        # display buttons frame
        self.__make_buttons_frame(main)

    # components

    def __make_canvas(self, window):
        self.__canvasWidth = 900
        self.__canvasHeight = 600
        self.canvas = Canvas(window, width=self.__canvasWidth, height=self.__canvasHeight)
        self.canvas.pack(expand=True, pady=10)

    def __make_buttons_frame(self, window):
        self.frame = Frame(window)
        self.frame.pack(expand=True)

        # button to load image
        self.__make_load_button(self.frame)

        # button to process image
        self.__make_process_button(self.frame)

    def __make_load_button(self, frame):
        self.loadButton = RoundedButton(
            frame,
            text="Select image",
            radius=25,
            action=self.handle_open_dialog,
            width=200,
            height=50)
        self.loadButton.pack(side="left")

    def __make_process_button(self, frame):
        self.processButton = RoundedButton(
            frame,
            text="Process",
            radius=25,
            action=self.process_image,
            width=200,
            height=50)
        self.processButton.pack(side="left")
        self.processButton.disabled(is_disabled=True)

    # methods

    def handle_open_dialog(self):
        filetypes = [("Image File", '.jpg'), ("Image File", '.png')]
        self.path = filedialog.askopenfilename(filetypes=filetypes)
        if self.path:
            # TODO: remove after implementation of the ML component
            temporary_path = "resources/initial.png"
            img = Image.open(temporary_path)
            img = img.resize((self.__canvasWidth, self.__canvasHeight))
            self.image = ImageTk.PhotoImage(img)
            self.canvas.itemconfig(self.image_on_canvas, image=self.image)
            self.processButton.disabled(is_disabled=False)
        # TODO: ML component integration

    def process_image(self):
        if self.path == "":
            return
        path = "resources\\result.png"
        if path:
            img = Image.open(path)
            img = img.resize((self.__canvasWidth, self.__canvasHeight))
            self.image = ImageTk.PhotoImage(img)
            self.canvas.itemconfig(self.image_on_canvas, image=self.image)
