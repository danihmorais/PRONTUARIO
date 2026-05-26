import os
import hashlib
import customtkinter as ctk
from PIL import Image
from theme_manager import ThemeManager
from config import BASE_DIR
import sqlite3
from views.components.theme_switch import ThemeSwitch


class BaseWindow(ctk.CTkToplevel):

    def __init__(self, parent, controller, title, usuario=None):
        self._themed_widgets: list[dict] = []
        self._tm = ThemeManager.get()

        super().__init__(parent)
        self.controller = controller
        self.usuario = usuario

        self.title(title)
        self.theme_switch = ThemeSwitch(self)

        self.theme_switch.place(
            x=820,
            y=20
        )
        try:
            self.iconbitmap(os.path.join(BASE_DIR, "assets", "icon.ico"))
        except Exception:
            pass

        self._tm.subscribe(self._on_theme_change)
        self.configure(fg_color=self._tm.c("GRAY_BG"))

    def _get_image(self, *path_parts):
        try:
            return Image.open(os.path.join(BASE_DIR, *path_parts))
        except Exception:
            return Image.new("RGBA", (32, 32), (0, 0, 0, 0))

    def _tw_add(self, widget, **color_keys):
        self._themed_widgets.append({"widget": widget, "keys": color_keys})

    def _label(self, parent, text, font_size=12, bold=False, **place_kwargs):
        weight = "bold" if bold else "normal"
        lbl = ctk.CTkLabel(
            parent,
            text=text,
            text_color=self._tm.c("BLACK"),
            font=(self._tm.font, font_size, weight),
        )
        lbl.place(**place_kwargs)
        self._tw_add(lbl, text_color="BLACK")
        return lbl

    def _entry(self, parent, width, height=32, disabled=False, placeholder="", **place_kwargs):
        state = "disabled" if disabled else "normal"
        fg = self._tm.c("GRAY_LIGHT") if disabled else self._tm.c("WHITE")
        ent = ctk.CTkEntry(
            parent,
            width=width,
            height=height,
            fg_color=fg,
            bg_color=self._tm.c("BLUE_XL"),
            corner_radius=6,
            border_color=self._tm.c("GRAY_DARK"),
            border_width=1,
            text_color=self._tm.c("BLACK"),
            font=(self._tm.font, 14, "normal"),
            placeholder_text=placeholder,
            placeholder_text_color=self._tm.c("GRAY"),
            state=state,
        )
        ent.place(**place_kwargs)
        if disabled:
            self._tw_add(ent, fg_color="GRAY_LIGHT", bg_color="BLUE_XL",
                         border_color="GRAY_DARK", text_color="BLACK")
        else:
            self._tw_add(ent, fg_color="WHITE", bg_color="BLUE_XL",
                         border_color="GRAY_DARK", text_color="BLACK")
        return ent

    def _combo(self, parent, width, values, **place_kwargs):
        cb = ctk.CTkComboBox(
            parent,
            width=width,
            height=32,
            fg_color=self._tm.c("WHITE"),
            bg_color=self._tm.c("BLUE_XL"),
            corner_radius=6,
            border_color=self._tm.c("GRAY_DARK"),
            border_width=1,
            button_color=self._tm.c("BLUE"),
            button_hover_color=self._tm.c("DARK_BLUE"),
            dropdown_fg_color=self._tm.c("WHITE"),
            dropdown_hover_color=self._tm.c("BLUE_XL"),
            dropdown_text_color=self._tm.c("BLACK"),
            dropdown_font=(self._tm.font, 14, "normal"),
            text_color=self._tm.c("BLACK"),
            font=(self._tm.font, 14, "normal"),
            values=values,
        )
        cb.place(**place_kwargs)
        self._tw_add(
            cb,
            fg_color="WHITE",
            bg_color="BLUE_XL",
            border_color="GRAY_DARK",
            text_color="BLACK",
            button_color="BLUE",
            button_hover_color="DARK_BLUE",
            dropdown_fg_color="WHITE",
            dropdown_hover_color="BLUE_XL",
            dropdown_text_color="BLACK",
        )
        return cb

    def _cal_button(self, parent, command, **place_kwargs):
        icon = ctk.CTkImage(self._get_image("assets", "icons", "calendar-search.png"), size=(20, 20))
        btn = ctk.CTkButton(
            parent,
            width=32,
            height=32,
            text="",
            image=icon,
            compound="left",
            fg_color=self._tm.c("BLUE"),
            bg_color=self._tm.c("BLUE_XL"),
            hover_color=self._tm.c("DARK_BLUE"),
            corner_radius=6,
            command=command,
        )
        btn.place(**place_kwargs)
        self._tw_add(btn, fg_color="BLUE", bg_color="BLUE_XL", hover_color="DARK_BLUE")
        return btn

    def _search_button(self, parent, text, command=None, **place_kwargs):
        btn = ctk.CTkButton(
            parent,
            width=131,
            height=32,
            text=text,
            compound="left",
            fg_color=self._tm.c("BLUE"),
            bg_color=self._tm.c("BLUE_XL"),
            hover_color=self._tm.c("DARK_BLUE"),
            corner_radius=6,
            command=command,
        )
        btn.place(**place_kwargs)
        self._tw_add(btn, fg_color="BLUE", bg_color="BLUE_XL", hover_color="DARK_BLUE")
        return btn

    def _build_topbar(self, width):
        self.fr_topbar = ctk.CTkFrame(
            self,
            width=width,
            height=53,
            fg_color=self._tm.c("TOPBAR_BG"),
            corner_radius=0,
        )
        self.fr_topbar.place(x=0, y=0)
        self._tw_add(self.fr_topbar, fg_color="TOPBAR_BG")

        try:
            icon_user = ctk.CTkImage(
                self._get_image("assets", "icons", "user.png"), size=(32, 32)
            )
            lb_icon = ctk.CTkLabel(
                self.fr_topbar, image=icon_user, text="", fg_color=self._tm.c("TOPBAR_BG")
            )
            lb_icon.place(x=24, y=10)
            self._tw_add(lb_icon, fg_color="TOPBAR_BG")
        except Exception:
            pass

        nome_exibido = self.usuario["nome"] if self.usuario else "Usuário"
        nivel_exibido = self.usuario["nivel"].capitalize() if self.usuario else ""

        lbl_nome = ctk.CTkLabel(
            self.fr_topbar,
            text=nome_exibido,
            text_color=self._tm.c("TOPBAR_TEXT"),
            font=(self._tm.font, 12, "bold"),
            height=12,
        )
        lbl_nome.place(x=64, y=10)
        self._tw_add(lbl_nome, text_color="TOPBAR_TEXT", fg_color="TOPBAR_BG")

        lbl_nivel = ctk.CTkLabel(
            self.fr_topbar,
            text=nivel_exibido,
            text_color=self._tm.c("TOPBAR_TEXT"),
            font=(self._tm.font, 12, "normal"),
            height=12,
        )
        lbl_nivel.place(x=64, y=28)
        self._tw_add(lbl_nivel, text_color="TOPBAR_TEXT", fg_color="TOPBAR_BG")

    def _on_theme_change(self, colors: dict):
        self.configure(fg_color=colors["GRAY_BG"])
        for entry in self._themed_widgets:
            widget = entry["widget"]
            keys = entry["keys"]
            try:
                widget.configure(**{param: colors.get(ck) for param, ck in keys.items()})
            except Exception:
                pass
        if hasattr(self, "_theme_btn"):
            self._theme_btn.configure(
                text=self._theme_icon(),
                fg_color=colors["TOPBAR_BG"],
                hover_color=colors["BLUE"],
                text_color=colors["TOPBAR_TEXT"],
            )

    def _fechar(self):
        self._tm.unsubscribe(self._on_theme_change)
        self.destroy()

    def _maximize(self):
        try:
            self.state("zoomed")
        except Exception:
            self.attributes("-fullscreen", True)

    @staticmethod
    def _ufs():
        return [
            "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
            "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
            "RS", "RO", "RR", "SC", "SP", "SE", "TO",
        ]