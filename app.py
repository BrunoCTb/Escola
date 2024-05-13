from tkinter import *


class Front:
    def __init__(self, master):
        self.root = master
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

        self.submit = Button(self.root, text="Enviar").pack()



def app():
    root = Tk()
    Front(root)
    root.mainloop()

app()
        
