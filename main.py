import traceback
import sys

try:
    import ctypes
    import threading
    import time
    import customtkinter as ctk

    from controllers.app_controller import AppController
    from updater import (
        verificar_e_atualizar,
        perguntar_atualizacao,
        executar_modo_update,
    )

    def checar_update_background(controller):
        try:
            data = verificar_e_atualizar()
            if not data:
                return
            if controller.app and controller.app.winfo_exists():
                controller.app.after(0, lambda: perguntar_atualizacao(data))
        except Exception:
            pass

    if __name__ == "__main__":
        if "--apply-update" in sys.argv:
            executar_modo_update()
            sys.exit()

        ctk.set_default_color_theme("blue")

        app = AppController()
        app.iniciar()

        threading.Thread(
            target=lambda: (
                time.sleep(2),
                checar_update_background(app)
            ),
            daemon=True
        ).start()

        app.app.mainloop()

except Exception as e:
    print("ERRO CRÍTICO NA INICIALIZAÇÃO:")
    traceback.print_exc()
    if sys.stdin and sys.stdin.isatty():
        input("\nPressione ENTER para fechar a janela...")