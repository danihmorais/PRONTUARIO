import customtkinter as ctk
from tkinter import END
from PIL import Image
import sqlite3
from layout import *
from views.components.theme import *

class MainWindow(ctk.CTk, layout, ComponentThemeSelector):

    def __init__(self, controller):
        super().__init__()
        layout.__init__(self)
        ComponentThemeSelector.__init__(self)

        self.controller = controller

        width = 900
        height = 500

        self.title("Bem-Vindo!")
        ctk.set_appearance_mode("light")

        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)

        self.geometry(f"{width}x{height}+{x}+{y}")
        self.resizable(False, False)
        self.iconbitmap('assets/icon.ico')

        self.monta_tabela_usuario()

        self.bg_img = ctk.CTkImage(
            light_image=Image.open('assets/BG_Inicial.png'),
            dark_image=Image.open('assets/BG_Inicial.png'),
            size=(579, 500)
        )

        self.lb_image = ctk.CTkLabel(
            self,
            image=self.bg_img,
            text="",
            fg_color=self.WHITE
        )
        self.lb_image.place(x=0, y=0)

        self._build_theme_selector()
        self.theme_selector.place(x=20, y=10)

        self.logo_img = ctk.CTkImage(
            light_image=Image.open('assets/logo.png'),
            dark_image=Image.open('assets/logo.png'),
            size=(70, 70)
        )

        self.lb_logo = ctk.CTkLabel(
            self,
            image=self.logo_img,
            text="",
            fg_color=self.WHITE
        )
        self.lb_logo.place(x=579 + (321 // 2) - 35, y=24)

        self.fr_login = ctk.CTkFrame(
            self,
            width=321,
            height=340,
            fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"],
            corner_radius=16
        )
        self.fr_login.place(x=579, y=230)

        self.titulo = ctk.CTkLabel(
            self,
            text='Bem-vindo de\nvolta!',
            text_color=self.BLACK,
            font=('Segoe UI', 28, 'bold'),
            justify='left'
        )
        self.titulo.place(x=610, y=110)

        self.subtitulo = ctk.CTkLabel(
            self,
            text='Faça o login para acessar sua conta:',
            text_color=self.BLACK,
            font=('Segoe UI', 12)
        )
        self.subtitulo.place(x=610, y=190)

        self.lb_usuario = ctk.CTkLabel(
            self,
            text='Usuário',
            text_color=self.BLACK,
            fg_color="transparent",
            font=('Segoe UI', 14)
        )
        self.lb_usuario.place(x=610, y=250)

        self.entry_usuario = ctk.CTkEntry(
            self,
            width=260,
            height=32,
            font=('Segoe UI', 14),
            text_color=self.BLACK,
            border_color=self.DARK_BLUE,
            border_width=1.5,
            corner_radius=8,
            fg_color=self.WHITE,
            placeholder_text='Ex. usuario123',
            placeholder_text_color=self.GRAY
        )
        self.entry_usuario.place(x=610, y=280)

        self.lb_senha = ctk.CTkLabel(
            self,
            text='Senha',
            text_color=self.BLACK,
            font=('Segoe UI', 14)
        )
        self.lb_senha.place(x=610, y=320)

        self.entry_senha = ctk.CTkEntry(
            self,
            width=260,
            height=32,
            font=('Segoe UI', 14),
            text_color=self.BLACK,
            border_color=self.DARK_BLUE,
            border_width=1.5,
            corner_radius=8,
            fg_color=self.WHITE,
            placeholder_text='Insira sua senha',
            placeholder_text_color=self.GRAY,
            show='*'
        )
        self.entry_senha.place(x=610, y=350)

        self.bt_entrar = ctk.CTkButton(
            self,
            width=220,
            height=34,
            text='Entrar',
            font=('Segoe UI', 12, 'bold'),
            fg_color=self.BLUE,
            hover_color=self.DARK_BLUE,
            corner_radius=8,
            command=self.login
        )
        self.bt_entrar.place(x=630, y=400)

        self.subtitulo_rodape = ctk.CTkLabel(
            self,
            text='Dúvidas ou problemas? Entre em contato\ncom nosso suporte técnico.',
            text_color=self.GRAY,
            font=('Segoe UI', 10),
            justify='center'
        )
        self.subtitulo_rodape.place(x=648, y=456)

    def atualizar_tema_ui(self):
        self.configure(fg_color=self.WHITE)

        self.lb_image.configure(fg_color=self.WHITE)
        self.lb_logo.configure(fg_color=self.WHITE)

        self.fr_login.configure(fg_color=self.BLUE_LIGHT_2)

        self.titulo.configure(text_color=self.BLACK)
        self.subtitulo.configure(text_color=self.BLACK)
        self.lb_usuario.configure(text_color=self.BLACK)
        self.lb_senha.configure(text_color=self.BLACK)
        self.subtitulo_rodape.configure(text_color=self.GRAY)

        self.entry_usuario.configure(
            fg_color=self.WHITE,
            text_color=self.BLACK,
            border_color=self.DARK_BLUE
        )

        self.entry_senha.configure(
            fg_color=self.WHITE,
            text_color=self.BLACK,
            border_color=self.DARK_BLUE
        )

    def login(self):
        self.conecta_bd()

        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        self.cursor.execute(
            "SELECT usuario FROM usuarios WHERE usuario = ? AND senha = ?",
            (usuario, senha)
        )

        resultado = self.cursor.fetchall()

        if resultado:
            self.controller.abrir_principal(self)
        else:
            self.entry_usuario.delete(0, END)
            self.entry_senha.delete(0, END)

    def conecta_bd(self):
        self.conn = sqlite3.connect('usuarios.bd')
        self.cursor = self.conn.cursor()

    def desconecta_bd(self):
        self.conn.close()

    def monta_tabela_usuario(self):
        self.conecta_bd()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario INTEGER PRIMARY KEY,
                usuario TEXT NOT NULL,
                senha TEXT NOT NULL,
                nivel TEXT NOT NULL
            );
        """)
        self.conn.commit()
        self.desconecta_bd()

    def cadastro_usuario(self):
        self.conecta_bd()
        self.cursor.execute(
            "INSERT INTO usuarios (usuario, senha, nivel) VALUES (?, ?, ?)",
            (self.entry_usuario.get(), self.entry_senha.get(), "Admin")
        )
        self.conn.commit()
        self.desconecta_bd()