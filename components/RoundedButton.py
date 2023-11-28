from tkinter import Canvas


class RoundedButton(Canvas):

    def __init__(
            self,
            master=None,
            text: str = "",
            radius=25,
            foreground_color="#000000",
            background_color="#ffffff",
            action=None,
            font_size=12,
            *args, **kwargs
    ):
        super(RoundedButton, self).__init__(master, *args, **kwargs)
        self.config(bg=self.master["bg"])
        self.background = background_color
        self.clicked = action
        self.font_size = font_size

        self.radius = radius
        self.text = self.create_text(0, 0, text=text, tags="button", fill=foreground_color, font=("Times", font_size),
                                     justify="center")
        self.rect = self.round_rectangle(0, 0, 0, 0, tags="button", radius=radius, fill=background_color)

        self.tag_bind("button", "<ButtonPress>", self.border)
        self.tag_bind("button", "<ButtonRelease>", self.border)
        self.bind("<Configure>", self.resize)

        text_rect = self.bbox(self.text)
        if int(self["width"]) < text_rect[2] - text_rect[0]:
            self["width"] = (text_rect[2] - text_rect[0]) + 10

        if int(self["height"]) < text_rect[3] - text_rect[1]:
            self["height"] = (text_rect[3] - text_rect[1]) + 10

    def round_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):

        points = [x1 + radius, y1,
                  x1 + radius, y1,
                  x2 - radius, y1,
                  x2 - radius, y1,
                  x2, y1,
                  x2, y1 + radius,
                  x2, y1 + radius,
                  x2, y2 - radius,
                  x2, y2 - radius,
                  x2, y2,
                  x2 - radius, y2,
                  x2 - radius, y2,
                  x1 + radius, y2,
                  x1 + radius, y2,
                  x1, y2,
                  x1, y2 - radius,
                  x1, y2 - radius,
                  x1, y1 + radius,
                  x1, y1 + radius,
                  x1, y1]

        return self.create_polygon(points, **kwargs, smooth=True)

    def resize(self, event):
        text_bbox = self.bbox(self.text)

        if self.radius > event.width or self.radius > event.height:
            radius = min((event.width, event.height))

        else:
            radius = self.radius

        bg = self.itemcget(self.rect, "fill")

        width, height = event.width, event.height

        if event.width < text_bbox[2] - text_bbox[0]:
            width = text_bbox[2] - text_bbox[0] + 30

        if event.height < text_bbox[3] - text_bbox[1]:
            height = text_bbox[3] - text_bbox[1] + 30

        self.delete(self.rect)
        self.rect = self.round_rectangle(
            5,
            5,
            width - 5,
            height - 5,
            radius=radius,
            fill=bg,
            tags="button")

        bbox = self.bbox(self.rect)

        x = ((bbox[2] - bbox[0]) / 2) - ((text_bbox[2] - text_bbox[0]) / 2)
        y = ((bbox[3] - bbox[1]) / 2) - ((text_bbox[3] - text_bbox[1]) / 2) + self.font_size / 4

        self.moveto(self.text, x, y)
        self.tag_raise(self.text)

    def border(self, event):
        if event.type == "4":
            self.itemconfig(self.rect, fill="#d2d6d3")
            if self.clicked is not None:
                self.clicked()

        else:
            self.itemconfig(self.rect, fill=self.background)

    def disabled(self, is_disabled):
        if is_disabled:
            self.itemconfig(self.rect, fill="#d2d6d3")
            self.config(state="disabled")
        else:
            self.itemconfig(self.rect, fill=self.background)
            self.config(state="normal")
