import customtkinter as ctk

class ComponentThemeSelector:

    def _build_theme_selector(self):

        self.theme_selector = ctk.CTkSegmentedButton(
            self,
            values=["Claro", "Escuro", "Auto"],
            command=self.mudar_tema
        )

        tema_atual = self.controller.get_tema_atual()

        mapa = {
            "Light": "Claro",
            "Dark": "Escuro",
            "System": "Auto"
        }

        self.theme_selector.set(mapa.get(tema_atual, "Auto"))

    def mudar_tema(self, valor):

        mapa = {
            "Claro": "Light",
            "Escuro": "Dark",
            "Auto": "System"
        }

        self.controller.alternar_tema(mapa.get(valor, "System"))