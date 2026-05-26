"""
main_window.py
Janela de login do MediSystem com suporte a modo claro/escuro.
"""

import customtkinter as ctk
from tkinter import END
from PIL import Image
import sqlite3
from layout import layout
from theme_manager import ThemeManager


class MainWindow(ctk.CTk, layout):

    def __init__(self, controller):
        super().__init__()
        layout.__init__(self)

        self.controller = controller

        width  = 900
        height = 500

        self.title("Bem-Vindo!")

        x = (self.winfo_screenwidth()  // 2) - (width  // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)

        self.geometry(f"{width}x{height}+{x}+{y}")
        self.resizable(False, False)
        self.iconbitmap('assets/icon.ico')

        self.monta_tabela_usuario()

        # ── ThemeManager ──────────────────────────────────────────────────
        self._tm = ThemeManager.get()
        self._tm.subscribe(self._on_theme_change)

        # Sincroniza o CTK com o estado atual do tema
        ctk.set_appearance_mode("dark" if self._tm.is_dark else "light")

        # ── Imagem de fundo ───────────────────────────────────────────────
        self.bg_img = ctk.CTkImage(
            light_image=Image.open('assets/BG_Inicial.png'),
            dark_image=Image.open('assets/BG_Inicial.png'),
            size=(579, 500)
        )
        self.lb_image = ctk.CTkLabel(
            self, image=self.bg_img, text="", fg_color=self.WHITE)
        self.lb_image.place(x=0, y=0)

        # ── Logo ──────────────────────────────────────────────────────────
        self.logo_img = ctk.CTkImage(
            light_image=Image.open('assets/logo.png'),
            dark_image=Image.open('assets/logo.png'),
            size=(70, 70)
        )
        self.lb_logo = ctk.CTkLabel(
            self, image=self.logo_img, text="", fg_color=self.WHITE)
        self.lb_logo.place(x=579 + (321 // 2) - 35, y=24)

        # ── Frame do formulário ───────────────────────────────────────────
        self.fr_login = ctk.CTkFrame(
            self, width=321, height=340,
            fg_color=self.BLUE_XL,
            corner_radius=16
        )
        self.fr_login.place(x=579, y=230)

        # ── Textos ────────────────────────────────────────────────────────
        self.titulo = ctk.CTkLabel(
            self, text='Bem-vindo de\nvolta!',
            text_color=self.BLACK,
            font=('Segoe UI', 28, 'bold'), justify='left'
        )
        self.titulo.place(x=610, y=110)

        self.subtitulo = ctk.CTkLabel(
            self, text='Faça o login para acessar sua conta:',
            text_color=self.BLACK,
            font=('Segoe UI', 12)
        )
        self.subtitulo.place(x=610, y=190)

        self.lb_usuario = ctk.CTkLabel(
            self, text='Usuário',
            text_color=self.BLACK, fg_color="transparent",
            font=('Segoe UI', 14)
        )
        self.lb_usuario.place(x=610, y=250)

        # ── Entradas ──────────────────────────────────────────────────────
        self.entry_usuario = ctk.CTkEntry(
            self, width=260, height=32,
            font=('Segoe UI', 14),
            text_color=self.BLACK,
            border_color=self.DARK_BLUE, border_width=1.5,
            corner_radius=8,
            fg_color=self.WHITE,
            placeholder_text='Ex. usuario123',
            placeholder_text_color=self.GRAY
        )
        self.entry_usuario.place(x=610, y=280)

        self.lb_senha = ctk.CTkLabel(
            self, text='Senha',
            text_color=self.BLACK,
            font=('Segoe UI', 14)
        )
        self.lb_senha.place(x=610, y=320)

        self.entry_senha = ctk.CTkEntry(
            self, width=260, height=32,
            font=('Segoe UI', 14),
            text_color=self.BLACK,
            border_color=self.DARK_BLUE, border_width=1.5,
            corner_radius=8,
            fg_color=self.WHITE,
            placeholder_text='Insira sua senha',
            placeholder_text_color=self.GRAY,
            show='*'
        )
        self.entry_senha.place(x=610, y=350)

        # ── Botão entrar ──────────────────────────────────────────────────
        self.bt_entrar = ctk.CTkButton(
            self, width=220, height=34,
            text='Entrar',
            font=('Segoe UI', 12, 'bold'),
            fg_color=self.BLUE, hover_color=self.DARK_BLUE,
            corner_radius=8,
            command=self.login
        )
        self.bt_entrar.place(x=630, y=400)

        # ── Botão de tema (canto superior direito do painel) ──────────────
        self._theme_btn = ctk.CTkButton(
            self,
            text=self._theme_icon(),
            width=32, height=28,
            font=('Segoe UI', 14),
            fg_color=self.BLUE_XL,
            hover_color=self.GRAY_LIGHT,
            text_color=self.GRAY_DARK,
            corner_radius=8,
            command=self._toggle_theme,
        )
        self._theme_btn.place(x=868, y=8)

        # ── Rodapé ────────────────────────────────────────────────────────
        self.subtitulo_rodape = ctk.CTkLabel(
            self,
            text='Dúvidas ou problemas? Entre em contato\ncom nosso suporte técnico.',
            text_color=self.GRAY,
            font=('Segoe UI', 10), justify='center'
        )
        self.subtitulo_rodape.place(x=648, y=456)

        # Aplica cores iniciais
        self._on_theme_change(self._tm.colors)

    # ── Tema ──────────────────────────────────────────────────────────────────

    def _theme_icon(self) -> str:
        return "☀️" if self._tm.is_dark else "🌙"

    def _toggle_theme(self):
        self._tm.toggle()  # dispara _on_theme_change via subscribe

    def _on_theme_change(self, colors: dict):
        """Recolore todos os widgets da janela de login."""
        self.configure(fg_color=colors["WHITE"])

        self.lb_image.configure(fg_color=colors["WHITE"])
        self.lb_logo.configure(fg_color=colors["WHITE"])

        self.fr_login.configure(fg_color=colors["BLUE_XL"])

        self.titulo.configure(text_color=colors["BLACK"])
        self.subtitulo.configure(text_color=colors["BLACK"])
        self.lb_usuario.configure(text_color=colors["BLACK"])
        self.lb_senha.configure(text_color=colors["BLACK"])
        self.subtitulo_rodape.configure(text_color=colors["GRAY"])

        self.entry_usuario.configure(
            fg_color=colors["WHITE"],
            text_color=colors["BLACK"],
            border_color=colors["DARK_BLUE"],
        )
        self.entry_senha.configure(
            fg_color=colors["WHITE"],
            text_color=colors["BLACK"],
            border_color=colors["DARK_BLUE"],
        )

        self.bt_entrar.configure(
            fg_color=colors["BLUE"],
            hover_color=colors["DARK_BLUE"],
            text_color=colors["TOPBAR_TEXT"],
        )

        self._theme_btn.configure(
            text=self._theme_icon(),
            fg_color=colors["BLUE_XL"],
            hover_color=colors["GRAY_LIGHT"],
            text_color=colors["GRAY_DARK"],
        )

    # ── Login / BD ────────────────────────────────────────────────────────────

    def login(self):
        self.conecta_bd()

        usuario = self.entry_usuario.get()
        senha   = self.entry_senha.get()

        self.cursor.execute(
            "SELECT usuario FROM usuarios WHERE usuario = ? AND senha = ?",
            (usuario, senha)
        )
        resultado = self.cursor.fetchall()

        if resultado:
            self._tm.unsubscribe(self._on_theme_change)
            self.controller.abrir_principal(self)
        else:
            self.entry_usuario.delete(0, END)
            self.entry_senha.delete(0, END)

    def conecta_bd(self):
        self.conn   = sqlite3.connect('usuarios.bd')
        self.cursor = self.conn.cursor()

    def desconecta_bd(self):
        self.conn.close()

    def monta_tabela_usuario(self):
        self.conecta_bd()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario INTEGER PRIMARY KEY,
                usuario    TEXT NOT NULL,
                senha      TEXT NOT NULL,
                nivel      TEXT NOT NULL
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