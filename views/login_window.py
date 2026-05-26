import customtkinter as ctk
from tkinter import END
from PIL import Image
import sqlite3
from theme_manager import ThemeManager


class LoginWindow(ctk.CTk):

    def __init__(self, controller):
        super().__init__()

        self.controller = controller

        self._width  = 900
        self._height = 500

        self.title("Bem-Vindo!")
        self.resizable(False, False)
        self.iconbitmap('assets/icon.ico')

        self._tm = ThemeManager.get()
        ctk.set_appearance_mode("dark" if self._tm.is_dark else "light")

        self.monta_tabela_usuario()
        self._build_ui()

        self.update_idletasks()
        self._center_window()

        self._tm.subscribe(self._on_theme_change)
        self._on_theme_change(self._tm.colors)

    def _build_ui(self):
        self.bg_img = ctk.CTkImage(
            light_image=Image.open('assets/BG_Inicial.png'),
            dark_image=Image.open('assets/BG_Inicial.png'),
            size=(579, 500)
        )
        self.lb_image = ctk.CTkLabel(self, image=self.bg_img, text="", fg_color=self._tm.c("WHITE"))
        self.lb_image.place(x=0, y=0)

        self.logo_img = ctk.CTkImage(
            light_image=Image.open('assets/logo.png'),
            dark_image=Image.open('assets/logo.png'),
            size=(70, 70)
        )
        self.lb_logo = ctk.CTkLabel(self, image=self.logo_img, text="", fg_color=self._tm.c("WHITE"))
        self.lb_logo.place(x=579 + (321 // 2) - 35, y=24)

        self.fr_login = ctk.CTkFrame(
            self, width=321, height=340,
            fg_color=self._tm.c("BLUE_XL"), corner_radius=16
        )
        self.fr_login.place(x=579, y=230)

        self.titulo = ctk.CTkLabel(
            self, text='Bem-vindo de\nvolta!',
            text_color=self._tm.c("BLACK"),
            font=(self._tm.font, 28, 'bold'), justify='left'
        )
        self.titulo.place(x=610, y=110)

        self.subtitulo = ctk.CTkLabel(
            self, text='Faça o login para acessar sua conta:',
            text_color=self._tm.c("BLACK"), font=(self._tm.font, 12)
        )
        self.subtitulo.place(x=610, y=190)

        self.lb_usuario = ctk.CTkLabel(
            self, text='Usuário',
            text_color=self._tm.c("BLACK"), fg_color=self._tm.c("BLUE_XL"),
            font=(self._tm.font, 14)
        )
        self.lb_usuario.place(x=610, y=250)

        self.entry_usuario = ctk.CTkEntry(
            self, width=260, height=32,
            font=(self._tm.font, 14),
            text_color=self._tm.c("BLACK"),
            border_color=self._tm.c("DARK_BLUE"), border_width=1.5,
            corner_radius=8, fg_color=self._tm.c("WHITE"),
            placeholder_text='Ex. usuario123',
            placeholder_text_color=self._tm.c("GRAY")
        )
        self.entry_usuario.place(x=610, y=280)

        self.lb_senha = ctk.CTkLabel(
            self, text='Senha',
            text_color=self._tm.c("BLACK"), fg_color=self._tm.c("BLUE_XL"), font=(self._tm.font, 14)
        )
        self.lb_senha.place(x=610, y=320)

        self.entry_senha = ctk.CTkEntry(
            self, width=260, height=32,
            font=(self._tm.font, 14),
            text_color=self._tm.c("BLACK"),
            border_color=self._tm.c("DARK_BLUE"), border_width=1.5,
            corner_radius=8, fg_color=self._tm.c("WHITE"),
            placeholder_text='Insira sua senha',
            placeholder_text_color=self._tm.c("GRAY"),
            show='*'
        )
        self.entry_senha.place(x=610, y=350)

        self.bt_entrar = ctk.CTkButton(
            self, width=220, height=34,
            text='Entrar', font=(self._tm.font, 12, 'bold'),
            fg_color=self._tm.c("BLUE"), hover_color=self._tm.c("DARK_BLUE"),
            corner_radius=8, command=self.login
        )
        self.bt_entrar.place(x=630, y=400)

        self._theme_btn = ctk.CTkButton(
            self, text=self._theme_icon(),
            width=32, height=28,
            font=(self._tm.font, 14),
            fg_color=self._tm.c("BLUE_XL"), hover_color=self._tm.c("GRAY_LIGHT"),
            text_color=self._tm.c("GRAY_DARK"),
            corner_radius=8, command=self._toggle_theme,
        )
        self._theme_btn.place(x=868, y=8)

        self.subtitulo_rodape = ctk.CTkLabel(
            self,
            text='Dúvidas ou problemas? Entre em contato\ncom nosso suporte técnico.',
            text_color=self._tm.c("GRAY"), font=(self._tm.font, 10), justify='center', fg_color=self._tm.c("BLUE_XL")
        )
        self.subtitulo_rodape.place(x=648, y=456)

    def _center_window(self):
        self.update_idletasks()
        scale = self._get_window_scaling()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = int(((sw - self._width)  // 2) * scale)
        y = (sh - self._height) // 2
        self.geometry(f"{self._width}x{self._height}+{x}+{y}")

    def _theme_icon(self) -> str:
        return "☀️" if self._tm.is_dark else "🌙"

    def _toggle_theme(self):
        self._tm.toggle()

    def _on_theme_change(self, colors: dict):
        self.configure(fg_color=colors["WHITE"])

        self.lb_image.configure(fg_color=colors["WHITE"])
        self.lb_logo.configure(fg_color=colors["WHITE"])
        self.fr_login.configure(fg_color=colors["BLUE_XL"])

        self.titulo.configure(text_color=colors["BLACK"])
        self.subtitulo.configure(text_color=colors["BLACK"])
        self.lb_usuario.configure(
            text_color=colors["BLACK"],
            fg_color=colors["BLUE_XL"]
        )

        self.lb_senha.configure(
            text_color=colors["BLACK"],
            fg_color=colors["BLUE_XL"]
        )

        self.subtitulo_rodape.configure(
            text_color=colors["GRAY"],
            fg_color=colors["BLUE_XL"]
        )

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
            self.controller.open_main(self)
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