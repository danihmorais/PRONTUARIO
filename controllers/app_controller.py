import customtkinter as ctk
from views.login_window import LoginWindow
from views.main_window import MainWindow

class AppController:
    def __init__(self):
        self.app = None

    def iniciar(self):
        self.app = LoginWindow(self)

    def open_main(self, parent_window):
        parent_window.destroy()
        self.app = MainWindow(self)
        self.app.mainloop()

    def realizar_logout(self, parent_window):
        parent_window.destroy()
        self.app = LoginWindow(self)
        self.app.mainloop()