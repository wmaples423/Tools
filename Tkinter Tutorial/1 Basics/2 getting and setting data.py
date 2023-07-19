import tkinter as tk
from tkinter import ttk

def button_func():
    # get content of the entry
    entry_text = entry.get()

    # update the label
    # label.configure(text = 'some other text')
    label['text'] = entry_text
    entry['state'] = 'disabled'
    # print(label.configure())

# window
window = tk.Tk()
window.title('Getting and setting widgets')

# widgets
label = ttk.Label(master=window, text = 'Some text')
label.pack()

entry = ttk.Entry(master=window)
entry.pack()

button = ttk.Button(master=window, text = 'The button', command=button_func)
button.pack()

# * exercise
def reset_func():
    label['text'] = 'some text'
    entry['state'] = 'enabled'

exercise_button = ttk.Button(master = window, text = 'Excercise button', command = reset_func)
exercise_button.pack()

# run
window.mainloop()