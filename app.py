import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
from PIL import Image, ImageTk
from entities.user import user
from Database.Qmanager import Products, Users, Log
from datetime import datetime

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
        self.current_window = None

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

        #args when the function is called by the combobox
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
     
    ########## Widgets ##########

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

            self.navbar_frame = ctk.CTkFrame(self.main_frame, bg_color='#121212', fg_color='#121212')
            self.data_frame = ctk.CTkFrame(self.main_frame, bg_color='#383838', fg_color='#383838')
            self.table_frame = ctk.CTkFrame(self.main_frame, bg_color='#383838', fg_color='#383838')

            self.navbar_frame.pack(side='left', fill='y')
            self.data_frame.pack(side='left', fill='y')
            self.table_frame.pack(side='left', expand=True, fill='both')
            
            self.navbar()
            self.form_data('Create')    
            self.table('product_id')

    def navbar(self, *args):
        width = int(self.winfo_width() * 0.025)

        for widget in self.navbar_frame.winfo_children():
                widget.destroy()
        
        create_image = ctk.CTkImage(dark_image=Image.open('static/Create.png'))
        delete_image = ctk.CTkImage(dark_image=Image.open('static/Delete.png'))
        modify_image = ctk.CTkImage(dark_image=Image.open('static/Modify.png'))
        log_image = ctk.CTkImage(dark_image=Image.open('static/Log.png'))
        
        create_button = ctk.CTkButton(self.navbar_frame, image=create_image, bg_color='#121212', fg_color='#121212', width=width, text='', command=lambda: self.form_data('Create'))
        modify_button = ctk.CTkButton(self.navbar_frame, image=modify_image, bg_color='#121212', fg_color='#121212', width=width, text='', command=lambda: self.form_data('Modify'))
        delete_button = ctk.CTkButton(self.navbar_frame, image=delete_image, bg_color='#121212', fg_color='#121212', width=width, text='', command=lambda: self.form_data('Delete'))
        log_button = ctk.CTkButton(self.navbar_frame, image=log_image, bg_color='#121212', fg_color='#121212', width=width, text='', command=lambda: self.form_data('Log'))

        create_button.pack(pady=(20, 10), padx=10)
        modify_button.pack(pady=10, padx=10)
        delete_button.pack(pady=10, padx=10)
        log_button.pack(pady=10, padx=10)

    def form_data(self, *args):
        width = int(self.winfo_width() * 0.05)
        if args:
                option = args[0]
        else:
            option = 'Create'

        #Variables
        product_id = ctk.IntVar(value='')
        name = ctk.StringVar()
        price = ctk.DoubleVar(value='')
        description = ctk.StringVar()
        category = ctk.StringVar()
        available = ctk.BooleanVar()

        #Self.current_window prevents the user from overloading the app with queries by pressing the same button multiple times
        if option == 'Modify' and self.current_window != 'Modify':

            for widget in self.data_frame.winfo_children():
                widget.destroy()
            
            # This changes the table content only when the previous section of the app was Log
            if self.current_window == 'Log':
                self.table('product_id')

            self.current_window = 'Modify'
            #Form/data
            product_id_label = ctk.CTkLabel(self.data_frame, text='ID', font=('Arial', 20))
            product_name_label = ctk.CTkLabel(self.data_frame, text='Product name', font=('Arial', 20))
            product_price_label = ctk.CTkLabel(self.data_frame, text='Price', font=('Arial', 20))
            product_desc_label = ctk.CTkLabel(self.data_frame, text='Description', font=('Arial', 20))
            product_category_label = ctk.CTkLabel(self.data_frame, text='Category', font=('Arial', 20))
            product_available_label = ctk.CTkLabel(self.data_frame, text='Available', font=('Arial', 20))

            product_id_entry = ctk.CTkEntry(self.data_frame, textvariable=product_id, font=('Arial', 24), height=40, width=width*3)
            product_name_entry = ctk.CTkEntry(self.data_frame, textvariable=name, font=('Arial', 20), height=40, width=width*3)
            product_price_entry = ctk.CTkEntry(self.data_frame, textvariable=price, font=('Arial', 20), height=40, width=width*3)
            product_desc_entry = ctk.CTkTextbox(self.data_frame, font=('Arial', 20), border_color='gray50', border_width=2, height=100)
            product_category_entry = ctk.CTkOptionMenu(self.data_frame, values=['Para acompañar', 'Pastelería', 'Sándwich Salados', 'Sin tacc', 'Café', 'Café gourmet', 'Té y otros', 'Promos cafetería'], variable=category, height=40, width=width*3 , font=('Arial', 18), fg_color='#434447', button_color='#353638', button_hover_color='#252627')
            product_available_entry = ctk.CTkCheckBox(self.data_frame, variable=available, text='')

            product_desc_button = ctk.CTkButton(self.data_frame, text='save',  command=lambda: description.set(product_desc_entry.get(1.0, "end-1c") ), width=100, height=24)
            button = ctk.CTkButton(self.data_frame, text='Modify', font=('Arial', 20), fg_color='blue', command=lambda: self.modify_data(product_id.get(), name.get(), price.get(), description.get(), category.get(), available.get()), height=50, width=180)

            product_id_label.pack(pady=(20, 10))
            product_id_entry.pack(padx=80)
            product_name_label.pack(pady=10)
            product_name_entry.pack( padx=80)
            product_price_label.pack(pady=10)
            product_price_entry.pack( padx=80)
            product_category_label.pack(pady=10)
            product_category_entry.pack( padx=80)
            product_available_label.pack(pady=10)
            product_available_entry.pack(padx=(70, 0))
            product_desc_label.pack(pady=10)
            product_desc_entry.pack( padx=80)
            product_desc_button.pack(pady=(5, 5))
            button.pack(pady=20)

        elif option == 'Delete' and self.current_window != 'Delete':

            for widget in self.data_frame.winfo_children():
                widget.destroy()

            if self.current_window == 'Log':
                self.table('product_id')

            self.current_window = 'Delete'
            product_id_label = ctk.CTkLabel(self.data_frame, text='ID', font=('Arial', 20))
            product_id_entry = ctk.CTkEntry(self.data_frame, textvariable=product_id, font=('Arial', 24), height=40, width=width*3)

            button = ctk.CTkButton(self.data_frame, text='Delete', font=('Arial', 20), fg_color='red', command=lambda: self.delete_data(product_id.get()), height=50, width=180)

            product_id_label.pack(pady=(20, 10))
            product_id_entry.pack(padx=84)
            button.pack(pady=20)

        elif option == 'Create' and self.current_window != 'Create':

            for widget in self.data_frame.winfo_children():
                widget.destroy()

            if self.current_window == 'Log':
                self.table('product_id')

            self.current_window = 'Create'
            #Form/data
            product_name_label = ctk.CTkLabel(self.data_frame, text='Product name', font=('Arial', 20))
            product_price_label = ctk.CTkLabel(self.data_frame, text='Price', font=('Arial', 20))
            product_desc_label = ctk.CTkLabel(self.data_frame, text='Description', font=('Arial', 20))
            product_category_label = ctk.CTkLabel(self.data_frame, text='Category', font=('Arial', 20))
            product_available_label = ctk.CTkLabel(self.data_frame, text='Available', font=('Arial', 20))

            product_name_entry = ctk.CTkEntry(self.data_frame, textvariable=name, font=('Arial', 20), height=40, width=width*3)
            product_price_entry = ctk.CTkEntry(self.data_frame, textvariable=price, font=('Arial', 20), height=40, width=width*3)
            product_desc_entry = ctk.CTkTextbox(self.data_frame, font=('Arial', 20), border_color='gray50', border_width=2, height=150)
            product_category_entry = ctk.CTkOptionMenu(self.data_frame, values=['Para acompañar', 'Pastelería', 'Sándwich Salados', 'Sin tacc', 'Café', 'Café gourmet', 'Té y otros', 'Promos cafetería'], variable=category,height=40, width=width*3 , font=('Arial', 18), fg_color='#434447', button_color='#353638', button_hover_color='#252627')
            product_available_entry = ctk.CTkCheckBox(self.data_frame, variable=available, text='')

            product_desc_button = ctk.CTkButton(self.data_frame, text='save',  command=lambda: description.set(product_desc_entry.get(1.0, "end-1c") ), width=100, height=24)
            send_button = ctk.CTkButton(self.data_frame, text='Add product', font=('Arial', 20), fg_color='green', command=lambda: self.add_data(name.get(), price.get(), description.get(), category.get(), available.get()), height=50, width=180)

            product_name_label.pack(pady=(20, 10))
            product_name_entry.pack( padx=80)
            product_price_label.pack(pady=10)
            product_price_entry.pack( padx=80)
            product_category_label.pack(pady=10)
            product_category_entry.pack( padx=80)
            product_available_label.pack(pady=10)
            product_available_entry.pack(padx=(70, 0))
            product_desc_label.pack(pady=10)
            product_desc_entry.pack( padx=80)
            product_desc_button.pack(pady=(5, 5))
            send_button.pack(pady=20)
        
        elif option == 'Log' and self.current_window != 'Log':
            
            #This can be placed in the table function but it is visually better when all the widgets changes at the same time
            for widget in self.table_frame.winfo_children():
                    widget.destroy()

            for widget in self.data_frame.winfo_children():
                widget.destroy()

            self.current_window = 'Log'
            self.table('log')
            
    def table(self, *args):
        #Use update to get the correct size of self.table_frame after adding all the widgets
        self.update()
        
        if 'log' in args:
            
            columns = ['User_id', 'Name', 'Action', 'Date']
            table_width = int(self.table_frame.winfo_width() / len(columns))

            custom_style = ttk.Style(self)
            custom_style.theme_use('default')
            custom_style.configure('Treeview', fieldbackground = '#383838', background= '#383838', foreground= 'white', bordercolor='#434447')
            custom_style.configure('Treeview.Heading', fieldbackground = '#434447', background= '#434447', foreground= 'white', bordercolor='#434447', font=('Arial', 12, "bold"))

            table = ttk.Treeview(self.table_frame, show='headings')
            table['columns'] = columns

            table.column('User_id', stretch=False, width=int(table_width * 0.5), anchor='center')
            table.heading('User_id', text= 'User_id')
            table.column('Name', stretch=True, width=table_width, anchor='center')
            table.heading('Name', text='Name')
            table.column('Action', stretch=True, width=table_width, anchor='center')
            table.heading('Action', text='Action')
            table.column('Date', stretch=True, width=table_width, anchor='center')
            table.heading('Date', text='Date')

            #Load products
            query_accepted, data = Log.get_logs()
            if query_accepted:
                for index, product in enumerate(data):
                    if index % 2 == 0:
                        table.insert('', 'end', values=product, tags=["even"])
                    else:
                        table.insert('', 'end', values=product, tags=["odd"])

                    table.tag_configure('even', background='#3d3d3d')
                    table.tag_configure('odd', background='#5d5d5d')

            else:
                CTkMessagebox(self, message=data)
            
            table.bind('<<TreeviewSelect>>', lambda event: self.show_description(event, data, table))

            table.pack(expand=True, fill='both')
        else:
            order = args[0]
            
            for widget in self.table_frame.winfo_children():
                    widget.destroy()

            columns = ['ID', 'Name', 'Price', 'Category', 'Available']
            table_width = int(self.table_frame.winfo_width() / len(columns))

            custom_style = ttk.Style(self)
            custom_style.theme_use('default')
            custom_style.configure('Treeview', fieldbackground = '#383838', background= '#383838', foreground= 'white', bordercolor='#434447')
            custom_style.configure('Treeview.Heading', fieldbackground = '#434447', background= '#434447', foreground= 'white', bordercolor='#434447', font=('Arial', 14, "bold"))

            table = ttk.Treeview(self.table_frame, show='headings')
            table['columns'] = columns

            table.column('ID', stretch=False, width=int(table_width * 0.5), anchor='center')
            table.heading('ID', text= 'ID', command=lambda: self.table('product_id'))
            table.column('Name', stretch=True, width=table_width, anchor='center')
            table.heading('Name', text='Name', command=lambda: self.table('product_name'))
            table.column('Price', stretch=True, width=table_width, anchor='center')
            table.heading('Price', text='Price', command=lambda: self.table('price'))
            table.column('Category', stretch=True, width=table_width, anchor='center')
            table.heading('Category', text='Category', command=lambda: self.table('category'))
            table.column('Available', stretch=True, width=table_width, anchor='center')
            table.heading('Available', text='Available', command=lambda: self.table('available'))

            #Load products
            query_accepted, data = Products.get_products(order)
            if query_accepted:
                for index, product in enumerate(data):
                    if index % 2 == 0:
                        table.insert('', 'end', values=product, tags=["even"])
                    else:
                        table.insert('', 'end', values=product, tags=["odd"])

                    table.tag_configure('even', background='#3d3d3d')
                    table.tag_configure('odd', background='#5d5d5d')

            else:
                CTkMessagebox(self, message=data)
            
            table.bind('<<TreeviewSelect>>', lambda event: self.show_description(event, data, table))

            table.pack(expand=True, fill='both')

    ########## Functionalities ##########

    def add_data(self,name: str, price: float, description: str, category: str, available: bool,  *args):
        if not isinstance(name, str) or name.isspace() or name == "":
            CTkMessagebox(self, message='Name must be a non empty string.')
        elif name.isdigit():
            CTkMessagebox(self, message='The product name cant be a digit.')
        elif not isinstance(price, (int, float)) or price < 0:
            CTkMessagebox(self, message='Price must be a positive real number.')
        elif not isinstance(category, str) or category.isspace() or category == "":
            CTkMessagebox(self, message='Category cant be empty.')
        elif not isinstance(description, str) or description.isspace() or description.isdigit() or description == "":
            CTkMessagebox(self, message='Description must be a non empty string.')
        else:
            query_accepted, msg = Products.add_product(name, price, description, category, available)
            if query_accepted:
                CTkMessagebox(self, message=msg)
                product_id = Products.get_last_id()[0][0]
                log = f'Added a new product: {name}, ID: {product_id}'
                self.add_log(self.session[0].get_id(), log, datetime.now().replace(second=0, microsecond=0))
                self.table('product_id')
            else:
                CTkMessagebox(self, message=msg)

    def delete_data(self, id: int):
        name = Products.get_product_name(id)[0]
        query_accepted, msg = Products.delete_product(id)
        if query_accepted:
            CTkMessagebox(self, message=msg)
            log = f'Deleted a product: {name}, ID: {id}'
            self.add_log(self.session[0].get_id(), log, datetime.now().replace(second=0, microsecond=0))
            self.table('product_id')
        else:
            CTkMessagebox(self, message=msg)

    def modify_data(self, id: int, name: str, price: float, description: str, category: str, available: bool):
        print(name.isdigit())
        if not isinstance(id, int ) or id < 0:
            CTkMessagebox(self, message='ID must be a positive integer.')
        elif not isinstance(name, str) or name.isspace() or name == "":
            CTkMessagebox(self, message='Name must be a non empty string.')
        elif name.isdigit():
            CTkMessagebox(self, message='The product name cant be a digit.')
        elif not isinstance(price, (int, float)) or price < 0:
            CTkMessagebox(self, message='Price must be a positive real number.')
        elif not isinstance(category, str) or category.isspace() or category == "":
            CTkMessagebox(self, message='Category cant be empty.')
        elif not isinstance(description, str) or description.isspace() or description.isdigit() or description == "":
            CTkMessagebox(self, message='Description must be a non empty string.')
        else:
            query_accepted, msg = Products.modify_products(id, name, price, description, category, available)

            if query_accepted:
                self.table('product_id')
                CTkMessagebox(self, message=msg)
            else:
                CTkMessagebox(self, message=msg)

    def show_description(self, event, data, table):
        item = table.selection()[0]
        product_id = table.item(item)['values'][0]
        query_accepted, data = Products.get_description(product_id)

        if query_accepted:
            CTkMessagebox(self, message=data[0][0], title='Description', option_1='Close', icon='')
        else:
            CTkMessagebox(self, message=data, title='Error')

    def add_log(self, user_id: int, log: str, date: datetime):
        Log.add_log(user_id, log, date)

    def send_email(self, *args):
        email = {'email' : args[0]}
        r = requests.post(os.getenv('VERIFICATION_ROUTE'), json=email)
        if r.status_code == 200:
            CTkMessagebox(self, message='Email sent')
        else:
            CTkMessagebox(self, message='An error ocurred.')

    def login_verificacion(self,*args, **kwargs):
        state, msg =  Users.sign_in(kwargs['email'], kwargs['password'])
        if state:
            query_accepted, data = Users.get_session_data(kwargs['email'])
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
        state, msg = Users.register(kwargs['name'], kwargs['email'], kwargs['password'])
        if state:
            CTkMessagebox(self, message=msg)
        else:
            CTkMessagebox(self, message=msg)


if __name__ == "__main__":
    app = MainScreen()
    app.mainloop()