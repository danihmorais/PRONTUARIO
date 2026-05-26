import ctypes
import sys
import threading
import time

import customtkinter as ctk

from controllers.app_controller import AppController
from updater import (
    verificar_e_atualizar,
    perguntar_atualizacao,
    executar_modo_update,
)


def checar_update_background(app_root):
    try:
        data = verificar_e_atualizar()

        if not data:
            return

        app_root.after(
            0,
            lambda: perguntar_atualizacao(data)
        )

    except Exception as e:
        print(e)


if __name__ == "__main__":

    if "--apply-update" in sys.argv:
        executar_modo_update()
        sys.exit()

    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        pass

    ctk.set_default_color_theme("blue")

    app = AppController()

    app.iniciar()

    threading.Thread(
        target=lambda: (
            time.sleep(2),
            checar_update_background(app.app)
        ),
        daemon=True
    ).start()

    app.app.mainloop()