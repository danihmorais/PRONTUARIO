from customtkinter import *
from PIL import Image
from layout import *


class PrincipalWindow(CTkToplevel, layout):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.title("MediSystem")
        self.configure(fg_color=self.GRAY_BG)
        self.state("zoomed")
        self.resizable(False, False)
        self.attributes("-toolwindow", False)

        self._build_sidebar()
        self._build_topbar()
        self._build_dashboard()

        self.protocol("WM_DELETE_WINDOW", self._close_window)

    # ── Sidebar ──────────────────────────────────────────────────────────────
    def _build_sidebar(self):
        sb = CTkFrame(self, width=220, height=768,
                      fg_color=self.WHITE,
                      border_color=self.GRAY, border_width=1,
                      corner_radius=0)
        sb.place(x=0, y=0)
        sb.pack_propagate(False)

        # Logo
        logo_frame = CTkFrame(sb, fg_color=self.WHITE, corner_radius=0)
        logo_frame.pack(fill="x", padx=20, pady=(28, 20))

        logo_icon = CTkFrame(logo_frame, width=32, height=32,
                             fg_color=self.BLUE, corner_radius=8)
        logo_icon.pack(side="left")
        CTkLabel(logo_icon, text="M", text_color=self.WHITE,
                 font=(self.FONT, 16, "bold")).place(relx=0.5, rely=0.5, anchor="center")

        logo_text_frame = CTkFrame(logo_frame, fg_color=self.WHITE, corner_radius=0)
        logo_text_frame.pack(side="left", padx=(10, 0))
        CTkLabel(logo_text_frame, text="MediSystem",
                 text_color=self.DARK_BLUE, font=(self.FONT, 14, "bold")).pack(anchor="w")
        CTkLabel(logo_text_frame, text="Gestão de saúde",
                 text_color=self.GRAY, font=(self.FONT, 10)).pack(anchor="w")

        # Divisor
        CTkFrame(sb, height=1, fg_color=self.GRAY_LIGHT).pack(fill="x")

        # Seção principal
        self._nav_section(sb, "PRINCIPAL")
        self.bt_dashboard = self._nav_button(
            sb, "  Dashboard", "assets/icons/graph.png",
            active=True)
        self.bt_consultas = self._nav_button(
            sb, "  Consultas", "assets/icons/clipboard.png",
            command=self._open_consulta)
        self.bt_cadastro = self._nav_button(
            sb, "  Cadastro", "assets/icons/personalcard.png",
            command=self._open_cadastro)
        self.bt_pacientes = self._nav_button(
            sb, "  Pacientes", "assets/icons/people.png")
        self.bt_medicos = self._nav_button(
            sb, "  Médicos", "assets/icons/personalcard.png")

        # Divisor + seção sistema
        CTkFrame(sb, height=1, fg_color=self.GRAY_LIGHT,
                 corner_radius=0).pack(fill="x", padx=16, pady=(8, 0))
        self._nav_section(sb, "SISTEMA")
        self.bt_exportar = self._nav_button(
            sb, "  Exportar dados", "assets/icons/document.png")
        self.bt_config = self._nav_button(
            sb, "  Configurações", "assets/icons/setting.png")

        # Rodapé do sidebar
        footer = CTkFrame(sb, fg_color=self.WHITE, corner_radius=0)
        footer.pack(side="bottom", fill="x", padx=12, pady=12)

        CTkFrame(footer, height=1, fg_color=self.GRAY_LIGHT).pack(fill="x", pady=(0, 12))

        user_row = CTkFrame(footer, fg_color=self.BLUE_XL, corner_radius=8)
        user_row.pack(fill="x", pady=(0, 6))

        # Avatar com iniciais
        av = CTkFrame(user_row, width=34, height=34,
                      fg_color=self.BLUE, corner_radius=17)
        av.pack(side="left", padx=(8, 0), pady=8)
        CTkLabel(av, text="BA", text_color=self.WHITE,
                 font=(self.FONT, 11, "bold")).place(relx=0.5, rely=0.5, anchor="center")

        info = CTkFrame(user_row, fg_color=self.BLUE_XL, corner_radius=0)
        info.pack(side="left", padx=10, pady=8)
        CTkLabel(info, text="Bruno Álex", text_color=self.DARK_BLUE,
                 font=(self.FONT, 12, "bold")).pack(anchor="w")
        CTkLabel(info, text="Administrador", text_color=self.BLUE,
                 font=(self.FONT, 10)).pack(anchor="w")

        self.bt_logout = CTkButton(
            footer, text="  Sair", text_color=self.RED,
            font=(self.FONT, 12), width=196, height=34,
            fg_color=self.WHITE, hover_color=self.RED_LIGHT,
            border_color=self.GRAY_LIGHT, border_width=1,
            corner_radius=8, anchor="w",
            command=self._logout)
        self.bt_logout.pack(fill="x")

    def _nav_section(self, parent, label):
        CTkLabel(parent, text=label, text_color=self.GRAY,
                 font=(self.FONT, 10, "bold")).pack(anchor="w", padx=20, pady=(12, 4))

    def _nav_button(self, parent, text, icon_path=None,
                    active=False, command=None):
        icon = None
        if icon_path:
            try:
                icon = CTkImage(Image.open(icon_path))
            except Exception:
                pass

        fg   = self.BLUE      if active else self.WHITE
        tc   = self.WHITE     if active else self.GRAY_DARK
        hc   = self.DARK_BLUE if active else self.BLUE_XL

        btn = CTkButton(
            parent, image=icon, compound="left", text=text,
            text_color=tc, font=(self.FONT, 13), width=196, height=38,
            fg_color=fg, hover_color=hc,
            corner_radius=8, anchor="w", command=command)
        btn.pack(padx=12, pady=2)
        return btn

    # ── Topbar ───────────────────────────────────────────────────────────────
    def _build_topbar(self):
        topbar = CTkFrame(self, height=56, fg_color=self.BLUE, corner_radius=0)
        topbar.place(x=220, y=0, relwidth=1)

        CTkLabel(topbar, text="Início /", text_color="#FFFFFFAA",
                 font=(self.FONT, 13)).place(x=24, y=18)
        CTkLabel(topbar, text="Dashboard", text_color=self.WHITE,
                 font=(self.FONT, 14, "bold")).place(x=80, y=18)

    # ── Dashboard ─────────────────────────────────────────────────────────────
    def _build_dashboard(self):
        x_start = 240
        y_start = 80

        CTkLabel(self, text="Visão geral",
                 text_color=self.BLACK,
                 font=(self.FONT, 20, "bold")).place(x=x_start, y=y_start)
        CTkLabel(self, text="Bem-vindo de volta, Bruno",
                 text_color=self.GRAY_DARK,
                 font=(self.FONT, 13)).place(x=x_start, y=y_start + 30)

        # Cards de métricas
        cards = [
            ("Total de consultas", "200", "+12% este mês",
             self.BLUE_XL, self.DARK_BLUE, "assets/icons/clipboard-card.png"),
            ("Total de pacientes", "172", "+8 esta semana",
             self.SUCCESS_BG, self.SUCCESS, "assets/icons/people-card.png"),
            ("Total de médicos", "6", "Sem variações",
             self.PURPLE_BG, self.PURPLE, "assets/icons/user-card.png"),
            ("Funcionários", "14", "+2 este mês",
             self.WARN_BG, self.WARN, "assets/icons/personal-card.png"),
        ]

        card_w, card_h, gap = 210, 90, 14
        y_card = y_start + 70
        for i, (label, value, trend, bg, accent, icon_path) in enumerate(cards):
            cx = x_start + i * (card_w + gap)
            self._metric_card(cx, y_card, card_w, card_h,
                              label, value, trend, bg, accent, icon_path)

        # Painel principal (tabela de consultas)
        panel_y = y_card + card_h + 20
        panel_h = 390
        main_panel = CTkFrame(self, width=640, height=panel_h,
                              fg_color=self.WHITE,
                              border_color=self.GRAY, border_width=1,
                              corner_radius=10)
        main_panel.place(x=x_start, y=panel_y)

        CTkLabel(main_panel, text="Próximas consultas",
                 text_color=self.BLACK,
                 font=(self.FONT, 14, "bold")).place(x=18, y=16)
        CTkLabel(main_panel, text="Ver todas →",
                 text_color=self.BLUE,
                 font=(self.FONT, 12)).place(x=560, y=20)

        self._consulta_table(main_panel)

        # Painel lateral
        side_panel = CTkFrame(self, width=278, height=panel_h,
                               fg_color=self.WHITE,
                               border_color=self.GRAY, border_width=1,
                               corner_radius=10)
        side_panel.place(x=x_start + 640 + 14, y=panel_y)

        CTkLabel(side_panel, text="Pacientes recentes",
                 text_color=self.BLACK,
                 font=(self.FONT, 14, "bold")).place(x=16, y=16)

    def _metric_card(self, x, y, w, h, label, value, trend,
                     bg, accent, icon_path):
        card = CTkFrame(self, width=w, height=h,
                        fg_color=self.WHITE,
                        border_color=self.GRAY, border_width=1,
                        corner_radius=10)
        card.place(x=x, y=y)

        # Ícone colorido
        icon_bg = CTkFrame(card, width=36, height=36,
                           fg_color=bg, corner_radius=8)
        icon_bg.place(x=w - 50, y=12)
        try:
            img = CTkImage(Image.open(icon_path), size=(20, 20))
            CTkLabel(icon_bg, image=img, text="",
                     fg_color=bg).place(relx=0.5, rely=0.5, anchor="center")
        except Exception:
            pass

        CTkLabel(card, text=label, text_color=self.GRAY,
                 font=(self.FONT, 11)).place(x=14, y=12)
        CTkLabel(card, text=value, text_color=self.BLACK,
                 font=(self.FONT, 26, "bold")).place(x=14, y=32)
        CTkLabel(card, text=trend, text_color=accent,
                 font=(self.FONT, 11)).place(x=14, y=66)

    def _consulta_table(self, parent):
        headers = ["Paciente", "Médico", "Horário", "Status"]
        col_x   = [18, 200, 340, 430]

        # Cabeçalho
        for header, cx in zip(headers, col_x):
            CTkLabel(parent, text=header, text_color=self.GRAY,
                     font=(self.FONT, 11, "bold")).place(x=cx, y=50)

        CTkFrame(parent, width=604, height=1,
                 fg_color=self.GRAY_LIGHT).place(x=18, y=70)

        rows = [
            ("Ana Paula Silva", "Dr. Ribeiro", "09:00", "Confirmada"),
            ("Carlos Mendes",   "Dra. Costa",  "10:30", "Pendente"),
            ("Joana Ferreira",  "Dr. Lima",    "11:00", "Confirmada"),
            ("Roberto Souza",   "Dra. Costa",  "14:00", "Cancelada"),
            ("Mariana Gomes",   "Dr. Ribeiro", "15:30", "Confirmada"),
        ]
        status_colors = {
            "Confirmada": (self.SUCCESS_BG, self.SUCCESS),
            "Pendente":   (self.WARN_BG,    self.WARN),
            "Cancelada":  (self.RED_LIGHT,  self.RED),
        }
        row_h = 46
        for i, (paciente, medico, hora, status) in enumerate(rows):
            row_y = 80 + i * row_h
            CTkLabel(parent, text=paciente, text_color=self.BLACK,
                     font=(self.FONT, 13)).place(x=col_x[0], y=row_y)
            CTkLabel(parent, text=medico, text_color=self.GRAY_DARK,
                     font=(self.FONT, 13)).place(x=col_x[1], y=row_y)
            CTkLabel(parent, text=hora, text_color=self.GRAY_DARK,
                     font=(self.FONT, 13)).place(x=col_x[2], y=row_y)

            s_bg, s_tc = status_colors[status]
            pill = CTkFrame(parent, width=80, height=24,
                            fg_color=s_bg, corner_radius=12)
            pill.place(x=col_x[3], y=row_y - 4)
            CTkLabel(pill, text=status, text_color=s_tc,
                     font=(self.FONT, 11, "bold"),
                     fg_color=s_bg).place(relx=0.5, rely=0.5, anchor="center")

            if i < len(rows) - 1:
                CTkFrame(parent, width=604, height=1,
                         fg_color=self.GRAY_LIGHT).place(x=18, y=row_y + 26)

    # ── Callbacks ─────────────────────────────────────────────────────────────
    def _open_cadastro(self):
        self.controller.abrir_cadastro(self)

    def _open_consulta(self):
        self.controller.abrir_consulta(self)

    def _close_window(self):
        self.quit()

    def _logout(self):
        self.controller.realizar_logout(self)