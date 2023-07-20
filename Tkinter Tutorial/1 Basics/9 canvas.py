import tkinter as tk
from tkinter import ttk

# setup
window = tk.Tk()
window.geometry('600x400')
window.title('Canvas')

#
canvas = tk.Canvas(window, bg = 'white')
canvas.pack()

canvas.create_rectangle((50, 20, 100, 200), fill = 'red', width=10, dash = (4,2), outline='purple')

# run
window.mainloop()
