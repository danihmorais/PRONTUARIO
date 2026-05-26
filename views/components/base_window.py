import customtkinter as ctk
from theme_manager import ThemeManager

class BaseWindow(ctk.CTkFrame):
    def __init__(self, parent, controller, title="", geometry=None, usuario=None):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.usuario = usuario
        self._tm = ThemeManager.get()
        self._themed_widgets = []
        self._tm.subscribe(self._on_theme_change)

    def _tw_add(self, widget, **color_keys):
        self._themed_widgets.append({"widget": widget, "keys": color_keys})

    def _label(self, parent, text, size=12, bold=False, x=0, y=0):
        font_weight = "bold" if bold else "normal"
        lbl = ctk.CTkLabel(parent, text=text, font=(self._tm.font, size, font_weight), text_color=self._tm.c("BLACK"))
        lbl.place(x=x, y=y)
        self._tw_add(lbl, text_color="BLACK")
        return lbl

    def _entry(self, parent, width, placeholder="", x=0, y=0, disabled=False):
        state = "disabled" if disabled else "normal"
        ent = ctk.CTkEntry(parent, width=width, placeholder_text=placeholder, state=state, fg_color=self._tm.c("WHITE"), text_color=self._tm.c("BLACK"), border_color=self._tm.c("GRAY_LIGHT"))
        ent.place(x=x, y=y)
        self._tw_add(ent, fg_color="WHITE", text_color="BLACK", border_color="GRAY_LIGHT")
        return ent

    def _combo(self, parent, width, values, x=0, y=0):
        cb = ctk.CTkComboBox(parent, width=width, values=values, fg_color=self._tm.c("WHITE"), text_color=self._tm.c("BLACK"), border_color=self._tm.c("GRAY_LIGHT"))
        cb.place(x=x, y=y)
        self._tw_add(cb, fg_color="WHITE", text_color="BLACK", border_color="GRAY_LIGHT")
        return cb

    def _cal_button(self, parent, command, x, y):
        btn = ctk.CTkButton(parent, text="📅", width=30, command=command, fg_color=self._tm.c("BLUE"), hover_color=self._tm.c("DARK_BLUE"))
        btn.place(x=x, y=y)
        self._tw_add(btn, fg_color="BLUE", hover_color="DARK_BLUE")
        return btn

    def _ufs(self):
        return ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]

    def _fechar(self):
        pass

    def _on_theme_change(self, colors: dict):
        alive_widgets = []
        for entry in self._themed_widgets:
            widget = entry["widget"]
            keys = entry["keys"]
            try:
                if widget.winfo_exists():
                    widget.configure(**{param: colors[color_key] for param, color_key in keys.items()})
                    alive_widgets.append(entry)
            except Exception:
                pass
        self._themed_widgets = alive_widgets

    def destroy(self):
        self._tm.unsubscribe(self._on_theme_change)
        super().destroy()