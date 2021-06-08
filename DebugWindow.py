import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# black
BGcolor = "#272727"

# grey
color1 = "#747474"

# red
color2 = "#FF652F"

# yellow
color3 = "#FFE400"

# green
color4 = "#14A76C"

BFSize = 15
BFFamily = "Verdana"
BFont = (BFFamily, BFSize)
pad = 7
pad2 = 2

def childWindow(window):
    child = tk.Toplevel(window)
    child.config(bg='#272727')
    child.rowconfigure([0, 1, 2], weight=1)
    child.columnconfigure(0, weight=1, minsize=50)
    child.title("Debug Window")
    child.geometry("800x480")

    frame1 = tk.Frame(master=child, width=800, height=140, bg=color2)
    frame1.grid(row=0, sticky="nsew", padx=5, pady=5)


    frame2 = tk.Frame(master=child, width=800, height=140,
                      borderwidth=5, bg=color1)
    frame2.grid(row=1, sticky="nsew", padx=5, pady=5)

    frame3 = tk.Frame(master=child, width=800, height=200, bg=color1)
    frame3.grid(row=2, sticky="nsew", padx=10, pady=10)
