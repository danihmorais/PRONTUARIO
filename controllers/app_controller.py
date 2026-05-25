from views.main_window import MainWindow
from views.principal_window import PrincipalWindow
from views.cadastro_window import CadastroWindow
from views.consulta_window import ConsultaWindows
import customtkinter as ctk
import config
import os
import json

class AppController:

    def __init__(self):
        self.app = None

    def iniciar(self):
        tema = self.get_tema_atual()
        ctk.set_appearance_mode(tema)
        self.app = MainWindow(self)
        self.app.mainloop()

    def abrir_principal(self, parent_window):
        PrincipalWindow(parent_window, self)

    def abrir_cadastro(self, parent_window):
        CadastroWindow(parent_window, self)

    def abrir_consulta(self, parent_window):
        ConsultaWindows(parent_window, self)

    def realizar_logout(self, parent_window):
        parent_window.destroy()
        self.iniciar()

    def get_tema_atual(self):
        if os.path.exists(config.ARQUIVO_DADOS):
            try:
                with open(config.ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                    return dados.get("tema", "System")
            except Exception:
                return "System"
        return "System"

    def alternar_tema(self, novo_tema):
        ctk.set_appearance_mode(novo_tema)

        dados = {}

        if os.path.exists(config.ARQUIVO_DADOS):
            try:
                with open(config.ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                    dados = json.load(f)
            except Exception:
                pass

        dados["tema"] = novo_tema

        with open(config.ARQUIVO_DADOS, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)

        if self.app:
            self.app.atualizar_tema_ui()