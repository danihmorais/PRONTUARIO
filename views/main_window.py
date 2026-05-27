import os
import sqlite3
from datetime import datetime
from typing import List

import customtkinter as ctk
from PIL import Image

import views.search_pacient_window as spw
import views.search_doctor_window  as sdw
from views.form_window        import FormWindow
from views.appointment_window import AppointmentWindow
from views.record_window      import RecordWindow
from views.export_window      import ExportView
from views.config_window      import ConfigView
from views.components.theme_switch import ThemeSwitch

from config        import BASE_DIR, DB_PATH
from theme_manager import ThemeManager

def _load_icon(path: str, size=(18, 18)) -> ctk.CTkImage | None:
    try:
        with Image.open(path) as img:
            return ctk.CTkImage(
                light_image=img.copy(),
                dark_image=img.copy(),
                size=size,
            )
    except Exception:
        return None

_STATUS_THEME_MAP = {
    "Confirmada": ("SUCCESS_BG", "SUCCESS"),
    "Pendente":   ("WARN_BG", "WARN"),
    "Cancelada":  ("RED_LIGHT", "RED"),
    "Realizada":  ("PURPLE_BG", "PURPLE"),
}

class MainWindow(ctk.CTk):

    def __init__(self, controller):
        super().__init__()

        self._tm: ThemeManager     = ThemeManager.get()
        self._themed_widgets: List[dict] = []
        self.controller            = controller
        self._current_view: str    = ""

        try:
            self.iconbitmap(os.path.join(BASE_DIR, "assets", "icon.ico"))
        except Exception:
            pass
        self.title("Prontuário — Dashboard")
        self.configure(fg_color=self._tm.c("GRAY_BG"))
        self.minsize(1280, 720)
        self.after(10, self._maximize)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self._build_sidebar()
        self._build_topbar()
        self._build_content_area()

        self._tm.subscribe(self._on_theme_change)

        self.show_view("dashboard")

        self.protocol("WM_DELETE_WINDOW", self._close_window)

    def _build_content_area(self):
        self._content = ctk.CTkFrame(self, fg_color="transparent")
        self._content.grid(row=1, column=1, sticky="nsew", padx=24, pady=24)
        self._content.grid_columnconfigure(0, weight=1)
        self._content.grid_rowconfigure(0, weight=1)

        self._views: dict[str, ctk.CTkFrame] = {
            "dashboard":      self._build_dashboard(),
            "form":           FormWindow(self._content, self.controller),
            "appointment":    AppointmentWindow(self._content, self.controller),
            "record":         RecordWindow(self._content, self.controller),
            "search_pacient": spw.SearchPacientView(self._content),
            "search_doctor":  sdw.SearchDoctorView(self._content),
            "export":         ExportView(self._content),
            "config":         ConfigView(self._content),
        }

        for view in self._views.values():
            view.grid(row=0, column=0, sticky="nsew")

    def _build_sidebar(self):
        self._sidebar = ctk.CTkFrame(
            self, width=224,
            fg_color=self._tm.c("WHITE"),
            border_color=self._tm.c("GRAY_LIGHT"),
            border_width=1,
            corner_radius=0,
        )
        self._sidebar.grid(row=0, column=0, rowspan=2, sticky="ns")
        self._sidebar.grid_propagate(False)
        self._tw(self._sidebar, fg_color="WHITE", border_color="GRAY_LIGHT")

        logo_fr = ctk.CTkFrame(self._sidebar, fg_color=self._tm.c("WHITE"), corner_radius=0)
        logo_fr.pack(fill="x", padx=18, pady=(20, 16))
        self._tw(logo_fr, fg_color="WHITE")

        self._logo_box = ctk.CTkFrame(
            logo_fr, width=32, height=32,
            fg_color=self._tm.c("BLUE"), corner_radius=8,
        )
        self._logo_box.pack(side="left")
        self._logo_box.pack_propagate(False)
        self._tw(self._logo_box, fg_color="BLUE")

        try:
            logo_img = _load_icon(
                os.path.join(BASE_DIR, "assets", "logo.png"), size=(20, 20)
            )
            if logo_img:
                ctk.CTkLabel(self._logo_box, image=logo_img, text="").place(
                    relx=0.5, rely=0.5, anchor="center"
                )
        except Exception:
            pass

        self._lbl_title = ctk.CTkLabel(
            logo_fr, text="PRONTUÁRIO",
            font=(self._tm.font, 13, "bold"),
            text_color=self._tm.c("BLACK"),
            fg_color="transparent",
        )
        self._lbl_title.pack(side="left", padx=(10, 0))
        self._tw(self._lbl_title, text_color="BLACK")

        div = ctk.CTkFrame(self._sidebar, height=1, fg_color=self._tm.c("GRAY_LIGHT"))
        div.pack(fill="x")
        self._tw(div, fg_color="GRAY_LIGHT")

        self._nav_section("PRINCIPAL")
        self._bt_dashboard     = self._nav_btn("  Dashboard",       "graph.png",           "dashboard")
        self._bt_consultas     = self._nav_btn("  Consultas",        "calendar-search.png", "appointment")
        self._bt_prontuario    = self._nav_btn("  Prontuário",       "clipboard.png",       "record")
        self._bt_cadastro      = self._nav_btn("  Cadastros",        "personalcard.png",    "form")
        self._bt_pacientes     = self._nav_btn("  Pacientes",        "people.png",          "search_pacient")
        self._bt_fisioterapeutas = self._nav_btn("  Equipe",         "personalcard.png",    "search_doctor")

        div2 = ctk.CTkFrame(self._sidebar, height=1, fg_color=self._tm.c("GRAY_LIGHT"))
        div2.pack(fill="x", padx=16, pady=(8, 0))
        self._tw(div2, fg_color="GRAY_LIGHT")

        self._nav_section("SISTEMA")
        self._bt_exportar = self._nav_btn("  Exportar dados",   "document.png",  "export")
        self._bt_config   = self._nav_btn("  Configurações",    "setting.png",   "config")

        self._nav_btns: dict[str, ctk.CTkButton] = {
            "dashboard":      self._bt_dashboard,
            "appointment":    self._bt_consultas,
            "record":         self._bt_prontuario,
            "form":           self._bt_cadastro,
            "search_pacient": self._bt_pacientes,
            "search_doctor":  self._bt_fisioterapeutas,
            "export":         self._bt_exportar,
            "config":         self._bt_config,
        }

        footer = ctk.CTkFrame(self._sidebar, fg_color=self._tm.c("WHITE"), corner_radius=0)
        footer.pack(side="bottom", fill="x", padx=12, pady=12)
        self._tw(footer, fg_color="WHITE")

        self._bt_logout = ctk.CTkButton(
            footer, text="  Sair",
            text_color=self._tm.c("RED"),
            font=(self._tm.font, 12),
            width=196, height=34,
            fg_color=self._tm.c("WHITE"),
            hover_color=self._tm.c("RED_LIGHT"),
            border_color=self._tm.c("GRAY_LIGHT"),
            border_width=1,
            corner_radius=8,
            anchor="w",
            command=self._logout,
        )
        self._bt_logout.pack(fill="x")
        self._tw(self._bt_logout,
                 text_color="RED", fg_color="WHITE",
                 hover_color="RED_LIGHT", border_color="GRAY_LIGHT")

    def _nav_section(self, label: str):
        lbl = ctk.CTkLabel(
            self._sidebar, text=label,
            text_color=self._tm.c("GRAY"),
            font=(self._tm.font, 10, "bold"),
        )
        lbl.pack(anchor="w", padx=20, pady=(12, 4))
        self._tw(lbl, text_color="GRAY")

    def _nav_btn(self, text: str, icon_file: str, view_key: str) -> ctk.CTkButton:
        icon = _load_icon(os.path.join(BASE_DIR, "assets", "icons", icon_file))
        btn = ctk.CTkButton(
            self._sidebar,
            image=icon, compound="left",
            text=text,
            text_color=self._tm.c("GRAY_DARK"),
            font=(self._tm.font, 13),
            width=196, height=38,
            fg_color=self._tm.c("WHITE"),
            hover_color=self._tm.c("BLUE_XL"),
            corner_radius=8,
            anchor="w",
            command=lambda k=view_key: self.show_view(k),
        )
        if icon:
            btn.image = icon
        btn.pack(fill="x", padx=12, pady=2)
        return btn

    def _build_topbar(self):
        self._topbar = ctk.CTkFrame(
            self, height=56,
            fg_color=self._tm.c("TOPBAR_BG"),
            corner_radius=0,
        )
        self._topbar.grid(row=0, column=1, sticky="ew")
        self._tw(self._topbar, fg_color="TOPBAR_BG")
        self._topbar.grid_columnconfigure(0, weight=1)

        breadcrumb = ctk.CTkFrame(self._topbar, fg_color="transparent")
        breadcrumb.grid(row=0, column=0, sticky="w", padx=24, pady=14)

        lbl_inicio = ctk.CTkLabel(
            breadcrumb, text="Início /",
            text_color=self._tm.c("TOPBAR_MUTED"),
            font=(self._tm.font, 13),
        )
        lbl_inicio.pack(side="left")
        self._tw(lbl_inicio, text_color="TOPBAR_MUTED")

        self._lbl_breadcrumb = ctk.CTkLabel(
            breadcrumb, text=" Dashboard",
            text_color=self._tm.c("TOPBAR_TEXT"),
            font=(self._tm.font, 14, "bold"),
        )
        self._lbl_breadcrumb.pack(side="left")
        self._tw(self._lbl_breadcrumb, text_color="TOPBAR_TEXT")

        self._theme_switch = ThemeSwitch(self._topbar)
        self._theme_switch.grid(row=0, column=1, sticky="e", padx=16, pady=8)

    _BREADCRUMBS = {
        "dashboard":      " Dashboard",
        "form":           " Cadastros",
        "appointment":    " Consultas",
        "record":         " Prontuário",
        "search_pacient": " Pacientes",
        "search_doctor":  " Equipe",
        "export":         " Exportar Dados",
        "config":         " Configurações",
    }

    def show_view(self, view_key: str):
        for key, btn in self._nav_btns.items():
            self._set_btn_active(btn, active=(key == view_key))

        self._lbl_breadcrumb.configure(
            text=self._BREADCRUMBS.get(view_key, "")
        )

        if view_key == "dashboard":
            self._views["dashboard"].destroy()
            
            self._themed_widgets = [entry for entry in self._themed_widgets if entry["widget"].winfo_exists()]
            
            self._views["dashboard"] = self._build_dashboard()
            self._views["dashboard"].grid(row=0, column=0, sticky="nsew")

        self._views[view_key].tkraise()
        self._current_view = view_key

    def _set_btn_active(self, btn: ctk.CTkButton, active: bool):
        if active:
            btn.configure(
                fg_color=self._tm.c("BLUE"),
                text_color=self._tm.c("TOPBAR_TEXT"),
                hover_color=self._tm.c("DARK_BLUE"),
            )
        else:
            btn.configure(
                fg_color=self._tm.c("WHITE"),
                text_color=self._tm.c("GRAY_DARK"),
                hover_color=self._tm.c("BLUE_XL"),
            )

    def _build_dashboard(self) -> ctk.CTkFrame:
        totais = {"consultas": 0, "pacientes": 0, "fisios": 0, "funcionarios": 0}
        consultas_proximas: list = []
        pacientes_recentes: list = []
        consultas_hoje: list = []

        try:
            conn = sqlite3.connect(DB_PATH)
            cur  = conn.cursor()

            cur.execute("SELECT COUNT(*) FROM consultas")
            totais["consultas"] = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM pacientes")
            totais["pacientes"] = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM fisioterapeutas")
            totais["fisios"] = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM funcionarios")
            totais["funcionarios"] = cur.fetchone()[0]

            cur.execute("""
                SELECT p.nome, f.nome, c.data_consulta, c.horario, c.status
                FROM consultas c
                JOIN pacientes p       ON c.id_paciente       = p.id
                JOIN fisioterapeutas f ON c.id_fisioterapeuta = f.id
                WHERE c.status NOT IN ('Cancelada')
                ORDER BY c.data_consulta ASC, c.horario ASC
                LIMIT 8
            """)
            consultas_proximas = cur.fetchall()

            cur.execute("""
                SELECT nome FROM pacientes ORDER BY id DESC LIMIT 5
            """)
            pacientes_recentes = cur.fetchall()

            hoje = datetime.now().strftime("%d/%m/%Y")
            cur.execute("""
                SELECT COUNT(*) FROM consultas
                WHERE data_consulta = ? AND status NOT IN ('Cancelada')
            """, (hoje,))
            consultas_hoje_n = cur.fetchone()[0]

            conn.close()
        except Exception:
            consultas_hoje_n = 0

        dash = ctk.CTkFrame(self._content, fg_color="transparent")

        hdr = ctk.CTkFrame(dash, fg_color="transparent")
        hdr.pack(fill="x")

        lbl_titulo = ctk.CTkLabel(
            hdr, text="Visão Geral",
            text_color=self._tm.c("BLACK"),
            font=(self._tm.font, 24, "bold"),
        )
        lbl_titulo.pack(anchor="w")
        self._tw(lbl_titulo, text_color="BLACK")

        lbl_data = ctk.CTkLabel(
            hdr,
            text=datetime.now().strftime("%A, %d de %B de %Y").capitalize(),
            text_color=self._tm.c("GRAY"),
            font=(self._tm.font, 13),
        )
        lbl_data.pack(anchor="w", pady=(4, 0))
        self._tw(lbl_data, text_color="GRAY")

        cards_fr = ctk.CTkFrame(dash, fg_color="transparent")
        cards_fr.pack(fill="x", pady=(20, 16))
        for i in range(4):
            cards_fr.grid_columnconfigure(i, weight=1)

        card_specs = [
            ("Consultas Totais",  str(totais["consultas"]),     "BLUE",    "📋"),
            ("Pacientes",         str(totais["pacientes"]),     "SUCCESS", "👤"),
            ("Fisioterapeutas",   str(totais["fisios"]),        "PURPLE",  "🩺"),
            ("Hoje",              str(consultas_hoje_n),        "WARN",    "📅"),
        ]

        for i, (label, valor, accent, emoji) in enumerate(card_specs):
            card = ctk.CTkFrame(
                cards_fr,
                fg_color=self._tm.c("WHITE"),
                corner_radius=12,
                border_width=1,
                border_color=self._tm.c("GRAY_LIGHT"),
            )
            card.grid(
                row=0, column=i, sticky="nsew",
                padx=(0 if i == 0 else 10, 0),
            )
            self._tw(card, fg_color="WHITE", border_color="GRAY_LIGHT")

            top = ctk.CTkFrame(card, fg_color="transparent")
            top.pack(fill="x", padx=16, pady=(10, 2))

            lbl_l = ctk.CTkLabel(
                top, text=label,
                text_color=self._tm.c("GRAY"),
                font=(self._tm.font, 12),
            )
            lbl_l.pack(side="left")
            self._tw(lbl_l, text_color="GRAY")

            lbl_e = ctk.CTkLabel(top, text=emoji, font=(self._tm.font, 16))
            lbl_e.pack(side="right")

            lbl_v = ctk.CTkLabel(
                card, text=valor,
                text_color=self._tm.c("BLACK"),
                font=(self._tm.font, 32, "bold"),
            )
            lbl_v.pack(anchor="w", padx=16, pady=(0, 10))
            self._tw(lbl_v, text_color="BLACK")

        bottom = ctk.CTkFrame(dash, fg_color="transparent")
        bottom.pack(fill="both", expand=True)
        bottom.grid_columnconfigure(0, weight=3)
        bottom.grid_columnconfigure(1, weight=1)
        bottom.grid_rowconfigure(0, weight=1)

        panel_c = ctk.CTkFrame(
            bottom,
            fg_color=self._tm.c("WHITE"),
            corner_radius=12,
            border_width=1,
            border_color=self._tm.c("GRAY_LIGHT"),
        )
        panel_c.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        panel_c.grid_rowconfigure(1, weight=1)
        panel_c.grid_columnconfigure(0, weight=1)
        self._tw(panel_c, fg_color="WHITE", border_color="GRAY_LIGHT")

        ph = ctk.CTkFrame(panel_c, fg_color="transparent")
        ph.grid(row=0, column=0, sticky="ew", padx=20, pady=(16, 8))
        ph.grid_columnconfigure(0, weight=1)

        lbl_pc = ctk.CTkLabel(
            ph, text="Próximas Consultas",
            text_color=self._tm.c("BLACK"),
            font=(self._tm.font, 15, "bold"),
        )
        lbl_pc.grid(row=0, column=0, sticky="w")
        self._tw(lbl_pc, text_color="BLACK")

        btn_ver_todas = ctk.CTkButton(
            ph, text="Ver todas →",
            width=100, height=28,
            fg_color=self._tm.c("BLUE_XL"),
            hover_color=self._tm.c("GRAY_LIGHT"),
            text_color=self._tm.c("BLUE"),
            font=(self._tm.font, 12),
            command=lambda: self.show_view("appointment"),
        )
        btn_ver_todas.grid(row=0, column=1, sticky="e")
        self._tw(btn_ver_todas, fg_color="BLUE_XL", hover_color="GRAY_LIGHT", text_color="BLUE")

        col_hdr = ctk.CTkFrame(
            panel_c, fg_color=self._tm.c("BLUE_XL"), corner_radius=6
        )
        col_hdr.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 4))
        self._tw(col_hdr, fg_color="BLUE_XL")

        for txt, w in [("Paciente", 190), ("Fisioterapeuta", 160),
                       ("Data", 90), ("Hora", 70), ("Status", 110)]:
            lbl_col = ctk.CTkLabel(
                col_hdr, text=txt, width=w, anchor="w",
                font=(self._tm.font, 11, "bold"),
                text_color=self._tm.c("DARK_BLUE"),
            )
            lbl_col.pack(side="left", padx=6, pady=5)
            self._tw(lbl_col, text_color="DARK_BLUE")

        scroll_c = ctk.CTkScrollableFrame(
            panel_c,
            fg_color="transparent",
            corner_radius=0,
            height=260,
        )
        scroll_c.grid(row=2, column=0, sticky="ew", padx=(20, 6), pady=(0, 8))
        panel_c.grid_rowconfigure(2, weight=0)

        if not consultas_proximas:
            lbl_empty_c = ctk.CTkLabel(
                scroll_c,
                text="Nenhuma consulta pendente.",
                font=(self._tm.font, 13),
                text_color=self._tm.c("GRAY"),
            )
            lbl_empty_c.pack(pady=20)
            self._tw(lbl_empty_c, text_color="GRAY")
        else:
            for idx, (pac, fisio, data, hora, status) in enumerate(consultas_proximas):
                bg_key = "WHITE" if idx % 2 == 0 else "GRAY_BG"
                row = ctk.CTkFrame(scroll_c, fg_color=self._tm.c(bg_key), corner_radius=4)
                row.pack(fill="x", pady=1)
                self._tw(row, fg_color=bg_key)

                lbl_p = ctk.CTkLabel(row, text=pac, width=190, anchor="w", font=(self._tm.font, 12), text_color=self._tm.c("BLACK"))
                lbl_p.pack(side="left", padx=6)
                self._tw(lbl_p, text_color="BLACK")

                lbl_f = ctk.CTkLabel(row, text=fisio, width=160, anchor="w", font=(self._tm.font, 12), text_color=self._tm.c("GRAY_DARK"))
                lbl_f.pack(side="left")
                self._tw(lbl_f, text_color="GRAY_DARK")

                lbl_d = ctk.CTkLabel(row, text=data, width=90, anchor="w", font=(self._tm.font, 12), text_color=self._tm.c("GRAY_DARK"))
                lbl_d.pack(side="left")
                self._tw(lbl_d, text_color="GRAY_DARK")

                lbl_h = ctk.CTkLabel(row, text=hora, width=70, anchor="w", font=(self._tm.font, 12), text_color=self._tm.c("GRAY_DARK"))
                lbl_h.pack(side="left")
                self._tw(lbl_h, text_color="GRAY_DARK")

                sbg_key, stc_key = _STATUS_THEME_MAP.get(status, ("GRAY_LIGHT", "GRAY_DARK"))
                lbl_st = ctk.CTkLabel(
                    row, text=status, width=110,
                    corner_radius=12, fg_color=self._tm.c(sbg_key), text_color=self._tm.c(stc_key),
                    font=(self._tm.font, 11, "bold"),
                )
                lbl_st.pack(side="left", padx=4, pady=3)
                self._tw(lbl_st, fg_color=sbg_key, text_color=stc_key)

        panel_p = ctk.CTkFrame(
            bottom,
            fg_color=self._tm.c("WHITE"),
            corner_radius=12,
            border_width=1,
            border_color=self._tm.c("GRAY_LIGHT"),
        )
        panel_p.grid(row=0, column=1, sticky="nsew")
        self._tw(panel_p, fg_color="WHITE", border_color="GRAY_LIGHT")

        pp_hdr = ctk.CTkFrame(panel_p, fg_color="transparent")
        pp_hdr.pack(fill="x", padx=16, pady=(16, 10))
        pp_hdr.grid_columnconfigure(0, weight=1)

        lbl_pp = ctk.CTkLabel(
            pp_hdr, text="Pacientes Recentes",
            text_color=self._tm.c("BLACK"),
            font=(self._tm.font, 15, "bold"),
        )
        lbl_pp.pack(side="left")
        self._tw(lbl_pp, text_color="BLACK")

        btn_ver_todos_pac = ctk.CTkButton(
            pp_hdr, text="Ver todos →",
            width=90, height=28,
            fg_color=self._tm.c("BLUE_XL"),
            hover_color=self._tm.c("GRAY_LIGHT"),
            text_color=self._tm.c("BLUE"),
            font=(self._tm.font, 12),
            command=lambda: self.show_view("search_pacient"),
        )
        btn_ver_todos_pac.pack(side="right")
        self._tw(btn_ver_todos_pac, fg_color="BLUE_XL", hover_color="GRAY_LIGHT", text_color="BLUE")

        if not pacientes_recentes:
            lbl_empty_p = ctk.CTkLabel(
                panel_p,
                text="Nenhum paciente cadastrado.",
                font=(self._tm.font, 13),
                text_color=self._tm.c("GRAY"),
            )
            lbl_empty_p.pack(pady=20, padx=16)
            self._tw(lbl_empty_p, text_color="GRAY")
        else:
            for pac in pacientes_recentes:
                nome = pac[0]
                item = ctk.CTkFrame(panel_p, fg_color="transparent")
                item.pack(fill="x", padx=16, pady=5)

                avatar = ctk.CTkFrame(
                    item, width=36, height=36,
                    corner_radius=18,
                    fg_color=self._tm.c("BLUE"),
                )
                avatar.pack(side="left")
                avatar.pack_propagate(False)
                self._tw(avatar, fg_color="BLUE")

                initials = "".join(p[0].upper() for p in nome.split()[:2]) or "?"
                lbl_av = ctk.CTkLabel(
                    avatar, text=initials,
                    text_color=self._tm.c("WHITE"),
                    font=(self._tm.font, 11, "bold"),
                )
                lbl_av.place(relx=0.5, rely=0.5, anchor="center")
                self._tw(lbl_av, text_color="WHITE")

                lbl_nome = ctk.CTkLabel(
                    item, text=nome,
                    font=(self._tm.font, 13),
                    text_color=self._tm.c("BLACK"),
                )
                lbl_nome.pack(side="left", padx=10)
                self._tw(lbl_nome, text_color="BLACK")
        return dash

    def _tw(self, widget, **color_keys):
        self._themed_widgets.append({"widget": widget, "keys": color_keys})

    def _on_theme_change(self, colors: dict):
        self.configure(fg_color=colors["GRAY_BG"])

        try:
            self._lbl_title.configure(text_color=colors["BLACK"])
            self._logo_box.configure(fg_color=colors["BLUE"])
        except Exception:
            pass

        for key, btn in self._nav_btns.items():
            try:
                if key == self._current_view:
                    btn.configure(
                        fg_color=colors["BLUE"],
                        text_color=colors["TOPBAR_TEXT"],
                        hover_color=colors["DARK_BLUE"],
                    )
                else:
                    btn.configure(
                        fg_color=colors["WHITE"],
                        text_color=colors["GRAY_DARK"],
                        hover_color=colors["BLUE_XL"],
                    )
            except Exception:
                pass

        alive = []
        for entry in self._themed_widgets:
            w    = entry["widget"]
            keys = entry["keys"]
            try:
                if w.winfo_exists():
                    w.configure(**{param: colors[ck] for param, ck in keys.items()})
                    alive.append(entry)
            except Exception:
                pass
        self._themed_widgets = alive

    def _maximize(self):
        try:
            self.state("zoomed")
        except Exception:
            self.attributes("-fullscreen", True)

    def _close_window(self):
        self._tm.unsubscribe(self._on_theme_change)
        self.destroy()

    def _logout(self):
        self._tm.unsubscribe(self._on_theme_change)
        self.controller.realizar_logout(self)