import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk


class MS(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.title('Prueba')
        self.resizable(0, 0)
        self.columnconfigure(0, weight=2, uniform='a')
        self.columnconfigure(1, weight=1, uniform='a')
        self.rowconfigure(0, weight=1)

        #Main frame

        self.Resolution(width = 1280, height =  720)

    def Resolution(self, *args, **kwargs):
        for widget in self.winfo_children():
            widget.destroy()

        self.form_frame = ctk.CTkFrame(self)
        self.image_frame = ctk.CTkFrame(self)
        self.form_frame.grid(row=0, column=1, sticky='nswe')
        self.image_frame.grid(row=0, column=0, sticky='nswe')

        self.image_frame.columnconfigure(0, weight=1)
        self.image_frame.rowconfigure(0, weight=1)

        #Resolution menu
        res_menu = ctk.CTkComboBox(self.form_frame, values= ['1280x720', '1176x664', '1152x864', '1024x768', '800x600'], command=self.Resolution)
        res_menu.pack(pady=10,padx=10)

        #kwargs for inicialization
        if kwargs:
            width = kwargs['width']
            height = kwargs['height']
            res_menu.set(f'{kwargs['width']}x{kwargs['height']}')

        #args when the function is called by the comobox
        else:
            width, height = args[0].split('x')
            width = int(width)
            height = int(height)
            res_menu.set(args[0])

        #This captures the w and h of the users screen 
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        # w and h of the window (app)
        self.width = width
        self.height = height

        #get the center of the screen and place the app there
        self.x = (self.screen_width / 2) - (self.width / 2)
        self.y = (self.screen_height / 2) - (self.height / 2)

        self.geometry('%dx%d+%d+%d' % (self.width, self.height, self.x, self.y))
        self.Loguin()
        self.Image()
        

    def Image(self, *args, **kwargs):

        #This deletes every widget(in this case image) everytime this function is called
        #keeping just 1 image at the time 
        for widget in self.image_frame.winfo_children():
            widget.destroy()


        width = self.image_frame.winfo_width()
        height = self.image_frame.winfo_height()
        
        #loading the image
        image = Image.open('static/Fondo.jpg').resize((width,height))
        image_tk = ImageTk.PhotoImage(image)
        
        #Canvas to place the image in it
        canvas_image = tk.Canvas(self.image_frame, bd=0, highlightthickness=0, relief='ridge')
        canvas_image.grid(row=0, column=0, sticky='nwse')
        canvas_image.create_image(0,0, image=image_tk, anchor='nw')

        #This prevents the image to be garbage collected
        canvas_image.image = image_tk

    def Loguin(self, *args):
        
        self.update()
        width = int(self.form_frame.winfo_width() / 1.3)

        mail = ctk.StringVar()
        password = ctk.StringVar()
        
        label_mail = ctk.CTkLabel(self.form_frame, text='Mail', font=('Arial', 24), text_color='white')
        label_password = ctk.CTkLabel(self.form_frame, text='Password', font=('Arial', 24), text_color='white')



        entry_mail = ctk.CTkEntry(self.form_frame, placeholder_text='example@gmail.com', textvariable=mail, width=width, height=45, font=('Arial', 18))
        entry_password = ctk.CTkEntry(self.form_frame, textvariable=password, show='*', width=width, height=45, font=('Arial', 18))

        Login_button = ctk.CTkButton(self.form_frame, text='Login', fg_color='green', width=width, height=40,  command=lambda: print(mail.get()))
        
        label_mail.pack(pady = (150,5))
        entry_mail.pack(pady= 5)
        label_password.pack(pady = 5)
        entry_password.pack(pady=5)
        Login_button.pack(pady=10)

    


if __name__ == "__main__":
    app = MS()
    app.mainloop()