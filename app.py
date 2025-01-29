import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
from PIL import Image, ImageTk
from datetime import datetime
import requests
import json
import sys

import os
from dotenv import load_dotenv


class MainScreen(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__()

        #path
        if getattr(sys, "frozen", False):
            #MEIPASS is the temp folder pyinstaller creates for storing
            self.path = sys._MEIPASS
        else:
            self.path = os.path.dirname(os.path.abspath(__file__))

        #Window config
        ctk.set_appearance_mode('dark')
        self.title('Menu manager')
        self.resizable(0, 0)
        self.Resolution(width = 1280, height =  720)

        #Variables
        self.widget_width = int(self.winfo_width() * 0.05)
        self.current_window = None
        self.__token = None
        self.__refresh_token = None
        self.__header = ""
        self.sent = False
        self.last_mail_sent = 0
        self.__remember_session = None

        
        env_path = os.path.join(self.path, ".env")
        load_dotenv(dotenv_path=env_path)

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
        self.widget_width = int(self.winfo_width() * 0.05)
        self.remember_tool_read()
        self.login_widgets()
        self.image_widget()

    ########## Widgets ##########

    def image_widget(self, *args, **kwargs):
        """
        Renders the login image.
        """

        #This deletes every widget(in this case image) everytime this function is called
        #keeping just 1 image at the time 
        for widget in self.image_frame.winfo_children():
            widget.destroy()


        width = self.image_frame.winfo_width()
        height = self.image_frame.winfo_height()
        
        #loading the image
        image = Image.open(os.path.join(self.path, "static/Fondo.jpg")).resize((width,height))
        image_tk = ImageTk.PhotoImage(image)
        
        #Canvas to place the image in it
        canvas_image = tk.Canvas(self.image_frame, bd=0, highlightthickness=0, relief='ridge')
        canvas_image.grid(row=0, column=0, sticky='nwse')
        canvas_image.create_image(0,0, image=image_tk, anchor='nw')

        #This prevents the image to be garbage collected
        canvas_image.image = image_tk

    def login_widgets(self, *args):
        """
        Renders the login widgets.
        """
        #Delete previous self.form_frame widgets that are not CTkComboBox
        for widget in self.form_frame.winfo_children():
            if not isinstance(widget, ctk.CTkComboBox):
                widget.destroy()

        width = int(self.form_frame.winfo_width() / 1.3)

        #Variables
        email = ctk.StringVar(value=self.__remember_session)
        password = ctk.StringVar()
        
        #Widgets
        label_mail = ctk.CTkLabel(self.form_frame, text='Email', font=('Arial', 24), text_color='white')
        label_password = ctk.CTkLabel(self.form_frame, text='Password', font=('Arial', 24), text_color='white')

        entry_mail = ctk.CTkEntry(self.form_frame, textvariable=email, width=width, height=45, font=('Arial', 18))
        entry_password = ctk.CTkEntry(self.form_frame, textvariable=password, show='*', width=width, height=45, font=('Arial', 18))

        remember_entry = ctk.CTkCheckBox(self.form_frame, text="Remember me")

        login_button = ctk.CTkButton(self.form_frame, text='Login', fg_color='green', width=width, height=40,  command=lambda: self.login_verificacion(mail=email.get(), password=password.get(), remember=remember_entry.get()))

        register_button = ctk.CTkButton(self.form_frame, text='Register', width=width, height=40, command=self.register_widgets)
        
        if self.__remember_session:
            remember_entry.select()

        #Layout
        label_mail.pack(pady = (150,5))
        entry_mail.pack(pady= 5)
        label_password.pack(pady = 5)
        entry_password.pack(pady=5)
        remember_entry.pack()
        login_button.pack(pady=10)
        register_button.pack(pady=40)

    def register_widgets(self, *args):
        """
        Renders the register widgets.
        """
        #Delete previous self.form_frame widgets that are not CTkComboBox
        for widget in self.form_frame.winfo_children():
            if not isinstance(widget, ctk.CTkComboBox):
                widget.destroy()

        width = int(self.form_frame.winfo_width() / 1.3)

        #Variables
        name = ctk.StringVar()
        email = ctk.StringVar()
        password = ctk.StringVar()
        key = ctk.StringVar()

        #Widgets
        label_name = ctk.CTkLabel(self.form_frame, text='Name', font=('Arial', 24), text_color='white')
        label_mail = ctk.CTkLabel(self.form_frame, text='Email', font=('Arial', 24), text_color='white')
        label_password = ctk.CTkLabel(self.form_frame, text='Password', font=('Arial', 24), text_color='white')
        label_key =  ctk.CTkLabel(self.form_frame, text='Key', font=('Arial', 24), text_color='white')

        entry_name = ctk.CTkEntry(self.form_frame, textvariable=name, width=width, height=45, font=('Arial', 18) )
        entry_mail = ctk.CTkEntry(self.form_frame, placeholder_text='example@gmail.com', textvariable=email, width=width, height=45, font=('Arial', 18))
        entry_password = ctk.CTkEntry(self.form_frame, textvariable=password, show='*', width=width, height=45, font=('Arial', 18))
        entry_key = ctk.CTkEntry(self.form_frame, textvariable=key, show='*', width=width, height=45, font=('Arial', 18))

        register_button = ctk.CTkButton(self.form_frame, text='Register', fg_color='green', width=width, height=40,  command=lambda: self.register_verification(name = name.get(), mail=email.get(), password=password.get(), key=key.get()))

        login_button = ctk.CTkButton(self.form_frame, text='Sign In', width=width, height=40, command=self.login_widgets)
        
        #Layout
        label_name.pack(pady = (80,5))
        entry_name.pack(pady = 5)
        label_mail.pack(pady = 5)
        entry_mail.pack(pady= 5)
        label_password.pack(pady = 5)
        entry_password.pack(pady=5)
        label_key.pack(pady= 5)
        entry_key.pack(pady= 5)
        register_button.pack(pady=10)
        login_button.pack(pady=40)

    def control_panel(self, *args, **kwargs):
        """
        This is the main function of the post login application. 
        
        ### Calls:
        - Navbar (Shows the navbar)
        - Table (Shows the table)
        - Form (Gets the user input)

        ### Notes:
        - Data form has 4 possible arguments. Create, Modify, Delete and Log. This means the operation you want to show on screen.  
        """
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
        self.data_form('Create')    
        self.table()

    def navbar(self, *args):
        """
        Renders the navbar widgets.
        """
        width = int(self.winfo_width() * 0.025)

        for widget in self.navbar_frame.winfo_children():
                widget.destroy()
        
        create_image = ctk.CTkImage(dark_image=Image.open(os.path.join(self.path, "static/Create.png")))
        delete_image = ctk.CTkImage(dark_image=Image.open(os.path.join(self.path, "static/Delete.png")))
        modify_image = ctk.CTkImage(dark_image=Image.open(os.path.join(self.path, "static/Modify.png")))
        log_image = ctk.CTkImage(dark_image=Image.open(os.path.join(self.path, "static/Log.png")))
        
        create_button = ctk.CTkButton(self.navbar_frame, image=create_image, bg_color="#121212", fg_color="#121212", width=width, text="", command=lambda: self.data_form("Create"))
        modify_button = ctk.CTkButton(self.navbar_frame, image=modify_image, bg_color="#121212", fg_color="#121212", width=width, text="", command=lambda: self.data_form("Modify"))
        delete_button = ctk.CTkButton(self.navbar_frame, image=delete_image, bg_color="#121212", fg_color="#121212", width=width, text="", command=lambda: self.data_form("Delete"))
        log_button = ctk.CTkButton(self.navbar_frame, image=log_image, bg_color="#121212", fg_color="#121212", width=width, text="", command=lambda: self.data_form("Log"))

        create_button.pack(pady=(20, 10), padx=10)
        modify_button.pack(pady=10, padx=10)
        delete_button.pack(pady=10, padx=10)
        log_button.pack(pady=10, padx=10)

    def data_form(self, operation, *args):
        """
        Contains the logic of the data forms.

        ### Arguments:
        - `operation` Create, Modify, Delete, Log
        """
        #Self.current_window prevents the user from overloading the app by pressing the same button multiple times
        if operation == "Modify" and self.current_window != "Modify":
            if self.current_window == "Log":
                self.current_window = "Modify"
                self.table("product_id")
            self.modify_widgets()

        elif operation == "Delete" and self.current_window != "Delete":
            if self.current_window == 'Log':
                self.current_window = "Delete"
                self.table('product_id')
            self.delete_widgets()

        elif operation == "Create" and self.current_window != "Create":
            if self.current_window == 'Log':
                self.current_window = "Create"
                self.table('product_id')
            self.add_widgets()
        
        elif operation == "Log" and self.current_window != "Log":
            self.log_widgets()
            self.table(Log="Log", new_id = -1)
            
    def table(self, order = "product_id", *args, **kwargs):
        """
        Contains the table call logic.

        ### Arguments:
        - `args` (order, Log)
        - `kwargs` (new_id)
        
        ### ex:
        
            self.table("price") -> table is ordered by products price
            
            self.table("Log", new_id=-1) -> log table 

        ### Notes:
        - new_id indicates the users id, if -1 then shows the complete table.
        """
        #Use update to get the correct size of self.table_frame after adding all the widgets
        self.update()

        if kwargs and kwargs["new_id"] != -1:
            for widget in self.table_frame.winfo_children():
                    widget.destroy()
        
        if "Log" in kwargs:
            self.log_table(kwargs["new_id"])
        else:
            self.product_table(order)
            
    ########## Tables ##########

    def log_table(self, new_id: int):
        """
        Renders the log table.

        ### Arguments:
        - `new_id` users ID to filter the table, -1 shows the complete table.


        ### Request:
        - Method: GET
        - Content-type: JSON
        - Response type: JSON

        ### Notes:
        - Request uses a JWT token  (header)
        """
        for widget in self.table_frame.winfo_children():
                    widget.destroy()

        columns = ['log_id', 'user_id', 'log', 'date']
        table_width = int(self.table_frame.winfo_width() / len(columns))

        custom_style = ttk.Style(self)
        custom_style.theme_use('default')
        custom_style.configure('Treeview', fieldbackground = '#383838', background= '#383838', foreground= 'white', bordercolor='#434447')
        custom_style.configure('Treeview.Heading', fieldbackground = '#434447', background= '#434447', foreground= 'white', bordercolor='#434447', font=('Arial', 12, "bold"))

        table = ttk.Treeview(self.table_frame, show='headings')
        table['columns'] = columns

        table.column('log_id', stretch=False, width=int(table_width * 0.5), anchor='center')
        table.heading('log_id', text= 'Log ID')
        table.column('user_id', stretch=True, width=table_width, anchor='center')
        table.heading('user_id', text='User ID')
        table.column('log', stretch=True, width=table_width, anchor='center')
        table.heading('log', text='Action')
        table.column('date', stretch=True, width=table_width, anchor='center')
        table.heading('date', text='Date')

        route = os.getenv("URL") + "/products/changelog"
        try:
            data = requests.get(route, headers=self.__header)
            if data.status_code == 200:
                data = data.json()
                for index, log in enumerate(data):
                    if new_id != -1: 
                        if log["user_id"] == new_id:
                            temp_list = [log[key] for key in columns]
                        else:
                            temp_list = []
                    else:
                        temp_list = [log[key] for key in columns]
                    if len(temp_list) == 0:
                        pass
                    else:
                        if index % 2 == 0:
                            table.insert('', 'end', values=temp_list, tags=["even"])
                        else:
                            table.insert('', 'end', values=temp_list, tags=["odd"])

                    table.tag_configure('even', background='#3d3d3d')
                    table.tag_configure('odd', background='#5d5d5d')
            elif data.status_code == 401:
                if self.refresh_token() is None:
                    return
                else:
                    self.log_table(new_id)
            else:
                data = data.json()
                CTkMessagebox(self, message=data["error"])
        except requests.ConnectionError:
            CTkMessagebox(self, message="Conection error, try again.")
        except Exception as e:
            print(str(e))
            CTkMessagebox(self, message="An error ocurred.")

        table.pack(expand=True, fill='both')

    def product_table(self, order,  *args) -> None:
        """
        Renders the product table.
        
        ### Arguments:
        - `order` 

        ### Request:
        - Method: Post
        - Key: Order
        - Content-type: JSON
        - Response-type: JSON
        
        ### Notes:
        - Request uses a JWT token  (header)
        """
        for widget in self.table_frame.winfo_children():
                    widget.destroy()

        columns = ["product_id", "product_name", "price", "category", "available"]
        table_width = int(self.table_frame.winfo_width() / len(columns))

        custom_style = ttk.Style(self)
        custom_style.theme_use('default')
        custom_style.configure('Treeview', fieldbackground = '#383838', background= '#383838', foreground= 'white', bordercolor='#434447')
        custom_style.configure('Treeview.Heading', fieldbackground = '#434447', background= '#434447', foreground= 'white', bordercolor='#434447', font=('Arial', 14, "bold"))

        table = ttk.Treeview(self.table_frame, show='headings')
        table['columns'] = columns

        table.column("product_id", stretch=False, width=int(table_width * 0.5), anchor='center')
        table.heading("product_id", text= 'ID', command=lambda: self.table('product_id'))
        table.column("product_name", stretch=True, width=table_width, anchor='center')
        table.heading("product_name", text='Name', command=lambda: self.table('product_name'))
        table.column("price", stretch=True, width=table_width, anchor='center')
        table.heading("price", text='Price', command=lambda: self.table('price'))
        table.column("category", stretch=True, width=table_width, anchor='center')
        table.heading("category", text='Category', command=lambda: self.table('category'))
        table.column("available", stretch=True, width=table_width, anchor='center')
        table.heading("available", text='Available', command=lambda: self.table('available'))

        #Load products
        route = os.getenv("URL") + "products"
        required_key = {"order": order}
        data = requests.post(route, json=required_key, headers=self.__header)
        if data.status_code == 200:
            data = data.json()
            for index, product in enumerate(data["products"]):
                temp_list = []
                for key in columns:
                    temp_list.append(product[key])
                if index % 2 == 0:
                    table.insert('', 'end', values=temp_list, tags=["even"])
                else:
                    table.insert('', 'end', values=temp_list, tags=["odd"])

                table.tag_configure('even', background='#3d3d3d')
                table.tag_configure('odd', background='#5d5d5d')
        elif data.status_code == 401:
            self.refresh_token()
            current_window = self.current_window
            self.current_window = ""
            self.table()
            self.data_form(current_window)
        else:
            data = data.json()
            CTkMessagebox(self, message=data["error"])
        
        table.bind('<<TreeviewSelect>>', lambda event: self.show_description(table))

        table.pack(expand=True, fill='both')

    ########## Form widgets ##########

    def delete_widgets(self):
        """
        Contains DELETE widgets.

        ### Parent frame
        - self.data_frame
        """
        for widget in self.data_frame.winfo_children():
                widget.destroy()
        
        product_id = ctk.IntVar(value='')

        self.current_window = 'Delete'
        product_id_label = ctk.CTkLabel(self.data_frame, text='ID', font=('Arial', 20))
        product_id_entry = ctk.CTkEntry(self.data_frame, textvariable=product_id, font=('Arial', 24), height=40, width=self.widget_width*3)

        button = ctk.CTkButton(self.data_frame, text='Delete', font=('Arial', 20), fg_color='red', command=lambda: self.delete_data(product_id.get()), height=50, width=180)

        product_id_label.pack(pady=(20, 10))
        product_id_entry.pack(padx=84)
        button.pack(pady=20)

    def add_widgets(self):
        """
        Contains CREATE widgets (add product)

        ### Parent frame
        - self.data_frame
        """

        for widget in self.data_frame.winfo_children():
                widget.destroy()

        self.current_window = 'Create'
        #Variables
        name = ctk.StringVar()
        price = ctk.DoubleVar(value=0)
        description = ctk.StringVar()
        category = ctk.StringVar()
        available = ctk.BooleanVar()

        #Form/data
        product_name_label = ctk.CTkLabel(self.data_frame, text='Product name', font=('Arial', 20))
        product_price_label = ctk.CTkLabel(self.data_frame, text='Price', font=('Arial', 20))
        product_desc_label = ctk.CTkLabel(self.data_frame, text='Description', font=('Arial', 20))
        product_category_label = ctk.CTkLabel(self.data_frame, text='Category', font=('Arial', 20))
        product_available_label = ctk.CTkLabel(self.data_frame, text='Available', font=('Arial', 20))

        product_name_entry = ctk.CTkEntry(self.data_frame, textvariable=name, font=('Arial', 20), height=40, width=self.widget_width*3)
        product_price_entry = ctk.CTkEntry(self.data_frame, textvariable=price, font=('Arial', 20), height=40, width=self.widget_width*3)
        product_desc_entry = ctk.CTkTextbox(self.data_frame, font=('Arial', 20), border_color='gray50', border_width=2, height=150)
        product_category_entry = ctk.CTkOptionMenu(self.data_frame, values=['Para acompañar', 'Pastelería', 'Sándwich Salados', 'Sin tacc', 'Café', 'Café gourmet', 'Té y otros', 'Promos cafetería'], variable=category,height=40, width=self.widget_width*3 , font=('Arial', 18), fg_color='#434447', button_color='#353638', button_hover_color='#252627')
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
        product_desc_button.pack(pady=5)
        send_button.pack(pady=20)

    def modify_widgets(self):
        """
        Contains MODIFY widgets.

        ### Parent frame:
        - self.data_frame
        """
        for widget in self.data_frame.winfo_children():
                widget.destroy()
        
        # This changes the table content only when the previous section of the app was Log
        if self.current_window == 'Log':
            self.table('product_id')

        self.current_window = 'Modify'
        #Variables
        product_id = ctk.IntVar(value='')
        name = ctk.StringVar()
        price = ctk.DoubleVar(value=0)
        description = ctk.StringVar()
        category = ctk.StringVar()
        available = ctk.BooleanVar()
        
        #Form/data
        product_id_label = ctk.CTkLabel(self.data_frame, text='ID', font=('Arial', 20))
        product_name_label = ctk.CTkLabel(self.data_frame, text='Product name', font=('Arial', 20))
        product_price_label = ctk.CTkLabel(self.data_frame, text='Price', font=('Arial', 20))
        product_desc_label = ctk.CTkLabel(self.data_frame, text='Description', font=('Arial', 20))
        product_category_label = ctk.CTkLabel(self.data_frame, text='Category', font=('Arial', 20))
        product_available_label = ctk.CTkLabel(self.data_frame, text='Available', font=('Arial', 20))

        product_id_entry = ctk.CTkEntry(self.data_frame, textvariable=product_id, font=('Arial', 24), height=40, width=self.widget_width*3)
        product_name_entry = ctk.CTkEntry(self.data_frame, textvariable=name, font=('Arial', 20), height=40, width=self.widget_width*3)
        product_price_entry = ctk.CTkEntry(self.data_frame, textvariable=price, font=('Arial', 20), height=40, width=self.widget_width*3)
        product_desc_entry = ctk.CTkTextbox(self.data_frame, font=('Arial', 20), border_color='gray50', border_width=2, height=100)
        product_category_entry = ctk.CTkOptionMenu(self.data_frame, values=['Para acompañar', 'Pastelería', 'Sándwich Salados', 'Sin tacc', 'Café', 'Café gourmet', 'Té y otros', 'Promos cafetería'], variable=category, height=40, width=self.widget_width*3 , font=('Arial', 18), fg_color='#434447', button_color='#353638', button_hover_color='#252627')
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

    def log_widgets(self):
        """
        Contains Log widgets (ID entry to filter the table)

        ### Parent frame
        - self.data_frame
        """
        #This can be placed in the table function but it is visually better when all the widgets changes at the same time
        for widget in self.table_frame.winfo_children():
                widget.destroy()

        for widget in self.data_frame.winfo_children():
            widget.destroy()

        user_id = ctk.IntVar()

        self.current_window = "Log"

        #Widgets
        id_label = ctk.CTkLabel(self.data_frame, text="User ID", font=("Arial", 20))

        id_entry = ctk.CTkEntry(self.data_frame, textvariable=user_id, font=("Arial", 20), height=40, width=self.widget_width*3)

        submit_button = ctk.CTkButton(self.data_frame, font=("Arial", 20), height=40, width=self.widget_width*3, text="Apply filter", fg_color="Green", command=lambda: self.table(Log="Log", new_id = user_id.get()))

        id_label.pack(pady=(20,10))
        id_entry.pack(padx=80)
        submit_button.pack(pady=5)

    ########## Functionalities ##########

    def remember_tool_read(self):
        """
        Reads the file that contains the email saved to remember and place it on the email entry (as placeholder).

        - Content-type: JSON
        """
        SESSION_PATH = "config.json"
        try:
            with open(SESSION_PATH, "r") as f:
                self.__remember_session = json.load(f).get("email")
                f.close()

        except IOError:
            self.__remember_session = ""

    def remember_tool_write(self, email: str):
        """
        Saves the email if the remember me checkbox is checked. Creates the file if it doesnt exists.

        - Content-type: JSON
        """
        SESSION_PATH = "config.json"
        with open(SESSION_PATH, "w") as f:
            json.dump({"email" : email}, f)
            f.close()

    def add_data(self,name: str, price: float, description: str, category: str, available: bool,  *args):
        """
        Makes a request to the server to add the product. If fails, returns an error message.

        ### Request:
        - Method: POST
        - Content-type: JSON
        - Response-type: JSON

        ### Payload example:
            {
                "product_name" : "Jorge",
                "price" : 1500.0,
                "description" : "some description",
                "category" : "some category",
                "available" : True
            }

        ### Authorization:
        - Uses jwt token for authorization (header)
        """
        if not isinstance(name, str) or name.isspace() or name == "":
            CTkMessagebox(self, message='Name must be a non empty string.')
        elif name.isdigit():
            CTkMessagebox(self, message='The product name cant be a digit.')
        elif not isinstance(price, (int, float)) or price < 0:
            CTkMessagebox(self, message='Price must be a positive real number.')
        elif not isinstance(category, str) or category.isspace() or category == "":
            CTkMessagebox(self, message='Category cant be empty.')
        elif not isinstance(description, str)  or description.isdigit():
            CTkMessagebox(self, message='Description must be str type.')
        else:
            route = os.getenv("URL") + "products/add"
            json_payload = {
                "product_name" : name,
                "price" : price,
                "description" : description,
                "category" : category,
                "available" : available
            }
            try:
                response = requests.post(route, json=json_payload, headers=self.__header)
                if response.status_code == 401:
                    self.refresh_token()
                    self.add_data(name, price, description, category, available)
                elif response.status_code == 201:
                    self.table()
                else:
                    CTkMessagebox(self, message=response.text["error"])
            except requests.ConnectionError:
                CTkMessagebox(self, message="Conection error, try again.")
            except Exception as e:
                print(str(e))
                CTkMessagebox(self, message="An error ocurred, please try again.")

    def delete_data(self, product_id: int):
        """
        Makes a request to the server to delete the product. If fails, returns an error message.

        ### Request:
        - Method: POST
        - Content-type: JSON

        ### Payload example:

            {"product_id : 1} In this case `product_id` is passed through the function argument.

        ### Authorization:
        - Uses jwt token for authorization (header)
        """
        if not isinstance(product_id, int) or product_id < 0:
            CTkMessagebox(self, message="The id must be a positive integer.")
        else:
            route = os.getenv("URL") + "products/delete"
            json_payload = {
                "product_id" : product_id
            }
            try:
                response = requests.delete(route, json=json_payload, headers=self.__header)
                if response.status_code == 401:
                    self.refresh_token()
                    self.delete_data(product_id)
                elif response.status_code == 200:
                    self.table()
                else:
                    CTkMessagebox(self, message=response.text["error"])
            except requests.ConnectionError:
                CTkMessagebox(self, message="Conection error, try again.")
            except Exception as e:
                CTkMessagebox(self, message=str(e))       

    def modify_data(self, id: int, name: str, price: float, description: str, category: str, available: bool):
        """
        Makes a request to the server to delete the product. If fails, returns an error message.

        ### Request:
        - Method: POST
        - Content-type: JSON

        ### Payload example:
            {   
                "product_id" : 1
                "product_name" : "Cheesecake",
                "price" : 1500.0,
                "description" : "some description",
                "category" : "some category",
                "available" : True
            }

        ### Authorization:
        - Uses jwt token for authorization (header)
        """
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
        elif not isinstance(description, str) or description.isdigit():
            CTkMessagebox(self, message='Description must be str type.')
        else:
            route = os.getenv("URL") + "products/update"
            json_payload = {
                "product_id" : id,
                "product_name" : name,
                "price" : price,
                "description" : description,
                "category" : category,
                "available" : available
            }
            try:
                response = requests.put(route, json=json_payload, headers=self.__header)
                if response.status_code == 401:
                    self.refresh_token()
                    self.modify_data(id, name, price, description, category, available)
                elif response.status_code == 200:
                    self.table()
                else:
                    CTkMessagebox(self, message=response.text["error"])
            except requests.ConnectionError:
                CTkMessagebox(self, message="Conection error, try again.")
            except Exception as e:
                CTkMessagebox(self, message=str(e))

    def show_description(self, table):
        """
        Shows the product description.


        ### Request:
        - Method: GET
        - Key: product ID
        - Response-type: JSON

        ### Request example:
            mainURL/products/1
        """
        item = table.selection()[0]
        product_id = table.item(item)['values'][0]
        route = os.getenv("URL") + "/products/%d" % product_id

        try:
            response = requests.get(route, headers=self.__header)
            if response.status_code == 401:
                self.refresh_token()
                self.show_description(table)
            elif response.status_code == 200:
                data = response.json()
                if data["description"] is None or data["description"].isspace() or data["description"] == "":
                    CTkMessagebox(self, message=" ", title='Description', option_1='Close', icon='')
                else:
                    CTkMessagebox(self, message=data["description"], title='Description', option_1='Close', icon='')
            else:
                CTkMessagebox(self, message=response.text, title='Error')
        except requests.ConnectionError:
            CTkMessagebox(self, message="Conection error, try again.")
        except Exception as e:
            print(f"Error: {str(e)}")
            CTkMessagebox(self, message="An error ocurred")  


    def send_email(self, *args):
        """
        Makes a request to the email endpoint.

        ### Request:
        - Method: POST
        - Content-type: JSON
        - Response-type: JSON

        ### Payload example:

         {"maii" : "yourmail@mail.com"}
        """
        route = os.getenv("URL") + "send-mail"
        json_payload = {
            "mail" : args[0]
        }
        #This part of the code prevents the client from spaming emails.
        if self.sent:
            time_difference = datetime.now() - self.last_mail_sent
            if time_difference.seconds >= 180:
                self.sent = False
            else:
                CTkMessagebox(self, message="Please wait before sending another email. \n Check your junk box.")
        
        if not self.sent:
            try:
                response = requests.post(route, json=json_payload)
                response_dict = response.json()
                if response.status_code == 200:
                    self.last_mail_sent = datetime.now()
                    self.sent = True
                    CTkMessagebox(self, message=response_dict["message"], title="Message")
                else:
                    CTkMessagebox(self, message=response_dict["error"], title="Error")
            except requests.ConnectionError:
                CTkMessagebox(self, message="Connection error.", title="Error")
            except Exception as e:
                CTkMessagebox(self, message=f'An error ocurred. \n Details: {str(e)}', title='Error')

    def login_verificacion(self,*args, **kwargs):
        remember = kwargs["remember"]
        route = os.getenv('URL') + 'login'
        json_payload = {
            "mail" : kwargs["mail"], 
            "password": kwargs["password"]
        }
        try:
            response = requests.post(route, json=json_payload)
            response_dict = response.json()
            if response.status_code == 200:
                self.__token = response_dict["access_token"]
                self.__refresh_token = response_dict["refresh_token"]
                self.__header = {"Authorization" : "Bearer {}".format(self.__token)}
                if remember:
                    self.remember_tool_write(kwargs["mail"])
                else:
                    self.remember_tool_write("")
                self.control_panel()
            elif response.status_code == 401:
                option = CTkMessagebox(self, message=response_dict["error"], option_1="Resend mail", option_2="Close", title="Account not verified")
                if option.get() == "Resend mail":
                    self.send_email(kwargs['mail'])
            else:
                CTkMessagebox(self, message=response_dict["error"])
        except requests.ConnectionError:
            CTkMessagebox(self, message='Connection error.', title='Error')
        except Exception as e:
            CTkMessagebox(self, message=f'An error ocurred. \n Details: {str(e)}', title='Error')

    def register_verification(self, *args, **kwargs):
        route = os.getenv('URL') + 'register'
        json_payload = {
            "name" : kwargs["name"],
            "mail" : kwargs["mail"],
            "password" : kwargs["password"],
            "key" : kwargs["key"]
        }
        try:
            response = requests.post(route, json=json_payload)
            response_dict =  response.json()
            if response.status_code == 201:
                CTkMessagebox(self, message=response_dict["message"])
                self.send_email(kwargs['mail'])
                self.login_widgets()
            else:
                CTkMessagebox(self, message=response_dict["error"])
        except requests.ConnectionError:
            CTkMessagebox(self, message='Connection error. \n Please verify your connection and try again.', title='Error')
        except Exception as e:
            CTkMessagebox(self, message=f"An error ocurred.", title='Error')

    def refresh_token(self) -> str:
        route = os.getenv("URL") + "/refresh"
        new_header = {"Authorization" : "Bearer {}".format(self.__refresh_token)}
        response = requests.post(route, headers=new_header)

        if response.status_code == 401:
            option = CTkMessagebox(self, message="Session expired.", option_1="Log in", option_2="Close", title="Error")
            if option.get() == "Log in":
                self.restart()
                return None
            else: 
                self.destroy()
        else:
            new_tokens = response.json()
            self.__token = new_tokens["access_token"]
            self.__refresh_token = new_tokens["refresh_token"]
            self.__header = {"Authorization" : "Bearer {}".format(self.__token)}

    def restart(self):
        """
        Redirects the user to the login screen.
        """
        self.current_window = None
        self.__token = None
        self.__refresh_token = None
        self.__header = ""
        self.sent = False
        self.last_mail_sent = 0
        self.__remember_session = None
    
        self.Resolution(width = 1280, height =  720)

if __name__ == "__main__":
    app = MainScreen()
    app.mainloop()