import customtkinter as ctk
from theme_manager import ThemeManager
from tkinter import Toplevel
import re

_STATUS_THEME_MAP = {
    "Confirmada": ("SUCCESS_BG", "SUCCESS"),
    "Pendente": ("WARN_BG", "WARN"),
    "Cancelada": ("RED_LIGHT", "RED"),
    "Realizada": ("PURPLE_BG", "PURPLE"),
}


class TimePopup:
    def __init__(self, master, on_select):
        self.top = Toplevel(master)
        self.top.title("Selecionar horário")
        self.top.geometry("220x140")
        self.top.resizable(False, False)

        self.on_select = on_select

        self.hour = ctk.CTkEntry(self.top, placeholder_text="HH")
        self.minute = ctk.CTkEntry(self.top, placeholder_text="MM")

        self.hour.pack(pady=10)
        self.minute.pack(pady=10)

        ctk.CTkButton(
            self.top,
            text="OK",
            command=self._confirm
        ).pack(pady=10)

    def _confirm(self):
        h = self.hour.get()
        m = self.minute.get()

        if h.isdigit() and m.isdigit():
            self.on_select(f"{int(h):02d}:{int(m):02d}")
            self.top.destroy()


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
        self._header = ctk.CTkFrame(
            self._panel,
            fg_color=self._tm.c("BLUE_XL"),
            corner_radius=6,
        )
        self._header.pack(fill="x", padx=10, pady=(10, 10))

        cols = ["Paciente", "Fisioterapeuta", "Data", "Hora", "Status", "Ações"]

        for i, txt in enumerate(cols):
            self._header.grid_columnconfigure(i, weight=1)

            ctk.CTkLabel(
                self._header,
                text=txt,
                anchor="w",
                font=(self._tm.font, 11, "bold"),
                text_color=self._tm.c("DARK_BLUE"),
            ).grid(row=0, column=i, sticky="w", padx=6, pady=6)

    def _build_body(self):
        self._scroll = ctk.CTkScrollableFrame(
            self._panel,
            fg_color="transparent",
        )
        self._scroll.pack(fill="both", expand=True, padx=6, pady=(0, 12))

        self._render_rows()

    def _only_digits_time(self, value):
        return re.sub(r"\D", "", value)[:4]

    def _format_time(self, value):
        if not value:
            return ""
        value = re.sub(r"\D", "", str(value))
        if len(value) >= 4:
            return f"{value[:2]}:{value[2:4]}"
        return value

    def _format_date(self, value):
        if not value:
            return ""
        value = str(value).replace("-", "/")
        parts = value.split("/")
        if len(parts) == 3:
            d, m, y = parts
            if len(y) == 2:
                y = "20" + y
            return f"{int(d):02d}/{int(m):02d}/{y}"
        return value

    def _open_time_picker(self, callback):
        TimePopup(self, callback)

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

            cid, pac, fisio, data, hora, status = row_data

            data = self._format_date(data)
            hora = self._format_time(hora)

            bg_key = "WHITE" if i % 2 == 0 else "GRAY_BG"

            row = ctk.CTkFrame(
                self._scroll,
                fg_color=self._tm.c(bg_key),
                corner_radius=4,
            )
            row.pack(fill="x", pady=2)

            for c in range(6):
                row.grid_columnconfigure(c, weight=1)

            ctk.CTkLabel(row, text=pac, anchor="w").grid(row=0, column=0, sticky="w", padx=6)
            ctk.CTkLabel(row, text=fisio, anchor="w").grid(row=0, column=1, sticky="w")
            ctk.CTkLabel(row, text=data, anchor="w").grid(row=0, column=2, sticky="w")

            hora_label = ctk.CTkLabel(row, text=hora, anchor="w")
            hora_label.grid(row=0, column=3, sticky="w")

            hora_label.bind(
                "<Button-1>",
                lambda e, cid=cid: self._open_time_picker(
                    lambda t: self._update_time(cid, t)
                )
            )

            sbg, stc = _STATUS_THEME_MAP.get(status, ("GRAY_LIGHT", "GRAY_DARK"))

            ctk.CTkLabel(
                row,
                text=status,
                fg_color=self._tm.c(sbg),
                text_color=self._tm.c(stc),
                corner_radius=12,
                font=(self._tm.font, 11, "bold"),
            ).grid(row=0, column=4, sticky="w", padx=4)

            actions = ctk.CTkFrame(row, fg_color="transparent")
            actions.grid(row=0, column=5, sticky="e", padx=6)

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

    def _update_time(self, cid, value):
        for i, r in enumerate(self._data):
            if r[0] == cid:
                self._data[i] = (r[0], r[1], r[2], r[3], value, r[5])
                break
        self._render_rows()

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