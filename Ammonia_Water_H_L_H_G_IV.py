#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 2024 23:50:00 

@author: aditya79
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_pdf import PdfPages
import mplcursors  # Import mplcursors library


x = np.linspace(0,1,1000)

def hL(T,x):
    h0 = 100
    T0 = 273.16
    m= [0,0,0,0,0,0,1,1,2,3,5,5,5,6,6,8]
    n= [1,4,8,9,12,14,0,1,1,3,3,4,5,2,4,0] 
    a=[-0.761080*10, +0.256905*(10**2), -0.247092*(10**3), +0.325952*(10**3), -0.158854*(10**3), +0.619084*(10**2),+0.114314*(10**2),+0.118157*10, +0.284179*10, +0.741609*10, +0.891844*(10**3), -0.161309*(10**4), +0.622106*(10**3), -0.207588*(10**3), -0.687393*10,+0.350716*10]
    q = 0
    for i in range(len(m)):
        q += a[i]*(((T/T0 - 1)**m[i])*(x**n[i]))      
    return(q*h0)


def Tx(p,x):
    T0 = 100
    p0 = 20
    m= [0,0,0,0,0,1,1,1,2,4,5,5,6,13]
    n= [0,1,2,3,4,0,1,2,3,0,0,1,0,1] 
    a=[0.322302*10, -0.384206*(10**0), 0.460965*(10**-1), -0.378645*(10**-2), 0.135610*(10**-3), 0.487755*(10**0), -0.120108*(10**0), 0.106154*(10**-1), -0.533589*(10**-3), +0.785041*10, -0.115941*(10**2), -0.523150*(10**-1), +0.489596*(10**1), 0.421059*(10**-1)]
    q = 0
    for i in range(len(m)):
        q += a[i]*((1-x)**m[i])*(np.log(p0/p)**n[i])  
    return(q*T0)

def Ty(p,y):
    p0=20
    T0=100
    m=[0,0,0,0,1,1,1,2,2,3,3,4,4,5,5,6,7]
    n=[0,1,2,3,0,1,2,0,1,0,1,0,2,0,2,0,2]
    a=[0.324004*(10), -0.395920, 0.435624*(10**-1), -0.218943*(10**-2), -0.143526*10, 0.105256*10, -0.719281*(10**-1), 0.122362*(10**2), -0.224368*(10), -0.201780*(10**2), 0.1108334*10, 0.145399*(10**2), 0.644312, -0.221246*(10), -0.756266, -0.135529*(10), 0.183541]
    q = 0
    for i in range(len(m)):
        q += a[i]*((1-y)**(m[i]/4))*(np.log(p0/p)**n[i])  
    return(q*T0)


def yy(p,x):
    p0=20
    m=[0,0,0,0,1,2,2,3,4,5,6,7,7,8]
    n=[0,1,6,7,0,1,2,2,3,4,5,6,7,7]
    a=[1.98022017*10, -1.18092669*10, 2.77479980*10, -2.88632477*10, -5.91616608*10, 5.78091305*(10**2), -6.21736743, -3.42198402*(10**3), 1.19403127*(10**4), -2.45413777*(10**4), 2.91591865*(10**4), -1.84782290*(10**4), 2.34819434*10, 4.80310617*(10**3)]
    q=0    
    for i in range (len(m)):
        q+=a[i]*((p/p0)**m[i])*(x**(n[i]/3))
    q=np.log(1-x+0.00001)*q
    q=np.exp(q)
    return(1-q)

def hG(T,y):
    h0=1000
    T0=324
    a= [1.28827, 0.125247, -2.08748, 2.17696, 2.35687, -8.86987, 10.2635, -2.37440, -6.70515, 16.4508, -9.36849, 8.42254, -8.58807, -2.77049, -0.961248, 0.988009, 0.308482]
    m= [0,1,2,3,0,1,2,3,0,1,2,0,1,0,4,2,1]
    n= [0,0,0,0,2,2,2,2,3,3,3,4,4,5,6,7,10]
    q = 0
    for i in range(len(m)):
        q += a[i]*((1 - T/T0)**m[i])*((1-y)**(n[i]/4))   
    return(q*h0)
    
class FunctionPlotter:
    def __init__(self, master):
        self.master = master
        self.master.title("Function Plotter")

        self.figure, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        functions = ["hL(Tx(p, x), x)", "hG(Tx(p, x), yy(p, x))", "hG(Ty(p, yy(p, x)), yy(p, x))"]
        self.function_var = tk.StringVar(value=functions[0])

        function_label = ttk.Label(master, text="Select Function:")
        function_label.pack(pady=5)
        self.function_menu = ttk.Combobox(master, values=functions, textvariable=self.function_var)
        self.function_menu.pack(pady=5)

        pressure_label = ttk.Label(master, text="Pressure (p):")
        pressure_label.pack(pady=5)
        self.pressure_var = tk.DoubleVar(value=1.0)
        self.pressure_entry = ttk.Entry(master, textvariable=self.pressure_var)
        self.pressure_entry.pack(pady=5)

        self.grid_var = tk.StringVar(value="Fine")
        grid_label = ttk.Label(master, text="Grid Lines:")
        grid_label.pack(pady=5)
        self.grid_menu = ttk.Combobox(master, values=["Fine", "Coarse"], textvariable=self.grid_var)
        self.grid_menu.pack(pady=5)

        self.print_button = ttk.Button(master, text="Print to File", command=self.print_to_file)
        self.print_button.pack(pady=10)

        self.plot_button = ttk.Button(master, text="Plot", command=self.plot_function)
        self.plot_button.pack(pady=10)

    def plot_function(self):
        try:
            p_value = self.pressure_var.get()
            x = np.linspace(0, 1, 1000)

            if "hL" in self.function_var.get():
                y = hL(Tx(p_value, x), x)
                self.ax.plot(x, y, label=f"{self.function_var.get()} (p={p_value})")

            elif "hG" in self.function_var.get():
                if "Tx" in self.function_var.get():
                    y = hG(Tx(p_value, x), yy(p_value, x))
                    self.ax.plot(x, y, label=f"{self.function_var.get()} (p={p_value})")

                elif "Ty" in self.function_var.get():
                    y = hG(Ty(p_value, yy(p_value, x)), yy(p_value, x))
                    self.ax.plot(yy(p_value, x), y, label=f"{self.function_var.get()} (p={p_value})")

            self.ax.legend()
            self.ax.set_xlabel("Liquid Concentration (mole fraction)")
            self.ax.set_ylabel("Enthalpy in kJ/kg")

            grid_type = self.grid_var.get().lower()
            if grid_type == "fine":
                self.ax.grid(True, linestyle="--", alpha=0.9)
            elif grid_type == "coarse":
                self.ax.grid(True, linestyle="--", alpha=0.2)
            # Add mplcursors for displaying coordinates at the mouse pointer
            mplcursors.cursor(hover=True)

            self.canvas.draw()

        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def print_to_file(self):
        try:
            filetypes = [("JPEG files", "*.jpg"), ("SVG files", "*.svg"), ("PDF files", "*.pdf")]
    
            filename = filedialog.asksaveasfilename(filetypes=filetypes, defaultextension=".jpg", title="Save Plot")
            if not filename:
                return  # User canceled the dialog
    
            # Ensure the correct file format extension
            format_extension = filename.split('.')[-1]
            if not format_extension:
                tk.messagebox.showwarning("Warning", "Please provide a filename with a valid format extension.")
                return
    
            # Save the plot in the selected format using matplotlib's asksavefig
            self.figure.savefig(filename, format=format_extension)
    
            tk.messagebox.showinfo("Save", f"Plot saved as '{filename}'.")
    
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred while saving the plot: {str(e)}")



def main():
    root = tk.Tk()
    app = FunctionPlotter(root)
    root.mainloop()

if __name__ == "__main__":
    main()