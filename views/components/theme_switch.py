import os
import customtkinter as ctk
from PIL import Image

from config import BASE_DIR
from theme_manager import ThemeManager


class ThemeSwitch(ctk.CTkButton):

    def __init__(self, parent, **kwargs):

        self._tm = ThemeManager.get()

        self.sun_icon = ctk.CTkImage(
            light_image=Image.open(
                os.path.join(BASE_DIR, "assets", "icons", "sun.png")
            ),
            dark_image=Image.open(
                os.path.join(BASE_DIR, "assets", "icons", "sun.png")
            ),
            size=(35, 35)
        )

        self.moon_icon = ctk.CTkImage(
            light_image=Image.open(
                os.path.join(BASE_DIR, "assets", "icons", "moon.png")
            ),
            dark_image=Image.open(
                os.path.join(BASE_DIR, "assets", "icons", "moon.png")
            ),
            size=(35, 35)
        )

        super().__init__(
            parent,
            text="",
            image=self._icon(),
            width=42,
            height=42,
            corner_radius=12,
            fg_color=self._tm.c("WHITE"),
            hover_color=self._tm.c("BLUE_XL"),
            bg_color="transparent",
            border_width=1,
            border_color=self._tm.c("GRAY_LIGHT"),
            command=self._toggle,
            **kwargs
        )

        self._tm.subscribe(self._on_theme_change)

    def _icon(self):
        return self.sun_icon if self._tm.is_dark else self.moon_icon

    def _toggle(self):
        self._tm.toggle()

    def _on_theme_change(self, colors):

        self.configure(
            image=self._icon(),

            fg_color=colors["WHITE"],
            
            hover_color=colors["BLUE_XL"],
            
            border_color=colors["GRAY_LIGHT"]
        )

    def destroy(self):

        try:
            self._tm.unsubscribe(self._on_theme_change)
        except Exception:
            pass

        super().destroy()