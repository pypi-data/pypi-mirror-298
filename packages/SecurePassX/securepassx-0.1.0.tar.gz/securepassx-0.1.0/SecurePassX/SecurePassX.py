from typing import Any, Dict, NamedTuple
from SecurePassX.database import DatabaseHandler
from pathlib import Path
from typing import Any, Dict, List, NamedTuple
from SecurePassX import DB_READ_ERROR, ID_ERROR
from SecurePassX.security import encrypt

class Secret(NamedTuple):
    secret: Dict[str, Any]
    error: int

class SecPassSecret:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def add(self, title: List[str], username: str, password: str) -> Secret:
        title_text = " ".join(title)
        # if not title_text.endswith("."):
        #     title_text += "."
        secret = {
            "Title": title_text,
            "Username": username,
            "Password": encrypt(password)
        }
        read = self._db_handler.read_secert()
        if read.error == DB_READ_ERROR:
            return Secret(secret, read.error)
        read.secret_list.append(secret)
        write = self._db_handler.write_secert(read.secret_list)
        return Secret(secret, write.error)
    
    def get_secret_list(self) -> List[Dict[str, Any]]:
        read = self._db_handler.read_secert()
        return read.secret_list
    
    def remove(self, todo_id: int) -> Secret:
        """Remove a to-do from the database using its id or index."""
        read = self._db_handler.read_secert()
        if read.error:
            return Secret({}, read.error)
        try:
            secret = read.secret_list.pop(todo_id - 1)
        except IndexError:
            return Secret({}, ID_ERROR)
        write = self._db_handler.write_secert(read.secret_list)
        return Secret(secret, write.error)
    
    def get_secret(self, secret_id:int) -> Secret:
        read = self._db_handler.read_secert()
        if read.error:
            return Secret({}, read.error)
        try:
            secret = read.secret_list[secret_id - 1]
        except IndexError:
            return Secret({}, ID_ERROR)
        return Secret(secret, read.error)