import tkinter as tk 
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

from api import get_historical, get_all_info, get_ids_info

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Cryptocurrency Tracker")
        self.root.geometry("1150x700")
        self.root.minsize(1050, 700)
        self.root.maxsize(1200,900)
        
        self.searchbox = tk.Entry(self.root)
        self.searchbox.grid(row=2, column=1, pady=10)

        self.searchbutton = tk.Button(self.root, text="Search Crypto!", command=self.show)
        self.searchbutton.grid(row=2, column=2, pady=10)

        self.fromlabel = tk.Label(self.root)
        self.fromlabel.config(text="From date (year, month, day)", justify="left")
        self.fromlabel.grid(row=3, column=1, pady=10, sticky="n")

        self.fyear = tk.Entry(self.root)
        self.fyear.grid(row=3, column=2, pady=10)
        self.fyear.config(width=10)

        self.fmonth = tk.Entry(self.root)
        self.fmonth.grid(row=3, column=3, pady=10, sticky="w")
        self.fmonth.config(width=10)

        self.fday = tk.Entry(self.root)
        self.fday.grid(row=3, column=4, pady=10, sticky="w")
        self.fday.config(width=10)

        self.tolabel = tk.Label(self.root)
        self.tolabel.config(text="To date (year, month, day)", justify="left")
        self.tolabel.grid(row=4, column=1, pady=10, sticky="n")

        self.tyear = tk.Entry(self.root)
        self.tyear.grid(row=4, column=2, pady=10, sticky="n")
        self.tyear.config(width=10)

        self.tmonth = tk.Entry(self.root)
        self.tmonth.grid(row=4, column=3, pady=10, sticky="w")
        self.tmonth.config(width=10)

        self.tday = tk.Entry(self.root)
        self.tday.grid(row=4, column=4, pady=10, sticky="w")
        self.tday.config(width=10)

        self.mlabel = tk.Label(self.root, text="Click 'Search Crypto' on empty search box for top 3 cryptos!")
        self.mlabel.grid(row=2, column=3, columnspan=4)
        self.mlabel.config(bg="white", width=55)

        self.oplabel = tk.Label(self.root, text="")
        self.oplabel.grid(column=4, columnspan=3, padx=10, pady=10)
        self.oplabel.config(bg="gray", height=20, width=35)

        self.redlabel = tk.Label(self.root, text="Ensure the last day of the month is\ncorrect or it won't work!",
                                 width=31,
                                 height=2,
                                 bg="red")
        self.redlabel.grid(column=5, row=3, rowspan=2)

        self.fig = Figure(figsize=(6, 5.2), dpi = 100)
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.root)
        self.canvas.get_tk_widget().grid(row=5, column=1, columnspan=3, padx=10)

    def show(self):
        if self.searchbox.get():
            self.fig.clear()
            self.oplabel.config(text="")
            self.mlabel.config(text="")

            time.sleep(0.3)

            try:
                x_values, y_values, frm, to, ids = get_historical(self.searchbox.get(), (int(self.fyear.get()), int(self.fmonth.get()), int(self.fday.get())), (int(self.tyear.get()), int(self.tmonth.get()), int(self.tday.get())))
                ids_info = get_ids_info(self.searchbox.get())
                pl1 = self.fig.add_subplot()
                pl1.plot(x_values, y_values)
                pl1.set_title(f"Value of {ids.capitalize()} from {frm[0], frm[1], frm[2]} to {to[0], to[1], to[2]}")

                self.oplabel.config(text=f"--TARGETED RANGE--\nHighest in range: {round(max(y_values), 2)}\nLowest in range: {round(min(y_values), 2)}\n\n-- IN 24H --\nPrice Change%: {round(ids_info[1],2)}%\nLowest Price: ${ids_info[2]}\nHighest Price: ${ids_info[3]}\n\nCurrent Price: ${ids_info[4]}\n\n--OTHERS in 24H--\nCirculating Supply: {ids_info[5]}\nMarket Cap: ${ids_info[6]}\nMarket Cap Change%: {round(ids_info[7], 2)}%", 
                                    anchor="n", 
                                    fg="white",
                                    justify="left")

                self.canvas = FigureCanvasTkAgg(self.fig, master = self.root)
                self.canvas.draw()
                self.canvas.get_tk_widget().grid(row=5, column=1, columnspan=3, padx=10)
            except KeyError:
                self.mlabel.config(text="Crypto doesn't exist or dates are not within one year from now!")
            except ValueError:
                self.mlabel.config(text="Dates must be in integer and not a string/float")
        else:
            self.mlabel.config(text="Entry box is empty!", anchor="n")
            general = get_all_info()
            format = '--TOP 3 IN 24H--\n'
            for crypto in general:
                a, b, c, d, e = crypto
                format += f'{a}\nPRICE CHANGE % IN 24H - {round(b,2)}%\nLOWEST IN 24H - ${round(c,5)}\nHIGHEST IN 24H - ${round(d,5)}\nCURRENT PRICE - ${round(e,5)}\n\n' 
            
            self.oplabel.config(text=format, justify="left", fg="white")