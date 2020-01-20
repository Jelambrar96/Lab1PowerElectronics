#
#
#
#
#
#

import os
import sys


from tkinter import filedialog
from tkinter import Tk
from tkinter import Label
from tkinter import LabelFrame
from tkinter import ttk
from tkinter import Text
from tkinter import Button
from tkinter import Spinbox


import tkinter as tk

import numpy as np
from matplotlib import pyplot as plt


from osc_files import CSVReader
from waveform_analysis import WaveAnalizer


class CSVLabel(LabelFrame):

    def __init__(self, *args, **kwargs):

        super(CSVLabel, self).__init__(*args, **kwargs)

        self._filename = ""        

        label = Label(self, text="File: ")
        # label.pack(padx=10, pady=5, side=tk.LEFT)
        label.grid(row=0, column=0, padx=10, pady=5)

        self._textbox = Text(self, height=1, width=57)
        # self._textbox.pack(padx=10, pady=5, side=tk.LEFT)
        self._textbox.grid(row=0, column=1, padx=10, pady=5)

        fileselector = Button(self, text = "Browse",command = self.fileDialog)
        fileselector.grid(row=0, column=2, padx=10, pady=5)
        
        # fileselector.pack(padx=10, pady=5, side=tk.LEFT)


    def fileDialog(self):

        temp_filename = filedialog.askopenfilename(initialdir =  ".", title = "Select A File", filetypes = (("csv files","*.[c-C][s-S][v-V]"),("all files","*.*")) )
        # self._filename = filedialog.askopenfilename(initialdir =  "/", title = "Select A File")
        # self._textbox.delete(tk.START, tk.END)
        if temp_filename:
            self.filename = temp_filename
            self._textbox.delete("1.0", tk.END)
            self._textbox.insert(tk.END, self._filename)

    def getFilename(self):
        return self._textbox.get("1.0", tk.END)[:-1]



class App(Tk):

    def __init__(self):
        
        Tk.__init__(self)

        ##### OPTIONS
        self._frequency = tk.IntVar()
        self._frequency.set(60)
        
        self._plot_figures = tk.BooleanVar()
        self._plot_figures.set(True)
        
        self._voltage_filename = ""
        self._current_filename = ""

        self._voltage_scale = tk.StringVar()
        self._voltage_scale.set("50")
        self._current_scale = tk.DoubleVar()
        self._current_scale.set(50)
        
        self._div_per_second = tk.IntVar()
        self._div_per_second.set(10)

        ##### windows setup
        
        self.geometry("640x480")
        self.resizable(width=False, height=False)

        self.title("Power Electronic App")
        
        self.voltagelabel = CSVLabel(self, text="Voltage")
        # self.voltagelabel.pack(fill=tk.X)
        self.voltagelabel.grid(row=1, column=0, columnspan=2)

        self.currentlabel = CSVLabel(self, text="Current")
        # self.currentlabel.pack(fill=tk.X)
        self.currentlabel.grid(row=2, column=0, columnspan=2)
        
        # pass

        options_labelframe = LabelFrame(self, text="Options")

        tk.Label(options_labelframe, text="Frequency: ", justify = tk.LEFT, padx = 20).pack()
        rb50 = tk.Radiobutton(options_labelframe, text="50 Hz", padx = 20, variable=self._frequency, value=50) 
        rb50.pack(anchor=tk.W)
        rb60 = tk.Radiobutton(options_labelframe, text="60 Hz (default)", padx = 20, variable=self._frequency, value=60)
        rb60.pack(anchor=tk.W)

        values_spinbox = [1] + [ round(item * 0.001, 3) for item in range(1, 100 * 1000)]

        vlabel = Label(options_labelframe, text="Voltage Scale: ")
        vlabel.pack()
        self._voltage_spin = Spinbox(options_labelframe, values=values_spinbox)
        self._voltage_spin.pack()
        
        clabel = Label(options_labelframe, text="Current Scale: ")
        clabel.pack()
        self._current_spin = Spinbox(options_labelframe, values=values_spinbox)
        self._current_spin.pack()
        
        tk.Label(options_labelframe, text="Sample period: ", justify = tk.LEFT, padx = 20).pack()
        sp5 = tk.Radiobutton(options_labelframe, text="5 ms/div", padx = 20, variable=self._div_per_second, value=5) 
        sp5.pack(anchor=tk.W)
        sp10 = tk.Radiobutton(options_labelframe, text="10 ms/div (default)", padx = 20, variable=self._div_per_second, value=10)
        sp10.pack(anchor=tk.W)
        sp20 = tk.Radiobutton(options_labelframe, text="20 ms/div", padx = 20, variable=self._div_per_second, value=20)
        sp20.pack(anchor=tk.W)
    
        check_button = tk.Checkbutton(options_labelframe, text="Plot figures.", 
            variable=self._plot_figures, padx = 20)
        check_button.pack()
        
        button = Button(options_labelframe, text = "Compute",command = self.compute)
        button.pack()

        options_labelframe.grid(row=3, column=0)
        
        compute_button = ""
        
        output_label_frame = LabelFrame(self, text="Output")
        self._output_text = Text(output_label_frame, height=12, width=32) # , state='disabled') 
        self._output_text.pack(padx=10, pady=10, side=tk.LEFT)
        output_label_frame.grid(row=3, column=1)
        # output_label_frame.pack(padx=10, pady=10, side=tk.LEFT)

    def compute(self):

        if not self.voltagelabel.getFilename():
            self.popupBonus("Error", "ERROR:\n Voltage CSV file is not inserted!")
            return
        
        if not os.path.isfile(self.voltagelabel.getFilename()):
            self.popupBonus("Error", "ERROR:\n Voltage CSV file does not exist!")
            return
        
        if not self.currentlabel.getFilename():
            self.popupBonus("Error", "ERROR:\n Current CSV file is not inserted!")
            return
        
        if not os.path.isfile(self.currentlabel.getFilename()):
            self.popupBonus("Error", "ERROR:\n Current CSV file does not exist!")
            return
        
        csv_reader = CSVReader(self.voltagelabel.getFilename(), self.currentlabel.getFilename())
        try:
            csv_reader.calcData()
        except Exception as e:
            self.popupBonus("ERROR", "" + e)
            return

        time_array, voltage_array, current_array = csv_reader.getData()

        # 250 dots / div * 16.66ms / 10ms/div
        n_one_period = int(round(250 * 1000.0/ (self._frequency.get() * self._div_per_second.get())))
        
        analizer = WaveAnalizer(voltage_array, current_array, time_array, n_one_period)
        analizer.compute()
        print(analizer.getOutputString())
        
        self._output_text.delete(1.0, tk.END)
        self._output_text.insert(tk.END, analizer.getOutputString())
        
        
        if self._plot_figures.get():
            # plt.show()
            analizer.plot()


    def popupBonus(self, title="title", message="ERROR"):
        """
        popupBonusWindow = tk.Tk()
        popupBonusWindow.wm_title(tittle)
        labelBonus = Label(popupBonusWindow, text=message)
        labelBonus.grid(row=0, column=0)
        B1 = ttk.Button(popupBonusWindow, text="Accept", command=popupBonusWindow.destroy())
        B1.pack()
        """
        popup = tk.Toplevel()
        popup.title(title)
        popup.geometry("240x180")
        popup.resizable(width=False, height=False)
        label = tk.Label(popup, text=message, wraplength=235) #Can add a font arg here
        label.pack(side="top", fill="x", pady=10)
        B1 = tk.Button(popup, text="Accept", command = popup.destroy)
        B1.pack()
        popup.mainloop()


if __name__ == '__main__':
    root = App()
    root.mainloop()


# root = App()
# root.filename = filedialog.askopenfilename()
# print (root.filename)
# root.mainloop()
