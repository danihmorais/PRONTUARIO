import customtkinter as ctk
from theme_manager import ThemeManager

_STATUS_THEME_MAP = {
    "Confirmada": ("SUCCESS_BG", "SUCCESS"),
    "Pendente":   ("WARN_BG", "WARN"),
    "Cancelada":  ("RED_LIGHT", "RED"),
    "Realizada":  ("PURPLE_BG", "PURPLE"),
}


class Appointments(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        theme_manager: ThemeManager,
        data: list,
        on_confirm=None,
        on_cancel=None,
        on_delete=None
    ):
        super().__init__(parent, fg_color="transparent")

        self._tm = theme_manager
        self._data = data or []

        self._on_confirm = on_confirm
        self._on_cancel = on_cancel
        self._on_delete = on_delete

        self._build()

    def _build(self):
        self._panel = ctk.CTkFrame(
            self,
            fg_color=self._tm.c("WHITE"),
            corner_radius=10,
            border_width=1,
            border_color=self._tm.c("GRAY_LIGHT"),
        )
        self._panel.pack(fill="both", expand=True)

        self._build_header()
        self._build_body()

    def _build_header(self):
        header = ctk.CTkFrame(
            self._panel,
            fg_color=self._tm.c("BLUE_XL"),
            corner_radius=6,
        )
        header.pack(fill="x", padx=10, pady=(10, 10))

        columns = [
            ("Paciente", 200),
            ("Fisioterapeuta", 180),
            ("Data", 100),
            ("Hora", 70),
            ("Status", 110),
            ("Ações", 120),
        ]

        for txt, width in columns:
            ctk.CTkLabel(
                header,
                text=txt,
                width=width,
                anchor="w",
                font=(self._tm.font, 11, "bold"),
                text_color=self._tm.c("DARK_BLUE"),
            ).pack(side="left", padx=6, pady=6)

    def _build_body(self):
        self._scroll = ctk.CTkScrollableFrame(
            self._panel,
            fg_color="transparent",
        )
        self._scroll.pack(fill="both", expand=True, padx=6, pady=(0, 12))

        self._render_rows()

    def _render_rows(self):
        for w in self._scroll.winfo_children():
            w.destroy()

        if not self._data:
            ctk.CTkLabel(
                self._scroll,
                text="Nenhuma consulta encontrada.",
                font=(self._tm.font, 13),
                text_color=self._tm.c("GRAY"),
            ).pack(pady=20)
            return

        for i, row_data in enumerate(self._data):
            if len(row_data) < 6:
                continue

            cid, pac, fisio, data, hora, status = row_data

            bg_key = "WHITE" if i % 2 == 0 else "GRAY_BG"

            row = ctk.CTkFrame(
                self._scroll,
                fg_color=self._tm.c(bg_key),
                corner_radius=4,
            )
            row.pack(fill="x", pady=2)

            ctk.CTkLabel(row, text=pac, width=200, anchor="w",
                        text_color=self._tm.c("BLACK")).pack(side="left", padx=6)

            ctk.CTkLabel(row, text=fisio, width=180, anchor="w",
                        text_color=self._tm.c("GRAY_DARK")).pack(side="left")

            ctk.CTkLabel(row, text=data, width=100, anchor="w",
                        text_color=self._tm.c("GRAY_DARK")).pack(side="left")

            ctk.CTkLabel(row, text=hora, width=70, anchor="w",
                        text_color=self._tm.c("GRAY_DARK")).pack(side="left")

            sbg, stc = _STATUS_THEME_MAP.get(
                status,
                ("GRAY_LIGHT", "GRAY_DARK")
            )

            ctk.CTkLabel(
                row,
                text=status,
                width=110,
                fg_color=self._tm.c(sbg),
                text_color=self._tm.c(stc),
                corner_radius=12,
                font=(self._tm.font, 11, "bold"),
            ).pack(side="left", padx=4)

            # ações
            actions = ctk.CTkFrame(row, fg_color="transparent")
            actions.pack(side="right", padx=6)

            ctk.CTkButton(
                actions,
                text="✔",
                width=32,
                height=28,
                fg_color=self._tm.c("SUCCESS_BG"),
                text_color=self._tm.c("SUCCESS"),
                command=lambda i=cid: self._emit("confirm", i),
            ).pack(side="left", padx=2)

            ctk.CTkButton(
                actions,
                text="✘",
                width=32,
                height=28,
                fg_color=self._tm.c("RED_LIGHT"),
                text_color=self._tm.c("RED"),
                command=lambda i=cid: self._emit("cancel", i),
            ).pack(side="left", padx=2)

            ctk.CTkButton(
                actions,
                text="🗑",
                width=32,
                height=28,
                fg_color=self._tm.c("GRAY_LIGHT"),
                text_color=self._tm.c("GRAY_DARK"),
                command=lambda i=cid, n=pac: self._emit("delete", i, n),
            ).pack(side="left", padx=2)

    def _emit(self, action, *args):
        if action == "confirm" and self._on_confirm:
            self._on_confirm(*args)
        elif action == "cancel" and self._on_cancel:
            self._on_cancel(*args)
        elif action == "delete" and self._on_delete:
            self._on_delete(*args)

    def update_data(self, data: list):
        self._data = data or []
        self._render_rows()