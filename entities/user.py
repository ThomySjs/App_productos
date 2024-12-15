class user:
    def __init__(self, id: int, name: str, email: str):
        self.__id = id
        self.__name = name
        self.__email = email

    def get_id(self) -> int:
        return self.__id
    
    def get_name(self) -> str:
        return self.__name
    
    def get_email(self) -> str:
        return self.__email
    
    def set_name(self, name: str):
        if not isinstance(name, str) or name.isdigit() or name.isspace() or name == "":
            msg = 'Invalid name'
            return False, msg
        self.__name = name
        msg = 'Name changed'
        return True, msg
    
    def set_email(self, email:str):
        if not isinstance(email, str) or email.isspace() or email == "" or email.count('@') != 1:
            msg = 'Invalid email syntax.'
            return False, msg
        front, dom =  email.split('@')
        dom = f'@{dom}'
        if len(front) < 5 and '.' not in dom or dom.index('.') in (len(dom), 1):
            msg = 'Invalid email syntax'
            return False, msg
        
        self.__email= email
        msg = 'Email changed'
        return True, msg
    
    def __str__(self):
        return f'ID: {self.__id}, name: {self.__name}, email: {self.__email}'
