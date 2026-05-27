import os
import customtkinter as ctk

from tkinter import font
from tkcalendar import Calendar
import ctypes
from config import BASE_DIR

def get_dpi_scale():
    try:
        return ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
    except Exception:
        return 1.0

class CalendarPopup:
    def __init__(self, parent, theme_manager):
        self.parent = parent
        self._tm = theme_manager

        self.top = None
        self.cal = None
        self.target = None

    def open(self, entry_target):
        self.target = entry_target

        self.top = ctk.CTkToplevel(self.parent)
        self.top.title("Calendário")
        self.top.resizable(False, False)
        self.top.transient(self.parent.winfo_toplevel())
        self.top.grab_set()
        self.top.focus_force()

        try:
            self.top.iconbitmap(
                os.path.join(BASE_DIR, "assets", "icon.ico")
            )
        except:
            pass

        self._center_window()

        colors = self._tm.colors

        self.top.configure(
            fg_color=colors["WHITE"]
        )

        cal_font = font.Font(
            family=self._tm.font,
            size=14
        )

        self.cal = Calendar(
            self.top,
            selectmode="day",
            date_pattern="dd/mm/yyyy",
            font=cal_font,
            headersfont=cal_font,
            normalfont=cal_font,
            weekendfont=cal_font
        )

        self.cal.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(10, 0)
        )

        buttons = ctk.CTkFrame(
            self.top,
            fg_color="transparent"
        )
        buttons.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ctk.CTkButton(
            buttons,
            text="Confirmar",
            height=36,
            fg_color=colors["BLUE"],
            hover_color=colors["DARK_BLUE"],
            text_color=colors["TOPBAR_TEXT"],
            font=(self._tm.font, 12, "bold"),
            command=self._confirm
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=(0, 5)
        )

        ctk.CTkButton(
            buttons,
            text="Cancelar",
            height=36,
            fg_color=colors["BLUE_XL"],
            hover_color=colors["GRAY_LIGHT"],
            text_color=colors["BLUE"],
            font=(self._tm.font, 12, "bold"),
            command=self.top.destroy
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=(5, 0)
        )

    def _confirm(self):
        if self.target:
            self.target.delete(0, "end")
            self.target.insert(0, self.cal.get_date())

        self.top.destroy()

    def _center_window(self):
        self.top.update_idletasks()

        scale = get_dpi_scale()

        width = int(380 * scale)
        height = int(280 * scale)

        screen_w = self.top.winfo_screenwidth()
        screen_h = self.top.winfo_screenheight()

        x = int(((screen_w - width)  // 2) * scale)
        y = (screen_h - height) // 2

        self.top.geometry(f"{width}x{height}+{x}+{y}")