from tkinter import *
from tkinter import ttk
import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("escola.db")
        self.cursor = self.conn.cursor()
        self.createUserTable()

    def createUserTable(self):
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS users(
                            id INTEGER PRIMARY KEY, 
                            nome TEXT, 
                            email TEXT, 
                            rgm INTEGER, 
                            senha TEXT,
                            nota_a2 TEXT DEFAULT '0.0',
                            nota_a1 REAL DEFAULT 0.0,
                            nota_atividades REAL DEFAULT 0.0,
                            nota_final REAL DEFAULT 0.0
                            );

        ''')
        self.conn.commit()

    def insert(self, name, email, rgm, password):
        try:
            self.cursor.execute(''' INSERT INTO users (nome, email, rgm, senha)
                              VALUES (?, ?, ?, ?); ''', (name, email, rgm, password))
            self.conn.commit()
        except:
            print("ERRO DB!")


    def getUsers(self):
        return self.conn.execute("SELECT * FROM users")

    def closeConnection(self):
        self.cursor.close()

class Application:
    def __init__(self, master):
        self.root = master
        self.db = Database()

        self.windowConfig()
        # self.registerWidgets()
        self.mainPage()

    def windowConfig(self):
        self.root.geometry("500x500")

    def mainPage(self):
        studentRegister = Button(self.root, text="Registrar um aluno", command=self.registerWidgets)
        studentRegister.pack()

        showStudents = Button(self.root, text="Mostrar todos alunos", command=self.showUsers)
        showStudents.pack()

        editStudents = Button(self.root, text="Editar nota do aluno")
        editStudents.pack()

    def topRoot(self):
        self.root2 = Toplevel()
        # self.root2.destroy()
        # self.root2.geometry("800x500")

    def registerWidgets(self):
        self.topRoot()

        nameLabel = Label(self.root2, text="Nome do aluno: ")
        nameLabel.pack()
        self.name = Entry(self.root2)
        self.name.pack()

        emailLabel = Label(self.root2, text="Email: ")
        emailLabel.pack()
        self.email = Entry(self.root2)
        self.email.pack()

        rgmLabel = Label(self.root2, text="RGM: ")
        rgmLabel.pack()
        self.rgm = Entry(self.root2)
        self.rgm.pack()

        passwordLabel = Label(self.root2, text="Senha: ")
        passwordLabel.pack()
        self.password = Entry(self.root2)
        self.password.pack()

        confirmLabel = Label(self.root2, text="Confirme a senha: ")
        confirmLabel.pack()
        self.confirm = Entry(self.root2)
        self.confirm.pack()

        submit = Button(self.root2, text="Enviar", command=self.saveUser)
        submit.pack()

    def saveUser(self):
        print(self.name.get(), self.email.get(), self.rgm.get(), self.password.get())
        self.db.insert(self.name.get(), self.email.get(), self.rgm.get(), self.password.get())

    def showUsers(self):
        self.topRoot()

        table = ttk.Treeview(self.root2, columns=("ID", "Nome", "Email", "RGM", "A2", "A1", "Atividades", "Nota final"))
        table.heading("#0", text="ID",)
        table.heading("#1", text="Nome")
        table.heading("#2", text="Email")
        table.heading("#3", text="RGM")
        table.heading("#4", text="A2")
        table.heading("#5", text="A1")
        table.heading("#6", text="Atividades")
        table.heading("#7", text="Nota final")

        users = self.db.getUsers()

        for user in users:
            print(user)
            table.insert("", "end", text=user[0], values=(user[1], user[2], user[3], user[5], user[6], user[7], user[8]))

        table.pack(expand=True, fill="both")



def app():
    root = Tk()
    Application(root)
    root.mainloop()


if __name__ == "__main__":
    app()
