import os
import sys

APP_NAME = "Prontuario"
APP_VERSION = "1.0"

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
    EXECUTABLE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    EXECUTABLE_DIR = BASE_DIR

DB_PATH = os.path.join(EXECUTABLE_DIR, "prontuario.db")
THEME_PREFS = os.path.join(EXECUTABLE_DIR, "theme_prefs.json")