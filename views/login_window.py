import customtkinter as ctk
import sqlite3
import hashlib
from PIL import Image
from theme_manager import ThemeManager
from config import BASE_DIR, DB_PATH
import os

def carregar_imagem_segura(caminho, size):
    try:
        return Image.open(caminho)
    except Exception:
        return Image.new('RGBA', size, (0, 0, 0, 0))

class LoginWindow(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self._tm = ThemeManager.get()
        self.controller = controller
        self._width = 900
        self._height = 500
        self.title("Bem-Vindo!")
        self.resizable(False, False)
        
        try:
            self.iconbitmap(os.path.join(BASE_DIR, "assets", "icon.ico"))
        except Exception:
            pass
            
        ctk.set_appearance_mode("dark" if self._tm.is_dark else "light")
        self.withdraw()
        self._build_ui()
        self.update_idletasks()
        self._center_window()
        self._tm.subscribe(self._on_theme_change)
        self._on_theme_change(self._tm.colors)
        self.deiconify()

    def _build_ui(self):
        img_bg_path = os.path.join(BASE_DIR, "assets", "BG_Inicial.png")
        img_logo_path = os.path.join(BASE_DIR, "assets", "logo.png")

        self.bg_img = ctk.CTkImage(
            light_image=carregar_imagem_segura(img_bg_path, (579, 500)),
            dark_image=carregar_imagem_segura(img_bg_path, (579, 500)),
            size=(579, 500)
        )
        self.lb_image = ctk.CTkLabel(self, image=self.bg_img, text="", fg_color=self._tm.c("WHITE"))
        self.lb_image.place(x=0, y=0)
        
        self.logo_img = ctk.CTkImage(
            light_image=carregar_imagem_segura(img_logo_path, (70, 70)),
            dark_image=carregar_imagem_segura(img_logo_path, (70, 70)),
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
            font=('Segoe UI', 28, 'bold'), justify='left'
        )
        self.titulo.place(x=610, y=110)
        
        self.subtitulo = ctk.CTkLabel(
            self, text='Faça o login para acessar sua conta:',
            text_color=self._tm.c("BLACK"), font=(self._tm.font, 12)
        )
        self.subtitulo.place(x=610, y=190)
        
        self.lb_usuario = ctk.CTkLabel(
            self, text='Usuário',
            text_color=self._tm.c("BLACK"), fg_color="transparent",
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
        self.entry_usuario.bind("<Key>", self.ocultar_erro)
        
        self.lb_senha = ctk.CTkLabel(
            self, text='Senha',
            text_color=self._tm.c("BLACK"), font=(self._tm.font, 14)
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
        self.entry_senha.bind("<Key>", self.ocultar_erro)
        
        self.bt_entrar = ctk.CTkButton(
            self, width=220, height=34,
            text='Entrar', font=(self._tm.font, 12, 'bold'),
            fg_color=self._tm.c("BLUE"), hover_color=self._tm.c("DARK_BLUE"),
            corner_radius=8, command=self.login
        )
        self.bt_entrar.place(x=630, y=400)
        
        self.lb_erro = ctk.CTkLabel(
            self, text='Credenciais inválidas!',
            text_color=self._tm.c("RED"), font=(self._tm.font, 12, 'bold')
        )
        
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
            text_color=self._tm.c("GRAY"), font=(self._tm.font, 10), justify='center'
        )
        self.subtitulo_rodape.place(x=648, y=456)

    def _center_window(self):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = int((sw - self._width) / 2)
        y = int((sh - self._height) / 2)
        self.geometry(f"{self._width}x{self._height}+{x}+{y}")

    def _theme_icon(self) -> str:
        return "☀️" if self._tm.is_dark else "🌙"

    def _toggle_theme(self):
        self._tm.toggle()

    def _on_theme_change(self, colors: dict):
        self.configure(fg_color=colors.get("WHITE", "white"))
        self.lb_image.configure(fg_color=colors.get("WHITE", "white"))
        self.lb_logo.configure(fg_color=colors.get("WHITE", "white"))
        self.fr_login.configure(fg_color=colors.get("BLUE_XL", "blue"))
        self.titulo.configure(text_color=colors.get("BLACK", "black"))
        self.subtitulo.configure(text_color=colors.get("BLACK", "black"))
        self.lb_usuario.configure(text_color=colors.get("BLACK", "black"))
        self.lb_senha.configure(text_color=colors.get("BLACK", "black"))
        self.subtitulo_rodape.configure(text_color=colors.get("GRAY", "gray"))
        self.entry_usuario.configure(
            fg_color=colors.get("WHITE", "white"),
            text_color=colors.get("BLACK", "black"),
            border_color=colors.get("DARK_BLUE", "darkblue"),
        )
        self.entry_senha.configure(
            fg_color=colors.get("WHITE", "white"),
            text_color=colors.get("BLACK", "black"),
            border_color=colors.get("DARK_BLUE", "darkblue"),
        )
        self.bt_entrar.configure(
            fg_color=colors.get("BLUE", "blue"),
            hover_color=colors.get("DARK_BLUE", "darkblue"),
            text_color=colors.get("TOPBAR_TEXT", "white"),
        )
        self._theme_btn.configure(
            text=self._theme_icon(),
            fg_color=colors.get("BLUE_XL", "blue"),
            hover_color=colors.get("GRAY_LIGHT", "gray"),
            text_color=colors.get("GRAY_DARK", "darkgray"),
        )

    def ocultar_erro(self, event=None):
        self.lb_erro.place_forget()

    def login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        try:
            self.conecta_bd()
            self.cursor.execute(
                "SELECT usuario FROM usuarios WHERE usuario = ? AND senha = ?",
                (usuario, senha_hash)
            )
            resultado = self.cursor.fetchall()
            if resultado:
                self._tm.unsubscribe(self._on_theme_change)
                self.controller.open_main(self)
            else:
                self.lb_erro.place(x=630, y=440)
        except Exception:
            pass
        finally:
            self.desconecta_bd()

    def conecta_bd(self):
        try:
            self.conn = sqlite3.connect(DB_PATH)
            self.cursor = self.conn.cursor()
        except Exception:
            pass

    def desconecta_bd(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()