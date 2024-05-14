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
            print("ERRO EM INSERIR!")

    def updateGrade(self, id, a2, a1, atividades, nota_final):
        self.cursor.execute(
            '''UPDATE users SET nota_a2 = ?, nota_a1 = ?, nota_atividades = ?, nota_final = ? WHERE id = ?''',
            (a2, a1, atividades, nota_final, id))
        self.conn.commit()
        print("salvou")

    def getStudentById(self, id=1):
        self.cursor.execute('''SELECT * FROM users WHERE id = ?''', (id))
        return self.cursor.fetchone()


    def getStudents(self):
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
        studentRegister = Button(self.root, text="Registrar um aluno", command=self.registerStudents)
        studentRegister.pack()

        showStudents = Button(self.root, text="Mostrar todos alunos", command=self.showStudents)
        showStudents.pack()

        editStudents = Button(self.root, text="Editar nota do aluno", command=self.findStudent)
        editStudents.pack()

    def topRoot(self):
        self.root2 = Toplevel()
        # self.root2.destroy()
        self.root2.geometry("1800x500")

    def registerStudents(self):
        self.topRoot()
          
        title = Label(self.root2, text="REGISTRAR ALUNO")
        title.pack()

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

        submit = Button(self.root2, text="Enviar", command=self.saveStudent)
        submit.pack()

    def saveStudent(self):
        print(self.name.get(), self.email.get(), self.rgm.get(), self.password.get())
        self.db.insert(self.name.get(), self.email.get(), self.rgm.get(), self.password.get())

    def showStudents(self):
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

        users = self.db.getStudents()

        for user in users:
            print(user)
            table.insert("", "end", text=user[0], values=(user[1], user[2], user[3], user[5], user[6], user[7], user[8]))

        table.pack(expand=True, fill="both")

    def findStudent(self):
        self.topRoot()

        findId = Label(self.root2, text="Digite o id do aluno: ")
        findId.pack()
        findIdEntry = Entry(self.root2)
        findIdEntry.pack()
        findIdButton = Button(self.root2, text="Encontrar", command=lambda: self.editStudent(findIdEntry.get()))
        findIdButton.pack()


    def editStudent(self, id):
        aluno = self.db.getStudentById(id)

        title = Label(self.root2, text=f"EDITANDO NOTA DE: {aluno[1]}")
        title.pack()

        a2Label = Label(self.root2, text="Nota A2: ")
        a2Label.pack()
        a2 = Entry(self.root2)
        a2.pack()

        a1Label = Label(self.root2, text="Nota A1: ")
        a1Label.pack()
        a1 = Entry(self.root2)
        a1.pack()

        atividadesLabel = Label(self.root2, text="Nota de Atividades: ")
        atividadesLabel.pack()
        atividades = Entry(self.root2)
        atividades.pack()

        finalLabel = Label(self.root2, text="Nota Final: ")
        finalLabel.pack()
        final = Entry(self.root2)
        final.pack()

        submit = Button(self.root2, text="ATUALIZAR NOTA",
                        command=lambda: self.db.updateGrade(id, a2.get(), a1.get(), atividades.get(), final.get()))
        submit.pack()


def app():
    root = Tk()
    Application(root)
    root.mainloop()


if __name__ == "__main__":
    app()
