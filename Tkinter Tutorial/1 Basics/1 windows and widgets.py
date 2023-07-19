import tkinter as tk
from tkinter import ttk

def button_func():
    print('a button was pressed')

def hello():
    print('hello')

# create window
window = tk.Tk()
window.title('Window and Widgets')
window.geometry('800x500')

# ttk label
label = ttk.Label(master= window, text = 'This is a test')
label.pack()

# tk text
text = tk.Text(master= window)
text.pack()

# ttk entry
entry = ttk.Entry(master= window)
entry.pack()

my_label = ttk.Label(master=window, text = 'hello')
my_label.pack()

# ttk button
button = ttk.Button(master=window, text = 'A button', command=button_func)
button.pack()

#my_button = ttk.Button(master=window, text = 'hello', command=hello)
my_button = ttk.Button(master=window, text = 'hello', command=lambda: print('hello'))
my_button.pack()


# run
window.mainloop()