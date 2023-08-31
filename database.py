import sqlite3
from dataclasses import dataclass

class Database:
    def __init__(self, nome):
        self.conn = sqlite3.connect(nome+'.db')
        self.conn.execute("CREATE TABLE IF NOT EXISTS note ( id INTEGER PRIMARY KEY, title TEXT, content TEXT NOT NULL)")

    def add(self, note):
        self.conn.execute(f"INSERT INTO note (title,content) VALUES ('{note.title}', '{note.content}')")
        self.conn.commit()
    
    def get_all(self):
        cursor = self.conn.execute(f"SELECT id, title, content FROM note")
        lista = []
        for linha in cursor:
            id, title, content = linha[0], linha[1], linha[2]
            lista.append(Note(id,title,content))
        
        return lista
    
    def update(self,entry):
        self.conn.execute(f"UPDATE note SET title = '{entry.title}', content = '{entry.content}' WHERE id = {entry.id}")
        self.conn.commit()
    
    def delete(self, note_id):
        self.conn.execute(f"DELETE FROM note WHERE id = {note_id}")
        self.conn.commit()

    def id_correspondente(self, id_nota):
        cursor = self.conn.execute(f"SELECT id, title, content FROM note")
        for linha in cursor:
            id, title, content = linha[0], linha[1], linha[2]
            if id == int(id_nota):
                return(title, content)




@dataclass
class Note:
    id: int = None
    title: str = None
    content: str = ''


