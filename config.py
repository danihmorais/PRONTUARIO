import json
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

ARQUIVO_DADOS = os.path.join(EXECUTABLE_DIR, "dados_salvos.json")
ARQUIVO_SETTINGS_EXTERNO = os.path.join(EXECUTABLE_DIR, "settings.json")
ARQUIVO_SETTINGS_BUNDLED = os.path.join(BASE_DIR, "settings.json")

MODEL_OPENROUTER = "openrouter/free"
MODEL_GEMINI = "gemini-2.5-flash"

PROVEDORES_IA = {
    "openrouter": "OpenRouter",
    "gemini": "Gemini (Google)"
}

DEFAULT_PROVIDER = "gemini"

BASE_FILES = [
    "DFD - BASE.docx",
    "ETP - BASE.docx",
    "TR - BASE.docx",
]

PASTA_MODELOS = os.path.join(BASE_DIR, "modelos")

DEFAULT_OUTPUT_FOLDER_NAME = "Documentos_Gerados"

DEFAULT_SETTINGS = {
    "secretarias_default": [],
    "limites": {
        "dispensa_80k": 80000,
        "dispensa_pequeno_valor": 9635
    },
    "textos": {
        "clausula_padrao": "",
        "meepp_exclusivo": "",
        "meepp_nao_exclusivo": ""
    }
}


def deep_merge(default: dict, custom: dict) -> dict:
    result = default.copy()
    for key, value in custom.items():
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def carregar_settings() -> dict:
    arquivo_para_carregar = None

    if os.path.exists(ARQUIVO_SETTINGS_EXTERNO):
        arquivo_para_carregar = ARQUIVO_SETTINGS_EXTERNO
    elif os.path.exists(ARQUIVO_SETTINGS_BUNDLED):
        arquivo_para_carregar = ARQUIVO_SETTINGS_BUNDLED

    if not arquivo_para_carregar:
        return DEFAULT_SETTINGS.copy()

    try:
        with open(arquivo_para_carregar, "r", encoding="utf-8") as file:
            custom_settings = json.load(file)
        return deep_merge(DEFAULT_SETTINGS, custom_settings)
    except Exception:
        return DEFAULT_SETTINGS.copy()


SETTINGS = carregar_settings()
SECRETARIAS_DEFAULT = SETTINGS["secretarias_default"]
LIMITES = SETTINGS["limites"]
TEXTOS = SETTINGS["textos"]
