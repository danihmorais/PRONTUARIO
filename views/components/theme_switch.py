import customtkinter as ctk
from theme_manager import ThemeManager

class ThemeSwitch(ctk.CTkButton):

    def __init__(self, parent, **kwargs):

        self._tm = ThemeManager.get()

        super().__init__(
            parent,

            text=self._icon(),

            width=42,
            height=42,

            corner_radius=12,

            font=(self._tm.font, 18),

            fg_color=self._tm.c("WHITE"),
            hover_color=self._tm.c("BLUE_XL"),

            text_color=self._tm.c("GRAY_DARK"),

            border_width=1,
            border_color=self._tm.c("GRAY_LIGHT"),

            command=self._toggle,

            **kwargs
        )

        self._tm.subscribe(self._on_theme_change)

    def _icon(self):
        return "☀️" if self._tm.is_dark else "🌙"

    def _toggle(self):
        self._tm.toggle()

    def _on_theme_change(self, colors):

        self.configure(
            text=self._icon(),

            fg_color=colors["WHITE"],
            hover_color=colors["BLUE_XL"],

            text_color=colors["GRAY_DARK"],

            border_color=colors["GRAY_LIGHT"]
        )

    def destroy(self):

        try:
            self._tm.unsubscribe(self._on_theme_change)
        except:
            pass

        super().destroy()