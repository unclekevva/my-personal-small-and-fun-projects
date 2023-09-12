import tkinter as tk
from tkinter import colorchooser, messagebox, filedialog
from PIL import Image, ImageDraw
import PIL

WIDTH, HEIGHT = 700, 700
CENTER = WIDTH // 2
WHITE = (255, 255, 255)

class Painter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.geometry(f'{WIDTH}x{HEIGHT}')
        self.root.title('Paint!')
        self.root.config(bg='#FCA292')

        self.brushsize = 25
        self.currentcolor = '#000000'
        self.argclr1 = 0
        self.argclr2 = 1

        self.image = PIL.Image.new('RGB', (WIDTH, HEIGHT), WHITE)
        self.draw = ImageDraw.Draw(self.image)

        self.cnv = tk.Canvas(self.root, width=WIDTH-150, height=HEIGHT-100)
        self.cnv.pack(padx=10, pady=10, side=tk.RIGHT)
        self.cnv.bind('<B1-Motion>', self.paint)

        #toolbar frame - start
        self.btnframe = tk.Frame(self.root, bg='#8ca292', relief=tk.RIDGE)
        self.btnframe.pack(padx=10, pady=10, side=tk.LEFT)

            #size frame - start
        self.sizeframe = tk.Frame(self.btnframe, bd=1, bg='#000', relief=tk.RIDGE)
        self.sizeframe.pack(padx=5, pady=5, side=tk.TOP)
        self.sizeframe.grid_columnconfigure((0,1,2,3), weight=1)

        self.label = tk.Label(self.sizeframe, text='Toolbar', font=('Times New Roman', 15, 'bold'))
        self.label.grid(row=0, column=0, columnspan=3, sticky=tk.W+tk.E)
        self.rsize = tk.Button(self.sizeframe, width=15, text='Reset Size', command=self.resetsize)
        self.rsize.grid(row=1, column=1, columnspan=2)
        self.psize = tk.Button(self.sizeframe, text='+Size', command=self.incsize)
        self.psize.grid(row=2, column=1, sticky=tk.W+tk.E)
        self.dsize = tk.Button(self.sizeframe, text='-Size', command=self.decsize)
        self.dsize.grid(row=2, column=2, sticky=tk.W+tk.E)
        self.sizelabel = tk.Label(self.sizeframe, text=self.brushsize, font=('Arial', 10, 'bold'))
        self.sizelabel.grid(row=3, column=0, columnspan=4, sticky=tk.W+tk.E)
            #size frame - end

            #color frame - start
        self.colorframe = tk.Frame(self.btnframe, bd=1, bg='#000', relief=tk.RIDGE)
        self.colorframe.pack(padx=5, pady=5)
        self.colorframe.grid_columnconfigure((0,1,2), weight=1)

        self.label = tk.Label(self.colorframe, text='Colours', font=('Times New Roman', 15, 'bold'))
        self.label.grid(row=0, column=0, columnspan=3, sticky=tk.W + tk.E)
        self.palette = tk.Button(self.colorframe, text='Color Palette', command=self.openplt)
        self.palette.grid(row=1, column=1, columnspan=3, sticky=tk.W+tk.E)
        self.color1 = tk.Button(self.colorframe, text='1', bg='#000000', command=self.btncolor1)
        self.color1.grid(row=2, column=1, sticky=tk.W+tk.E)
        self.color2 = tk.Button(self.colorframe, text='2', bg='#000000', command=self.btncolor2)
        self.color2.grid(row=2, column=2, sticky=tk.W + tk.E)
            #color frame - end

            #file frame - start
        self.fileframe = tk.Frame(self.btnframe, relief=tk.RIDGE)
        self.fileframe.pack(padx=10, pady=10, side=tk.BOTTOM)
        self.fileframe.grid_columnconfigure((0,1), weight=1)

        self.clrbtn = tk.Button(self.fileframe, text='Clear', command=self.clear)
        self.clrbtn.grid(row=0, column=0, sticky=tk.W+tk.E)
        self.savebtn = tk.Button(self.fileframe, text='Save File', command=self.savefile)
        self.savebtn.grid(row=1, column=0, sticky=tk.W + tk.E)
            #file frame - end
        #toolbar frame - end

        self.root.protocol('WM_DELETE_WINDOW', self.on_closing)
        self.root.mainloop()

    def paint(self, event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        self.cnv.create_oval(x1, y1, x2, y2, outline=self.currentcolor, fill=self.currentcolor, width=self.brushsize)

    def resetsize(self):
        self.brushsize = 25
        self.sizelabel.config(text=self.brushsize)

    def incsize(self):
        self.brushsize += 5
        self.sizelabel.config(text=self.brushsize)

    def decsize(self):
        self.brushsize -= 5
        self.sizelabel.config(text=self.brushsize)

    def clear(self):
        self.cnv.delete('all')

    def openplt(self):
        _, self.currentcolor = colorchooser.askcolor()
        if self.argclr1 == 0 and self.argclr2 == 1:
            self.color1.config(bg=self.currentcolor)
            self.argclr1 += 1
            self.argclr2 -= 1
        elif self.argclr1 == 1 and self.argclr2 == 0:
            self.color2.config(bg=self.currentcolor)
            self.argclr1 -= 1
            self.argclr2 += 1


    def savefile(self):
        file = filedialog.asksaveasfilename(initialfile='untitled.png',
                                            defaultextension='.png',
                                            filetypes=[('PNG', 'JPG'), ['.png', '.jpg']])

    def on_closing(self):
        answer = messagebox.askyesnocancel(title='Save File?', message='Do you want to save your file?', parent=self.root)
        if answer is not None:
            if answer:
                self.savefile()
            self.root.destroy()
            exit(0)

    def btncolor1(self):
        self.currentcolor = self.color1.cget('bg')

    def btncolor2(self):
        self.currentcolor = self.color2.cget('bg')

Painter()