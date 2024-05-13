from tkinter import *
from tkinter import ttk
import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("escola.db")
        self.cursor = self.conn.cursor()
        self.createTable()
        
    def createTable(self):
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS users(
                            id INTEGER PRIMARY KEY, 
                            nome TEXT, 
                            email TEXT, 
                            rgm INTEGER, 
                            senha TEXT);
        ''')
        self.conn.commit()

    def insert(self, name, email, rgm, password):
        self.cursor.execute(''' INSERT INTO users (nome, email, rgm, senha)
                          VALUES (?, ?, ?, ?); ''', (name, email, rgm, password))
        self.conn.commit()
                          

    def getUsers(self):
        return self.conn.execute("SELECT * FROM users")
    
    def closeConnection(self):
        self.cursor.close()


class Application:
    def __init__(self, master):
        self.root = master
        self.db = Database()
        self.windowConfig()
        self.widgetsConfig()

    def windowConfig(self):
        self.root.geometry("500x500")

    def widgetsConfig(self):
        self.nameLabel = Label(self.root, text="Nome do aluno: ").pack()
        self.name = Entry(self.root)
        self.name.pack()

        self.emailLabel = Label(self.root, text="Email: ").pack()
        self.email = Entry(self.root)
        self.email.pack()

        self.rgmLabel = Label(self.root, text="RGM: ").pack()
        self.rgm = Entry(self.root)
        self.rgm.pack()

        self.passwordLabel = Label(self.root, text="Senha: ").pack()
        self.password = Entry(self.root)
        self.password.pack()

        self.confirmLabel = Label(self.root, text="Confirme a senha: ").pack()
        self.confirm = Entry(self.root)
        self.confirm.pack()

        self.submit = Button(self.root, text="Enviar", command=self.saveUser).pack()

        self.newWindow = Button(self.root, text="Mostrar usuários", command=self.showUsers).pack()

    def saveUser(self):
        self.db.insert(self.name.get(), self.email.get(), self.rgm.get(), self.password.get())

    def showUsers(self):
        self.rootUsers = Toplevel()
        self.rootUsers

        table = ttk.Treeview(self.rootUsers, columns=("ID", "Nome", "Email", "RGM"))
        table.heading("#0", text="ID",)
        table.heading("#1", text="Nome")
        table.heading("#2", text="Email")
        table.heading("#3", text="RGM")

        users = self.db.getUsers()
        
        for user in users:
            table.insert("", "end", text=user[0], values=(user[1], user[2], user[3]))

        table.pack(expand=True, fill="both")


def app():
    root = Tk()
    Application(root)
    root.mainloop()


if __name__ == "__main__":
    app()
        
