from typing import TypedDict, Dict

class SQLValue(TypedDict):
    id_user: int
    username: str
    password: str
    role: str

class User : 
    def __init__(self, dico: Dict[str, SQLValue]) -> None :
        self.id_user = dico['id_user']
        self.username = dico['username']
        self.password = dico['password']
        self.role = dico['role']