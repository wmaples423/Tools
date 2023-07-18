import tkinter as tk
from tkinter import ttk

def button_func():
    print(string_var.get())
    string_var.set('button pressed')

# window
window = tk.Tk()
window.title('Tkinter variables')

#tkinter variable
string_var = tk.StringVar()

# widgets
label = ttk.Label(master= window, text = 'label', textvariable=string_var)
label.pack()

entry = ttk.Entry(master= window, textvariable=string_var)
entry.pack()

button = ttk.Button(master=window, text='button', command=button_func)
button.pack()

# exercises
ex_string = tk.StringVar(value = 'test')

ex_entry = ttk.Entry(master=window,textvariable=ex_string)
ex_entry.pack()

ex_entry2 = ttk.Entry(master=window,textvariable=ex_string)
ex_entry2.pack()

ex_label = ttk.Label(master=window, text='label',textvariable=ex_string)
ex_label.pack()

# run
window.mainloop()