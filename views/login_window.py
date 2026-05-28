import customtkinter as ctk
from tkinter import END
from PIL import Image
import sqlite3
import hashlib
from database import inicializar_banco
from theme_manager import ThemeManager
from views.components.theme_switch import ThemeSwitch
from config import DB_PATH


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

        # Garante que o banco principal está inicializado
        inicializar_banco()

        self._build_ui()
        self.bind("<Return>", lambda event: self.login())

        self.theme_switch = ThemeSwitch(self)
        self.theme_switch.place(x=20, y=20)

        self.update_idletasks()
        self._center_window()

        self._tm.subscribe(self._on_theme_change)
        self._on_theme_change(self._tm.colors)

    def _build_ui(self):
        try:
            self.bg_img = ctk.CTkImage(
                light_image=Image.open('assets/BG_Inicial.png'),
                dark_image=Image.open('assets/BG_Inicial.png'),
                size=(579, 500)
            )
            self.lb_image = ctk.CTkLabel(self, image=self.bg_img, text="", fg_color=self._tm.c("WHITE"))
            self.lb_image.place(x=0, y=0)
        except Exception:
            self.lb_image = ctk.CTkFrame(self, width=579, height=500, fg_color=self._tm.c("BLUE"))
            self.lb_image.place(x=0, y=0)

        try:
            self.logo_img = ctk.CTkImage(
                light_image=Image.open('assets/logo.png'),
                dark_image=Image.open('assets/logo.png'),
                size=(70, 70)
            )
            self.lb_logo = ctk.CTkLabel(self, image=self.logo_img, text="", fg_color=self._tm.c("WHITE"))
            self.lb_logo.place(x=579 + (321 // 2) - 35, y=24)
        except Exception:
            self.lb_logo = ctk.CTkLabel(self, text="🏥", font=(self._tm.font, 40), fg_color=self._tm.c("WHITE"))
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
            text_color=self._tm.c("BLACK"), fg_color=self._tm.c("BLUE_XL"),
            font=(self._tm.font, 14)
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
        self.bt_entrar.place(x=630, y=420)

        self.lb_feedback = ctk.CTkLabel(
            self,
            text="",
            width=260,
            text_color=self._tm.c("RED"),
            font=(self._tm.font, 12),
            fg_color=self._tm.c("BLUE_XL"),
            justify="center"
        )
        self.lb_feedback.place(x=610, y=390)

        self.subtitulo_rodape = ctk.CTkLabel(
            self,
            text='Dúvidas ou problemas? Entre em contato\ncom nosso suporte técnico.',
            text_color=self._tm.c("GRAY"), font=(self._tm.font, 10),
            justify='center', fg_color=self._tm.c("BLUE_XL")
        )
        self.subtitulo_rodape.place(x=648, y=462)

    def _center_window(self):
        self.update_idletasks()
        scale = self._get_window_scaling()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = int(((sw - self._width)  // 2) * scale)
        y = (sh - self._height) // 2
        self.geometry(f"{self._width}x{self._height}+{x}+{y}")

    def _on_theme_change(self, colors: dict):
        self.configure(fg_color=colors["WHITE"])
        
        if hasattr(self, 'bg_img'):
            self.lb_image.configure(fg_color=colors["WHITE"])
            
        self.lb_logo.configure(fg_color=colors["WHITE"])
        self.fr_login.configure(fg_color=colors["BLUE_XL"])
        self.titulo.configure(text_color=colors["BLACK"])
        self.subtitulo.configure(text_color=colors["BLACK"])
        self.lb_usuario.configure(text_color=colors["BLACK"], fg_color=colors["BLUE_XL"])
        self.lb_senha.configure(text_color=colors["BLACK"], fg_color=colors["BLUE_XL"])
        self.subtitulo_rodape.configure(text_color=colors["GRAY"], fg_color=colors["BLUE_XL"])
        
        self.entry_usuario.configure(
            fg_color=colors["WHITE"], text_color=colors["BLACK"],
            border_color=colors["DARK_BLUE"], placeholder_text_color=colors["GRAY"] # <--- Placeholder rastreado
        )
        self.entry_senha.configure(
            fg_color=colors["WHITE"], text_color=colors["BLACK"],
            border_color=colors["DARK_BLUE"], placeholder_text_color=colors["GRAY"] # <--- Placeholder rastreado
        )
        self.bt_entrar.configure(
            fg_color=colors["BLUE"], hover_color=colors["DARK_BLUE"],
            text_color=colors["TOPBAR_TEXT"],
        )
        self.lb_feedback.configure(fg_color=colors["BLUE_XL"], text_color=colors["RED"])

    def login(self):
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get().strip()

        if not usuario or not senha:
            self.lb_feedback.configure(text="Preencha usuário e senha.")
            return

        senha_hash = hashlib.sha256(senha.encode()).hexdigest()

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT usuario FROM usuarios WHERE usuario = ? AND senha = ?",
                (usuario, senha_hash)
            )
            resultado = cursor.fetchone()
            conn.close()
        except Exception as e:
            self.lb_feedback.configure(text=f"Erro de banco: {e}")
            return

        if resultado:
            self.lb_feedback.configure(text="")
            self._tm.unsubscribe(self._on_theme_change)
            self.controller.open_main(self)
        else:
            self.lb_feedback.configure(text="Usuário ou senha inválidos.")
            self.entry_senha.delete(0, END)
            self.entry_senha.focus()