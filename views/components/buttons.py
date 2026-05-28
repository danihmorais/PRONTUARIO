import customtkinter as ctk


class FooterButtons(ctk.CTkFrame):
    def __init__(self, master, theme_manager, on_editar=None, on_excluir=None):
        super().__init__(master, fg_color="transparent")

        self._tm = theme_manager
        self._editar = on_editar
        self._excluir = on_excluir

        self._themed_widgets = []

        self.grid_columnconfigure(0, weight=1)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=0, column=1, sticky="e")

        btn_frame.grid_columnconfigure(0, weight=0)
        btn_frame.grid_columnconfigure(1, weight=0)

        self.btn_editar = ctk.CTkButton(
            btn_frame,
            width=130,
            height=40,
            text="✏  Editar",
            fg_color=self._tm.c("BLUE"),
            hover_color=self._tm.c("DARK_BLUE"),
            text_color=self._tm.c("TOPBAR_TEXT"),
            font=(self._tm.font, 13, "bold"),
            corner_radius=8,
            command=self._editar,
        )
        self.btn_editar.grid(row=0, column=0, padx=(0, 10), sticky="e")

        self.btn_excluir = ctk.CTkButton(
            btn_frame,
            width=130,
            height=40,
            text="🗑  Excluir",
            fg_color=self._tm.c("RED_LIGHT"),
            hover_color=self._tm.c("RED"),
            text_color=self._tm.c("RED"),
            font=(self._tm.font, 13, "bold"),
            corner_radius=8,
            command=self._excluir,
        )
        self.btn_excluir.grid(row=0, column=1, sticky="e")

        self._tw(self.btn_editar, fg_color="BLUE", hover_color="DARK_BLUE", text_color="TOPBAR_TEXT")
        self._tw(self.btn_excluir, fg_color="RED_LIGHT", hover_color="RED", text_color="RED")

    def _tw(self, widget, **keys):
        self._themed_widgets.append({
            "widget": widget,
            "keys": keys
        })

    def apply_theme(self, colors):
        alive = []

        for item in self._themed_widgets:
            widget = item["widget"]
            keys = item["keys"]

            try:
                if widget.winfo_exists():
                    alive.append(item)

                    cfg = {
                        param: colors[color_key]
                        for param, color_key in keys.items()
                        if color_key in colors
                    }

                    if cfg:
                        widget.configure(**cfg)

            except Exception:
                pass

        self._themed_widgets = alive