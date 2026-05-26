import os
from typing import List
import sqlite3
from datetime import datetime
import customtkinter as ctk
from PIL import Image
import views.search_pacient_window as spw
import views.search_doctor_window as sdw
from config import BASE_DIR
from theme_manager import ThemeManager
from views.components.theme_switch import ThemeSwitch

class MainWindow(ctk.CTk):

    def __init__(self, controller):
        super().__init__()

        self._themed_widgets: List[dict] = []
        self._tm = ThemeManager.get()
        self.controller = controller

        self.iconbitmap(os.path.join(BASE_DIR, "assets", "icon.ico"))

        self.title("Prontuário - Dashboard")
        self.configure(fg_color=self._tm.c("GRAY_BG"))

        self.minsize(1280, 720)

        self.after(10, self._maximize)

        self._tm.subscribe(self._on_theme_change)

        self._configure_layout()

        self._build_sidebar()
        self._build_topbar()
        self._build_dashboard()

        self.protocol("WM_DELETE_WINDOW", self._close_window)

    def _maximize(self):
        try:
            self.state("zoomed")
        except Exception:
            self.attributes("-fullscreen", True)

    def _configure_layout(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

    def _tw_add(self, widget, **color_keys):
        self._themed_widgets.append({
            "widget": widget,
            "keys": color_keys
        })

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            fg_color=self._tm.c("WHITE"),
            border_color=self._tm.c("GRAY_LIGHT"),
            border_width=1,
            corner_radius=0
        )

        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="ns")

        self.sidebar.grid_propagate(False)

        self._tw_add(
            self.sidebar,
            fg_color="WHITE",
            border_color="GRAY_LIGHT"
        )

        logo_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color=self._tm.c("WHITE"),
            corner_radius=0
        )

        logo_frame.pack(fill="x", padx=20, pady=(20, 20))

        self._tw_add(logo_frame, fg_color="WHITE")

        self.logo_icon = ctk.CTkFrame(
            logo_frame,
            width=32,
            height=32,
            fg_color=self._tm.c("BLUE"),
            corner_radius=8
        )

        self.logo_icon.pack(side="left")

        self.lbl_title = ctk.CTkLabel(
            logo_frame,
            text="PRONTUÁRIO",
            font=(self._tm.font, 14, "bold"),
            text_color=self._tm.c("BLACK"),
            fg_color="transparent"
        )

        self.lbl_title.pack(side="left", padx=(10, 0))

        self._tw_add(self.logo_icon, fg_color="BLUE")

        logo_path = os.path.join(BASE_DIR, "assets", "logo.png")

        with Image.open(logo_path) as img:
            logo_img = ctk.CTkImage(
                light_image=img.copy(),
                dark_image=img.copy(),
                size=(20, 20)
            )

        self.logo_img = logo_img

        lbl_logo = ctk.CTkLabel(
            self.logo_icon,
            image=self.logo_img,
            text=""
        )

        lbl_logo.place(relx=0.5, rely=0.5, anchor="center")

        div1 = ctk.CTkFrame(
            self.sidebar,
            height=1,
            fg_color=self._tm.c("GRAY_LIGHT")
        )

        div1.pack(fill="x")

        self._tw_add(div1, fg_color="GRAY_LIGHT")

        self._nav_section(self.sidebar, "PRINCIPAL")

        self.bt_dashboard = self._nav_button(
            self.sidebar,
            "  Dashboard",
            os.path.join(BASE_DIR, "assets", "icons", "graph.png"),
            active=True
        )

        self.bt_consultas = self._nav_button(
            self.sidebar,
            "  Consultas",
            os.path.join(BASE_DIR, "assets", "icons", "clipboard.png"),
            command=self._open_appointment
        )

        self.bt_cadastro = self._nav_button(
            self.sidebar,
            "  Cadastro",
            os.path.join(BASE_DIR, "assets", "icons", "personalcard.png"),
            command=self._open_form
        )

        self.bt_pacientes = self._nav_button(
            self.sidebar,
            "  Pacientes",
            os.path.join(BASE_DIR, "assets", "icons", "people.png"),
            command=self._open_search_pacient
        )

        self.bt_medicos = self._nav_button(
            self.sidebar,
            "  Médicos",
            os.path.join(BASE_DIR, "assets", "icons", "personalcard.png"),
            command=self._open_search_doctor
        )

        div2 = ctk.CTkFrame(
            self.sidebar,
            height=1,
            fg_color=self._tm.c("GRAY_LIGHT")
        )

        div2.pack(fill="x", padx=16, pady=(8, 0))

        self._tw_add(div2, fg_color="GRAY_LIGHT")

        self._nav_section(self.sidebar, "SISTEMA")

        self.bt_exportar = self._nav_button(
            self.sidebar,
            "  Exportar dados",
            os.path.join(BASE_DIR, "assets", "icons", "document.png")
        )

        self.bt_config = self._nav_button(
            self.sidebar,
            "  Configurações",
            os.path.join(BASE_DIR, "assets", "icons", "setting.png")
        )

        footer = ctk.CTkFrame(
            self.sidebar,
            fg_color=self._tm.c("WHITE"),
            corner_radius=0
        )

        footer.pack(side="bottom", fill="x", padx=12, pady=12)

        self._tw_add(footer, fg_color="WHITE")

        self.bt_logout = ctk.CTkButton(
            footer,
            text="  Sair",
            text_color=self._tm.c("RED"),
            font=(self._tm.font, 12),
            width=196,
            height=34,
            fg_color=self._tm.c("WHITE"),
            hover_color=self._tm.c("RED_LIGHT"),
            border_color=self._tm.c("GRAY_LIGHT"),
            border_width=1,
            corner_radius=8,
            anchor="w",
            command=self._logout
        )

        self.bt_logout.pack(fill="x")

        self._tw_add(
            self.bt_logout,
            text_color="RED",
            fg_color="WHITE",
            hover_color="RED_LIGHT",
            border_color="GRAY_LIGHT"
        )

    def _nav_section(self, parent_widget, label):
        lbl = ctk.CTkLabel(
            parent_widget,
            text=label,
            text_color=self._tm.c("GRAY"),
            font=(self._tm.font, 10, "bold")
        )

        lbl.pack(anchor="w", padx=20, pady=(12, 4))

        self._tw_add(lbl, text_color="GRAY")

    def _load_icon(self, icon_path):
        try:
            with Image.open(icon_path) as img:
                return ctk.CTkImage(
                    light_image=img.copy(),
                    dark_image=img.copy(),
                    size=(18, 18)
                )
        except Exception as e:
            print(f"Erro ao carregar ícone '{icon_path}': {e}")
            return None

    def _nav_button(
        self,
        parent_widget,
        text,
        icon_path=None,
        active=False,
        command=None
    ):
        icon = self._load_icon(icon_path) if icon_path else None

        fg = self._tm.c("BLUE") if active else self._tm.c("WHITE")
        tc = self._tm.c("TOPBAR_TEXT") if active else self._tm.c("GRAY_DARK")
        hc = self._tm.c("DARK_BLUE") if active else self._tm.c("BLUE_XL")

        btn = ctk.CTkButton(
            parent_widget,
            image=icon,
            compound="left",
            text=text,
            text_color=tc,
            font=(self._tm.font, 13),
            width=196,
            height=38,
            fg_color=fg,
            hover_color=hc,
            corner_radius=8,
            anchor="w",
            command=command
        )

        btn.image = icon

        btn.pack(fill="x", padx=12, pady=2)

        self._tw_add(
            btn,
            fg_color="BLUE" if active else "WHITE",
            text_color="TOPBAR_TEXT" if active else "GRAY_DARK",
            hover_color="DARK_BLUE" if active else "BLUE_XL"
        )

        return btn

    def _build_topbar(self):
        self.topbar = ctk.CTkFrame(
            self,
            height=56,
            fg_color=self._tm.c("TOPBAR_BG"),
            corner_radius=0
        )

        self.topbar.grid(
            row=0,
            column=1,
            sticky="ew"
        )

        self._tw_add(self.topbar, fg_color="TOPBAR_BG")

        self.topbar.grid_columnconfigure(0, weight=1)

        breadcrumb = ctk.CTkFrame(
            self.topbar,
            fg_color="transparent"
        )

        breadcrumb.grid(
            row=0,
            column=0,
            sticky="w",
            padx=24,
            pady=14
        )

        lbl_inicio = ctk.CTkLabel(
            breadcrumb,
            text="Início /",
            text_color=self._tm.c("TOPBAR_MUTED"),
            font=(self._tm.font, 13)
        )

        lbl_inicio.pack(side="left")

        self._tw_add(lbl_inicio, text_color="TOPBAR_MUTED")

        lbl_dashboard = ctk.CTkLabel(
            breadcrumb,
            text=" Dashboard",
            text_color=self._tm.c("TOPBAR_TEXT"),
            font=(self._tm.font, 14, "bold")
        )

        lbl_dashboard.pack(side="left")

        self._tw_add(lbl_dashboard, text_color="TOPBAR_TEXT")

        self.theme_switch = ThemeSwitch(self.topbar)

        self.theme_switch.grid(
            row=0,
            column=1,
            sticky="e",
            padx=16,
            pady=8
        )

    def _build_dashboard(self):
        # =========================
        # DADOS DO BANCO
        # =========================

        total_consultas = 0
        total_pacientes = 0
        total_medicos = 0
        total_funcionarios = 0

        consultas = []
        pacientes_recentes = []

        try:
            conn = sqlite3.connect("prontuario.db")
            cursor = conn.cursor()

            # TOTAL CONSULTAS
            cursor.execute("SELECT COUNT(*) FROM consultas")
            total_consultas = cursor.fetchone()[0]

            # TOTAL PACIENTES
            cursor.execute("SELECT COUNT(*) FROM pacientes")
            total_pacientes = cursor.fetchone()[0]

            # TOTAL MEDICOS
            cursor.execute("SELECT COUNT(*) FROM medicos")
            total_medicos = cursor.fetchone()[0]

            # TOTAL FUNCIONARIOS
            cursor.execute("SELECT COUNT(*) FROM funcionarios")
            total_funcionarios = cursor.fetchone()[0]

            # PROXIMAS CONSULTAS
            cursor.execute("""
                SELECT paciente, medico, horario, status
                FROM consultas
                ORDER BY horario ASC
                LIMIT 5
            """)

            consultas = cursor.fetchall()

            # PACIENTES RECENTES
            cursor.execute("""
                SELECT nome
                FROM pacientes
                ORDER BY id DESC
                LIMIT 3
            """)

            pacientes_recentes = cursor.fetchall()

            conn.close()

        except Exception as e:
            print(f"Erro dashboard: {e}")

        # =========================
        # CONTAINER
        # =========================

        self.content = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.content.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=24,
            pady=24
        )

        self.content.grid_columnconfigure(0, weight=1)

        # =========================
        # HEADER
        # =========================

        header = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        title = ctk.CTkLabel(
            header,
            text="Visão geral",
            text_color=self._tm.c("BLACK"),
            font=(self._tm.font, 24, "bold")
        )

        title.pack(anchor="w")

        self._tw_add(title, text_color="BLACK")

        subtitle = ctk.CTkLabel(
            header,
            text=datetime.now().strftime("%d/%m/%Y"),
            text_color=self._tm.c("GRAY"),
            font=(self._tm.font, 13)
        )

        subtitle.pack(anchor="w", pady=(4, 0))

        self._tw_add(subtitle, text_color="GRAY")

        # =========================
        # CARDS
        # =========================

        cards = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        cards.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(24, 20)
        )

        for i in range(4):
            cards.grid_columnconfigure(i, weight=1)

        card_data = [
            ("Total de consultas", total_consultas),
            ("Total de pacientes", total_pacientes),
            ("Total de médicos", total_medicos),
            ("Funcionários", total_funcionarios)
        ]

        for i, (label, value) in enumerate(card_data):

            card = ctk.CTkFrame(
                cards,
                fg_color=self._tm.c("WHITE"),
                corner_radius=10,
                border_width=1,
                border_color=self._tm.c("GRAY_LIGHT")
            )

            card.grid(
                row=0,
                column=i,
                sticky="nsew",
                padx=(0 if i == 0 else 8, 8),
                ipadx=10,
                ipady=10
            )

            self._tw_add(
                card,
                fg_color="WHITE",
                border_color="GRAY_LIGHT"
            )

            lbl = ctk.CTkLabel(
                card,
                text=label,
                text_color=self._tm.c("GRAY"),
                font=(self._tm.font, 12)
            )

            lbl.pack(anchor="w", padx=16, pady=(12, 6))

            self._tw_add(lbl, text_color="GRAY")

            val = ctk.CTkLabel(
                card,
                text=str(value),
                text_color=self._tm.c("BLACK"),
                font=(self._tm.font, 28, "bold")
            )

            val.pack(anchor="w", padx=16, pady=(0, 12))

            self._tw_add(val, text_color="BLACK")

        # =========================
        # GRID INFERIOR
        # =========================

        bottom = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        bottom.grid(
            row=2,
            column=0,
            sticky="nsew"
        )

        bottom.grid_columnconfigure(0, weight=3)
        bottom.grid_columnconfigure(1, weight=1)

        # =========================
        # CONSULTAS
        # =========================

        panel_consultas = ctk.CTkFrame(
            bottom,
            fg_color=self._tm.c("WHITE"),
            corner_radius=10,
            border_width=1,
            border_color=self._tm.c("GRAY_LIGHT")
        )

        panel_consultas.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 10)
        )

        self._tw_add(
            panel_consultas,
            fg_color="WHITE",
            border_color="GRAY_LIGHT"
        )

        title_cons = ctk.CTkLabel(
            panel_consultas,
            text="Próximas consultas",
            text_color=self._tm.c("BLACK"),
            font=(self._tm.font, 16, "bold")
        )

        title_cons.pack(anchor="w", padx=20, pady=16)

        self._tw_add(title_cons, text_color="BLACK")

        for paciente, medico, horario, status in consultas:

            row = ctk.CTkFrame(
                panel_consultas,
                fg_color="transparent",
                height=42
            )

            row.pack(fill="x", padx=20, pady=2)

            ctk.CTkLabel(
                row,
                text=paciente,
                width=180,
                anchor="w",
                font=(self._tm.font, 13)
            ).pack(side="left")

            ctk.CTkLabel(
                row,
                text=medico,
                width=120,
                anchor="w",
                text_color=self._tm.c("GRAY")
            ).pack(side="left")

            ctk.CTkLabel(
                row,
                text=horario,
                width=90,
                anchor="w",
                text_color=self._tm.c("GRAY")
            ).pack(side="left")

            status_color = {
                "Confirmada": "#D1FAE5",
                "Pendente": "#FEF3C7",
                "Cancelada": "#FEE2E2"
            }.get(status, "#E5E7EB")

            txt_color = {
                "Confirmada": "#065F46",
                "Pendente": "#92400E",
                "Cancelada": "#991B1B"
            }.get(status, "#374151")

            status_lbl = ctk.CTkLabel(
                row,
                text=status,
                width=100,
                corner_radius=20,
                fg_color=status_color,
                text_color=txt_color,
                font=(self._tm.font, 11, "bold")
            )

            status_lbl.pack(side="right")

        # =========================
        # SIDEBAR DIREITA
        # =========================

        side = ctk.CTkFrame(
            bottom,
            fg_color=self._tm.c("WHITE"),
            corner_radius=10,
            border_width=1,
            border_color=self._tm.c("GRAY_LIGHT")
        )

        side.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self._tw_add(
            side,
            fg_color="WHITE",
            border_color="GRAY_LIGHT"
        )

        side_title = ctk.CTkLabel(
            side,
            text="Pacientes recentes",
            text_color=self._tm.c("BLACK"),
            font=(self._tm.font, 15, "bold")
        )

        side_title.pack(anchor="w", padx=16, pady=16)

        self._tw_add(side_title, text_color="BLACK")

        for paciente in pacientes_recentes:

            item = ctk.CTkFrame(
                side,
                fg_color="transparent"
            )

            item.pack(fill="x", padx=16, pady=6)

            avatar = ctk.CTkFrame(
                item,
                width=36,
                height=36,
                corner_radius=18,
                fg_color=self._tm.c("BLUE")
            )

            avatar.pack(side="left")

            initials = paciente[0][:2].upper()

            lbl_avatar = ctk.CTkLabel(
                avatar,
                text=initials,
                text_color="white",
                font=(self._tm.font, 11, "bold")
            )

            lbl_avatar.place(
                relx=0.5,
                rely=0.5,
                anchor="center"
            )

            name = ctk.CTkLabel(
                item,
                text=paciente[0],
                font=(self._tm.font, 13)
            )

            name.pack(side="left", padx=12)

    def _on_theme_change(self, colors: dict):
        self.configure(fg_color=colors["GRAY_BG"])
        self.lbl_title.configure(text_color=colors["BLACK"])
        self.logo_icon.configure(fg_color=colors["BLUE"])
        alive_widgets = []

        for entry in self._themed_widgets:
            widget = entry["widget"]
            keys = entry["keys"]

            try:
                if widget.winfo_exists():
                    widget.configure(**{
                        param: colors[color_key]
                        for param, color_key in keys.items()
                    })

                    alive_widgets.append(entry)

            except Exception as e:
                print(f"Erro ao aplicar tema em {widget}: {e}")

        self._themed_widgets = alive_widgets

    def _open_form(self):
        self.controller.open_form(self)

    def _open_appointment(self):
        self.controller.open_appointment(self)

    def _open_search_pacient(self):
        self.controller.open_search_pacient(self)

    def _open_search_doctor(self):
        self.controller.open_search_doctor(self)

    def _close_window(self):
        self._tm.unsubscribe(self._on_theme_change)
        self.destroy()

    def _logout(self):
        self._tm.unsubscribe(self._on_theme_change)
        self.controller.realizar_logout(self)