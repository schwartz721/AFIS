from tkinter import *


class Color_Selection():
    def __init__(self, master, color, x, y):
        self.master = master
        self.master.geometry('+%d+%d' % (x, y))
        self.master.config(borderwidth=3, relief=RAISED)
        self.canvas = Canvas(self.master)
        self.canvas.pack(fill=BOTH, expand=True)
        self.canvas.config(width=256 // 8 * 16, height=256 // 8 * 16)
        self.canvas.bind('<Button-1>', self.click)
        self.color = color
        self.slider = IntVar()
        self.slider.trace('w', self.show_colors)
        self.slider.set('0x' + self.color[-2:])
        x = int(self.color[1:3], 16) // 8 * 16
        y = int(self.color[3:5], 16) // 8 * 16
        self.choice_outline = self.canvas.create_rectangle(x - 1, y - 1, x + 17, y + 17,
                                                           outline='white')
        self.choice = self.canvas.create_rectangle(x, y, x + 16, y + 16,
                                                   fill=self.color)
        Button(self.master, text='Select Color', command=lambda: self.destroy()).pack(side=RIGHT)
        if max(int(self.color[1:3], 16), int(self.color[3:5], 16)) < 128:
            text_color = 'white'
        else:
            text_color = 'black'
        self.preview = Label(self.master, text='Color preview', bd=2, relief='solid',
                             bg=self.color, fg=text_color)
        self.preview.pack(side=LEFT)
        Scale(self.master, from_=0, to=255, variable=self.slider, orient=HORIZONTAL).pack()

    def show_colors(self, *args):
        self.canvas.delete(ALL)
        b = self.slider.get()
        for x, r in enumerate(range(0, 256, 8)):
            for y, g in enumerate(range(0, 256, 8)):
                self.canvas.create_rectangle(x * 16, y * 16, (x + 1) * 16, (y + 1) * 16,
                                             fill='#%02x%02x%02x' % (r, g, b),
                                             outline='#%02x%02x%02x' % (r, g, b))

    def click(self, event):
        self.canvas.delete(self.choice_outline)
        self.canvas.delete(self.choice)
        x, y = event.x, event.y
        r = x // 16 * 8
        g = y // 16 * 8
        b = self.slider.get()
        self.color = '#%02x%02x%02x' % (r, g, b)
        self.choice_outline = self.canvas.create_rectangle(x - 9, y - 9, x + 9, y + 9,
                                                           outline='white')
        self.choice = self.canvas.create_rectangle(x - 8, y - 8, x + 8, y + 8,
                                                   fill=self.color)
        if max(int(self.color[1:3], 16), int(self.color[3:5], 16)) < 128:
            text_color = 'white'
        else:
            text_color = 'black'
        self.preview.config(bg=self.color, fg=text_color)

    def destroy(self):
        self.master.destroy()

    def wait(self):
        self.master.wait_window()
        return self.color
