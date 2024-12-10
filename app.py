import customtkinter as ctk
from tkinter import ttk 


class MS(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.Resolution(700, 600)

        #Main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(expand=True, fill='both')

        self.Loguin()

    def Resolution(self, *args, **kwargs):
        #This captures the w and h of the users screen 
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        # w and h of the window (app)
        self.width = args[0]
        self.height = args[1]

        #get the center of the screen and place the app there
        self.x = (self.screen_width / 2) - (self.width / 2)
        self.y = (self.screen_height / 2) - (self.height / 2)

        self.geometry('%dx%d+%d+%d' % (self.width, self.height, self.x, self.y))
        self.title('Prueba')
        self.resizable(0, 0)

    def Loguin(self):

        mail = ctk.StringVar()
        password = ctk.StringVar()
        
        label_mail = ctk.CTkLabel(self.main_frame, text='Mail', font=('Arial', 24), text_color='white')
        label_password = ctk.CTkLabel(self.main_frame, text='Password', font=('Arial', 24), text_color='white')


        entry_mail = ctk.CTkEntry(self.main_frame, placeholder_text='example@gmail.com', textvariable=mail, width=250, height=45, font=('Arial', 18))
        entry_password = ctk.CTkEntry(self.main_frame, textvariable=password, show='*', width=250, height=45, font=('Arial', 18))

        Login_button = ctk.CTkButton(self.main_frame, text='Login', fg_color='green', width=250, height=40,  command=lambda: print(mail.get()))
        
        
        
        label_mail.pack(pady = (150,5))
        entry_mail.pack(pady= 5)
        label_password.pack(pady = 5)
        entry_password.pack(pady=5)
        Login_button.pack(pady=10)

    


if __name__ == "__main__":
    app = MS()
    app.mainloop()