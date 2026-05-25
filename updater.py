import os
import sys
import json
import time
import shutil
import tempfile
import subprocess
import threading
import urllib.request
import urllib.error

import customtkinter as ctk

from tkinter import messagebox
from PIL import Image
from build_info import BUILD_DATE

try:
    from ctypes import windll
except ImportError:
    windll = None


REPO_URL = "https://api.github.com/repos/danihmorais/PRONTUARIO/releases/latest"
DOWNLOAD_TIMEOUT = 60

if getattr(sys, "frozen", False):
    _BASE_DIR = sys._MEIPASS
else:
    _BASE_DIR = os.path.dirname(os.path.abspath(__file__))

_LOGO_PNG = os.path.join(_BASE_DIR, "assets", "logo.png")
_LOGO_ICO = os.path.join(_BASE_DIR, "assets", "logo.ico")


def verificar_e_atualizar():
    try:
        req = urllib.request.Request(
            REPO_URL,
            headers={"User-Agent": "Prontuario-Updater"}
        )

        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())

        latest_date = data.get("published_at")

        if not latest_date:
            return None

        if latest_date <= BUILD_DATE:
            return None

        return data

    except Exception:
        return None


def perguntar_atualizacao(data):
    try:
        latest_date = data.get("published_at")

        resposta = messagebox.askyesno(
            "Atualização disponível",
            f"Nova atualização publicada em:\n{latest_date}\n\nDeseja atualizar?"
        )

        if not resposta:
            return False

        baixar_e_instalar_update(data)
        return True

    except Exception as e:
        messagebox.showerror(
            "Erro",
            f"Erro ao iniciar atualização:\n{str(e)}"
        )
        return False


def baixar_e_instalar_update(data):

    if not getattr(sys, "frozen", False):
        messagebox.showwarning(
            "Atualização",
            "Somente versão compilada."
        )
        return False

    download_url = None

    for asset in data.get("assets", []):
        nome = asset.get("name", "").lower()

        if nome.endswith(".exe"):
            download_url = asset.get("browser_download_url")
            break

    if not download_url:
        messagebox.showerror(
            "Erro",
            "Nenhum executável encontrado."
        )
        return False

    temp_dir = tempfile.mkdtemp(prefix="prontuario_update_")

    try:

        new_exe_path = os.path.join(
            temp_dir,
            "Prontuario_new.tmp"
        )

        req_dl = urllib.request.Request(
            download_url,
            headers={"User-Agent": "Prontuario-Updater"}
        )

        with urllib.request.urlopen(
            req_dl,
            timeout=DOWNLOAD_TIMEOUT
        ) as response, open(new_exe_path, "wb") as arquivo:

            shutil.copyfileobj(response, arquivo)

        current_exe = os.path.abspath(sys.executable)

        updater_copy = os.path.join(
            tempfile.gettempdir(),
            "Prontuario_Updater.exe"
        )

        if os.path.exists(updater_copy):
            try:
                os.remove(updater_copy)
            except Exception:
                pass

        shutil.copy2(current_exe, updater_copy)

        subprocess.Popen(
            [
                updater_copy,
                "--apply-update",
                current_exe,
                new_exe_path
            ],
            close_fds=True
        )

        os._exit(0)

    except Exception as e:

        messagebox.showerror(
            "Erro",
            f"Erro durante atualização:\n{str(e)}"
        )

        return False

    finally:
        try:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass


class _UpdateWindow(ctk.CTk):

    WIDTH = 540
    HEIGHT = 300

    _STEPS = [
        ("Aguardando encerramento da aplicação...", 2),
        ("Criando backup da versão atual...", 1),
        ("Instalando nova versão...", 2),
        ("Finalizando instalação...", 1),
        ("Abrindo nova versão...", 1),
    ]

    def __init__(self, old_exe: str, new_exe: str):
        super().__init__()

        self.old_exe = old_exe
        self.new_exe = new_exe

        self.title("Prontuario — Atualizando")
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        self.resizable(False, False)

        self.protocol(
            "WM_DELETE_WINDOW",
            lambda: None
        )

        self.configure(
            fg_color=("#EDEDED", "#171717")
        )

        self._set_icon()
        self._build_ui()

        self.after(10, self._center_window)

        self.lift()
        self.focus_force()

        self.attributes("-topmost", True)

        self.after(
            150,
            lambda: self.attributes("-topmost", False)
        )

        threading.Thread(
            target=self._run_update,
            daemon=True
        ).start()

    def _center_window(self):

        self.update()

        width = self.winfo_width()
        height = self.winfo_height()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.geometry(f"+{x}+{y}")

    def _set_icon(self):

        if os.path.exists(_LOGO_ICO):
            try:
                self.after(
                    0,
                    lambda: self.iconbitmap(_LOGO_ICO)
                )
            except Exception:
                pass

    def _build_ui(self):

        self.grid_columnconfigure(0, weight=1)

        if os.path.exists(_LOGO_PNG):

            try:

                img = Image.open(_LOGO_PNG)

                self._logo = ctk.CTkImage(
                    img,
                    img,
                    size=(56, 56)
                )

                ctk.CTkLabel(
                    self,
                    text="",
                    image=self._logo
                ).grid(
                    row=0,
                    column=0,
                    pady=(30, 0)
                )

                base_row = 1

            except Exception:
                base_row = 0

        else:
            base_row = 0

        ctk.CTkLabel(
            self,
            text="Atualizando Prontuario",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        ).grid(
            row=base_row,
            column=0
        )

        ctk.CTkLabel(
            self,
            text="Aguarde...",
            text_color=("gray45", "gray65")
        ).grid(
            row=base_row + 1,
            column=0
        )

        self._progress = ctk.DoubleVar(value=0)

        self._bar = ctk.CTkProgressBar(
            self,
            variable=self._progress,
            width=400
        )

        self._bar.grid(
            row=base_row + 2,
            column=0,
            pady=10
        )

        self._status = ctk.CTkLabel(
            self,
            text="Iniciando..."
        )

        self._status.grid(
            row=base_row + 3,
            column=0
        )

    def _set_status(self, texto):

        self.after(
            0,
            lambda: self._status.configure(text=texto)
        )

    def _set_progress(self, valor):

        self.after(
            0,
            lambda: self._progress.set(valor)
        )

    def _run_update(self):

        total = sum(
            duracao
            for _, duracao in self._STEPS
        )

        elapsed = 0

        try:

            for msg, duration in self._STEPS:

                self._set_status(msg)

                for _ in range(20):

                    time.sleep(duration / 20)

                    elapsed += duration / 20

                    self._set_progress(
                        min(elapsed / total, 0.99)
                    )

                self._execute_step(msg)

            self._set_progress(1.0)

            self._set_status("Concluído")

            time.sleep(1)

            self.after(0, self.destroy)

            os._exit(0)

        except Exception as e:

            self._set_status(
                f"Erro: {str(e)}"
            )

    def _execute_step(self, msg):

        old_backup = self.old_exe + ".old"

        if "backup" in msg.lower():

            if os.path.exists(old_backup):

                try:
                    os.remove(old_backup)
                except Exception:
                    pass

            if os.path.exists(self.old_exe):

                os.replace(
                    self.old_exe,
                    old_backup
                )

        elif "instalando" in msg.lower():

            try:

                os.replace(
                    self.new_exe,
                    self.old_exe
                )

            except Exception:

                if os.path.exists(old_backup):

                    os.replace(
                        old_backup,
                        self.old_exe
                    )

                raise

        elif "abrindo" in msg.lower():

            process = subprocess.Popen(
                [self.old_exe],
                close_fds=True
            )

            time.sleep(3)

            if process.poll() is None:

                try:
                    if os.path.exists(old_backup):
                        os.remove(old_backup)
                except Exception:
                    pass

            else:

                try:

                    if os.path.exists(old_backup):

                        if os.path.exists(self.old_exe):
                            os.remove(self.old_exe)

                        os.replace(
                            old_backup,
                            self.old_exe
                        )

                except Exception:
                    pass

                raise RuntimeError(
                    "Falha ao iniciar a nova versão. "
                    "Backup restaurado."
                )


def executar_modo_update():

    try:
        if windll:
            windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        pass

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    old_exe = sys.argv[2]
    new_exe = sys.argv[3]

    app = _UpdateWindow(
        old_exe,
        new_exe
    )

    app.mainloop()