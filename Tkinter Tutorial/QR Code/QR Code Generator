import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import qrcode

class App(ctk.CTk):
    def __init__(self):
        
        # window setup
        ctk.set_appearance_mode('light')
        super().__init__(fg_color = 'white')

        # customization
        self.title('')
        self.iconbitmap("C:\\Users\\MaplesWi\\OneDrive - Clayton Homes\\Desktop\\Tools\\Tools\\1 qr\\3 qr image\\empty.ico")
        self.geometry('400x400')

        # entry field
        # ! self.en
        EntryField(self)

        # QR code
        raw_image = Image.open("C:\\Users\\MaplesWi\\OneDrive - Clayton Homes\\Desktop\\Tools\\Tools\\1 qr\\3 qr image\\Placeholder.png").resize((200,200))
        tk_image = ImageTk.PhotoImage(raw_image)
        self.qr_image = QrImage(self)
        self.qr_image.update_image(tk_image)

        # running the loop
        self.mainloop()

class EntryField(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, corner_radius = 20, fg_color='#021FB3')
        self.place(relx=0.5, rely=1, relwidth=1, relheight=0.4, anchor='center')

        # grid layout
        self.rowconfigure((0,1), weight = 1, uniform='a')
        self.columnconfigure(0, weight =1, uniform='a')


        # widgets
        self.frame = ctk.CTkFrame(self, fg_color='transparent')
        self.frame.columnconfigure(0, weight = 1, uniform= 'b')
        self.frame.columnconfigure(1, weight = 4, uniform= 'b')
        self.frame.columnconfigure(2, weight = 2, uniform= 'b')
        self.frame.columnconfigure(3, weight = 1, uniform= 'b')
        self.frame.grid(row=0, column=0)

        entry = ctk.CTkEntry(self.frame, fg_color='#2E54E8', border_width = 0, text_color='white')
        entry.grid(row=0, column =1, sticky = 'nsew')

        button = ctk.CTkButton(self.frame, text = 'save', fg_color='#2E54E8', hover_color='#4266f1')
        button.grid(row=0, column=2, sticky = 'nsew', padx = 10)

class QrImage(tk.Canvas):
    def __init__(self,parent):
        super().__init__(master = parent, 
            background = 'red', 
            bd=0, 
            highlightthickness=0, 
            relief='ridge')
        self.place(relx = 0.5, rely= 0.4, width=200, height=200, anchor='center')

    def update_image(self, image_tk):
        self.create_image(0,0,image = image_tk, anchor='nw')

App()