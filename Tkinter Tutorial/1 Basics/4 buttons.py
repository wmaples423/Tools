import tkinter as tk
from tkinter import ttk

# setup
window = tk.Tk()
window.title('buttons')
window.geometry('600x400')

# button
def button_func():
    print('a basic button')
    print(radio_var.get())

button_string = tk.StringVar(value = 'A button with string var')
button = ttk.Button(window, text = 'A simple button', command= button_func, textvariable=button_string)
button.pack()

# check button
check_var = tk.IntVar(value = 10)
check1 = ttk.Checkbutton(
    window, 
    text= 'check box 1', 
    command=lambda: print(check_var.get()), 
    variable=check_var,
    onvalue= 10,
    offvalue=5)
check1.pack()

check2 = ttk.Checkbutton(
    window,
    text = 'Checkbox 2',
    command = lambda: check_var.set(5)
)
check2.pack()

# radio buttons
radio_var = tk.StringVar()
radio1 = ttk.Radiobutton(
    window, 
    text = 'Radiobutton 1', 
    value = 'radio 1',
    variable=radio_var, 
    command = lambda: print(radio_var.get())
)
radio1.pack()
radio2 = ttk.Radiobutton(
    window, 
    text = 'Radiobutton 2', 
    value = 2,
    variable= radio_var
)
radio2.pack()

# exercise

def radio_func():
    print(check_bool.get())
    check_bool.set(False)

# data
radio_string = tk.StringVar()
check_bool = tk.BooleanVar()

#widgets
ex_radio1 = ttk.Radiobutton(
    window,
    text = 'Radio A',
    value = 'A',
    command=radio_func,
    variable=radio_string
)

ex_radio2 = ttk.Radiobutton(
    window, 
    text = 'Radio B',
    value = 'B',
    command=radio_func,
    variable=radio_string
)

ex_check = ttk.Checkbutton(
    window,
    text = 'exercise check',
    variable= check_bool,
    command=lambda: print(radio_string.get())
)

# layout
ex_radio1.pack()
ex_radio2.pack()
ex_check.pack()

# run
window.mainloop()