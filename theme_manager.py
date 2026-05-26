import json
import os
import customtkinter as ctk

_PREFS_FILE = "theme_prefs.json"

def _load_dark_pref() -> bool:
    try:
        with open(_PREFS_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("dark_mode", False)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return False

def _save_dark_pref(dark: bool) -> None:
    try:
        with open(_PREFS_FILE, "w", encoding="utf-8") as f:
            json.dump({"dark_mode": dark}, f)
    except OSError:
        pass

LIGHT = {
    "GRAY_BG":      "#F4F6FA",
    "WHITE":        "#FFFFFF",
    "BLACK":        "#1A1D2E",
    "DARK_BLUE":    "#1A3C5E",
    "BLUE":         "#2563EB",
    "BLUE_XL":      "#EFF6FF",
    "GRAY":         "#94A3B8",
    "GRAY_DARK":    "#475569",
    "GRAY_LIGHT":   "#E2E8F0",
    "SUCCESS":      "#16A34A",
    "SUCCESS_BG":   "#DCFCE7",
    "WARN":         "#D97706",
    "WARN_BG":      "#FEF3C7",
    "RED":          "#DC2626",
    "RED_LIGHT":    "#FEE2E2",
    "PURPLE":       "#7C3AED",
    "PURPLE_BG":    "#EDE9FE",
    "PANEL_BG":     "#FFFFFF",
    "BORDER":       "#E2E8F0",
    "TOPBAR_BG":    "#2563EB",
    "TOPBAR_TEXT":  "#FFFFFF",
    "TOPBAR_MUTED": "#AAAAAA",
}

DARK = {
    "GRAY_BG":      "#0F1117",
    "WHITE":        "#1E2130",
    "BLACK":        "#F1F5F9",
    "DARK_BLUE":    "#93C5FD",
    "BLUE":         "#3B82F6",
    "BLUE_XL":      "#1E2A3A",
    "GRAY":         "#64748B",
    "GRAY_DARK":    "#94A3B8",
    "GRAY_LIGHT":   "#2D3748",
    "SUCCESS":      "#4ADE80",
    "SUCCESS_BG":   "#14532D",
    "WARN":         "#FCD34D",
    "WARN_BG":      "#451A03",
    "RED":          "#F87171",
    "RED_LIGHT":    "#450A0A",
    "PURPLE":       "#A78BFA",
    "PURPLE_BG":    "#2E1065",
    "PANEL_BG":     "#1E2130",
    "BORDER":       "#2D3748",
    "TOPBAR_BG":    "#141824",
    "TOPBAR_TEXT":  "#F1F5F9",
    "TOPBAR_MUTED": "#94A3B8",
}

class ThemeManager:
    _instance = None

    def __init__(self):
        self._dark_mode = _load_dark_pref()
        self._observers: list = []
        ctk.set_appearance_mode("dark" if self._dark_mode else "light")

    @classmethod
    def get(cls) -> "ThemeManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @property
    def is_dark(self) -> bool:
        return self._dark_mode

    @property
    def colors(self) -> dict:
        return DARK if self._dark_mode else LIGHT
    
    @property
    def font(self):
        return "Segoe UI"

    def c(self, key: str) -> str:
        return self.colors[key]

    def toggle(self):
        self._dark_mode = not self._dark_mode
        _save_dark_pref(self._dark_mode)
        ctk.set_appearance_mode("dark" if self._dark_mode else "light")
        self._notify()

    def set_dark(self, value: bool):
        if self._dark_mode != value:
            self.toggle()

    def subscribe(self, callback):
        if callback not in self._observers:
            self._observers.append(callback)

    def unsubscribe(self, callback):
        self._observers = [o for o in self._observers if o != callback]

    def _notify(self):
        colors = self.colors
        for cb in list(self._observers):
            try:
                cb(colors)
            except Exception:
                pass