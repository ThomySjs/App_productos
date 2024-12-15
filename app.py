import customtkinter as ctk
import tkinter as tk
from CTkMessagebox import CTkMessagebox
from PIL import Image, ImageTk
from entities.user import user
from Database.Qmanager import sign_in, register, get_session_data
import requests
import os
from dotenv import load_dotenv

class MainScreen(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__()
        ctk.set_appearance_mode('dark')
        load_dotenv()
        self.title('Menu manager')
        self.resizable(0, 0)
        self.session = []
        self.Resolution(width = 1280, height =  720)

    def Resolution(self, *args, **kwargs):
        for widget in self.winfo_children():
            widget.destroy()

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.columnconfigure(0, weight=2, uniform='a')
        self.main_frame.columnconfigure(1, weight=1, uniform='a')
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.pack(expand=True, fill='both')
        
        self.form_frame = ctk.CTkFrame(self.main_frame)
        self.image_frame = ctk.CTkFrame(self.main_frame)
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
            res_menu.set(f'{width}x{height}')

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

        #Set the app resolution and place it in the middle of the screen
        self.geometry('%dx%d+%d+%d' % (self.width, self.height, self.x, self.y))
        self.update()
        self.loguin_widgets()
        self.image_widget()
        

    def image_widget(self, *args, **kwargs):

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

    def loguin_widgets(self, *args):
        #Delete previous self.form_frame widgets that are not CTkComboBox
        for widget in self.form_frame.winfo_children():
            if not isinstance(widget, ctk.CTkComboBox):
                widget.destroy()

        width = int(self.form_frame.winfo_width() / 1.3)

        #Variables
        email = ctk.StringVar()
        password = ctk.StringVar()
        
        #Widgets
        label_mail = ctk.CTkLabel(self.form_frame, text='Email', font=('Arial', 24), text_color='white')
        label_password = ctk.CTkLabel(self.form_frame, text='Password', font=('Arial', 24), text_color='white')

        entry_mail = ctk.CTkEntry(self.form_frame, placeholder_text='example@gmail.com', textvariable=email, width=width, height=45, font=('Arial', 18))
        entry_password = ctk.CTkEntry(self.form_frame, textvariable=password, show='*', width=width, height=45, font=('Arial', 18))

        login_button = ctk.CTkButton(self.form_frame, text='Login', fg_color='green', width=width, height=40,  command=lambda: self.login_verificacion(email=email.get(), password=password.get()))

        register_button = ctk.CTkButton(self.form_frame, text='Register', width=width, height=40, command=self.register_widgets)
        
        #Layout
        label_mail.pack(pady = (150,5))
        entry_mail.pack(pady= 5)
        label_password.pack(pady = 5)
        entry_password.pack(pady=5)
        login_button.pack(pady=10)
        register_button.pack(pady=40)

    def register_widgets(self, *args):
        #Delete previous self.form_frame widgets that are not CTkComboBox
        for widget in self.form_frame.winfo_children():
            if not isinstance(widget, ctk.CTkComboBox):
                widget.destroy()

        width = int(self.form_frame.winfo_width() / 1.3)

        #Variables
        name = ctk.StringVar()
        email = ctk.StringVar()
        password = ctk.StringVar()
        
        #Widgets
        label_name = ctk.CTkLabel(self.form_frame, text='Name', font=('Arial', 24), text_color='white')
        label_mail = ctk.CTkLabel(self.form_frame, text='Email', font=('Arial', 24), text_color='white')
        label_password = ctk.CTkLabel(self.form_frame, text='Password', font=('Arial', 24), text_color='white')

        entry_name = ctk.CTkEntry(self.form_frame, textvariable=name, width=width, height=45, font=('Arial', 18) )
        entry_mail = ctk.CTkEntry(self.form_frame, placeholder_text='example@gmail.com', textvariable=email, width=width, height=45, font=('Arial', 18))
        entry_password = ctk.CTkEntry(self.form_frame, textvariable=password, show='*', width=width, height=45, font=('Arial', 18))

        register_button = ctk.CTkButton(self.form_frame, text='Register', fg_color='green', width=width, height=40,  command=lambda: self.register_verification(name = name.get(), email=email.get(), password=password.get()))

        login_button = ctk.CTkButton(self.form_frame, text='Sign In', width=width, height=40, command=self.loguin_widgets)
        
        #Layout
        label_name.pack(pady = (150,5))
        entry_name.pack(pady = 5)
        label_mail.pack(pady = 5)
        entry_mail.pack(pady= 5)
        label_password.pack(pady = 5)
        entry_password.pack(pady=5)
        register_button.pack(pady=10)
        login_button.pack(pady=40)

    def control_panel(self, *args, **kwargs):
        if self.session:
            #Delete previous self.form_frame widgets that are not CTkComboBox
            for widget in self.main_frame.winfo_children():
                widget.destroy()

            navbar_frame = ctk.CTkFrame(self.main_frame)
            data_frame = ctk.CTkFrame(self.main_frame)
            table_frame = ctk.CTkFrame(self.main_frame)


            navbar_frame.pack(side='left', fill='y')
            data_frame.pack(side='left', expand=True, fill='both')
            table_frame.pack(side='left', expand=True, fill='both')

            #navbar
            create_button = ctk.CTkButton(navbar_frame, fg_color='green')
            modify_button = ctk.CTkButton(navbar_frame, fg_color='blue')
            delete_button = ctk.CTkButton(navbar_frame, fg_color='red')

            create_button.pack(pady=10)
            modify_button.pack(pady=10)
            delete_button.pack(pady=10)

            


    def send_email(self, *args):
        email = {'email' : args[0]}

        r = requests.post(os.getenv('VERIFICATION_ROUTE'), json=email)
        if r.status_code == 200:
            CTkMessagebox(self, message='Email sent')
        else:
            CTkMessagebox(self, message='An error ocurred.')


    def login_verificacion(self,*args, **kwargs):
        state, msg =  sign_in(kwargs['email'], kwargs['password'])
        if state:
            query_accepted, data = get_session_data(kwargs['email'])
            user_id = data[0]
            user_name = data[1]
            verified = data[2]
            if query_accepted:
                if verified:

                    user_session = user(user_id, user_name, kwargs['email'])
                    self.session.append(user_session)
                    self.control_panel()
                else:
                    option = CTkMessagebox(self, message='Email verification required.', option_1='Cancel', option_2='Send email')
                    if option.get() == 'Send email':
                        self.send_email(kwargs['email'])
            else: 
                CTkMessagebox(self, message=data)
        else:
            CTkMessagebox(self, message=msg)

    def register_verification(self, *args, **kwargs):
        state, msg = register(kwargs['name'], kwargs['email'], kwargs['password'])
        if state:
            CTkMessagebox(self, message=msg)
        else:
            CTkMessagebox(self, message=msg)




if __name__ == "__main__":
    app = MainScreen()
    app.mainloop()