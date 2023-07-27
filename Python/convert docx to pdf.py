from docx2pdf import convert
from os import listdir
from os.path import isfile, join
import ctypes
from tkinter import filedialog
from tkinter import *
import os

#convert all files in location to pdf
root = Tk()
root.withdraw()
ctypes.windll.user32.MessageBoxW(0, "Select OK to choose the folder containing the Word documents you wish to convert to PDF.", "Complete", 0)
word_path = filedialog.askdirectory()
ctypes.windll.user32.MessageBoxW(0, "Select OK to choose the file folder where you want to save your PDFs.", "Complete", 0)
pdf_path = filedialog.askdirectory()
convert(word_path, pdf_path)

filenames = []
directory = r"folder\path"
for filename in os.listdir(directory):
    if filename.lower().endswith(".pdf"):
        filenames.append(os.path.join(directory, filename))