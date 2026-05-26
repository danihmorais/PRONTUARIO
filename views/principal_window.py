import customtkinter as ctk
from PIL import Image
import layout as L
from theme_manager import ThemeManager


class PrincipalWindow(ctk.CTkToplevel):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self._themed_widgets: list[dict] = []
        self._tm = ThemeManager.get()
        self.controller = controller

        self.title("Prontuário - Dashboard")
        self.configure(fg_color=L.GRAY_BG)
        self.state("zoomed")
        self.resizable(False, False)
        self.attributes("-toolwindow", False)

        self._tm.subscribe(self._on_theme_change)

        self._build_sidebar()
        self._build_topbar()
        self._build_dashboard()

        self.protocol("WM_DELETE_WINDOW", self._close_window)

    # ───────────────────────────────
    # THEME REGISTRY
    # ───────────────────────────────
    def _tw_add(self, widget, **color_keys):
        self._themed_widgets.append({
            "widget": widget,
            "keys": color_keys
        })

    # ───────────────────────────────
    # SIDEBAR
    # ───────────────────────────────
    def _build_sidebar(self):
        sb = ctk.CTkFrame(
            self,
            width=220,
            height=768,
            fg_color=L.WHITE,
            border_color=L.GRAY_LIGHT,
            border_width=1,
            corner_radius=0
        )
        sb.place(x=0, y=0)
        sb.pack_propagate(False)
        self._tw_add(sb, fg_color="WHITE", border_color="GRAY_LIGHT")

        # LOGO
        logo_frame = ctk.CTkFrame(sb, fg_color=L.WHITE, corner_radius=0)
        logo_frame.pack(fill="x", padx=20, pady=(28, 20))
        self._tw_add(logo_frame, fg_color="WHITE")

        logo_icon = ctk.CTkFrame(
            logo_frame,
            width=32,
            height=32,
            fg_color=L.BLUE,
            corner_radius=8
        )
        logo_icon.pack(side="left")
        self._tw_add(logo_icon, fg_color="BLUE")

        img = Image.open("assets/logo.png")
        logo_img = ctk.CTkImage(light_image=img, dark_image=img, size=(20, 20))

        lbl_logo = ctk.CTkLabel(
            logo_icon,
            image=logo_img,
            text=""
        )
        lbl_logo.place(relx=0.5, rely=0.5, anchor="center")

        self.logo_img = logo_img

        # DIV
        div1 = ctk.CTkFrame(sb, height=1, fg_color=L.GRAY_LIGHT)
        div1.pack(fill="x")
        self._tw_add(div1, fg_color="GRAY_LIGHT")

        self._nav_section(sb, "PRINCIPAL")

        self.bt_dashboard = self._nav_button(sb, "  Dashboard", "assets/icons/graph.png", active=True)
        self.bt_consultas = self._nav_button(sb, "  Consultas", "assets/icons/clipboard.png",
                                             command=L._open_consulta)
        self.bt_cadastro = self._nav_button(sb, "  Cadastro", "assets/icons/personalcard.png",
                                            command=L._open_cadastro)
        self.bt_pacientes = self._nav_button(sb, "  Pacientes", "assets/icons/people.png")
        self.bt_medicos = self._nav_button(sb, "  Médicos", "assets/icons/personalcard.png")

        div2 = ctk.CTkFrame(sb, height=1, fg_color=L.GRAY_LIGHT)
        div2.pack(fill="x", padx=16, pady=(8, 0))
        self._tw_add(div2, fg_color="GRAY_LIGHT")

        self._nav_section(sb, "SISTEMA")

        self.bt_exportar = self._nav_button(sb, "  Exportar dados", "assets/icons/document.png")
        self.bt_config = self._nav_button(sb, "  Configurações", "assets/icons/setting.png")

        footer = ctk.CTkFrame(sb, fg_color=L.WHITE, corner_radius=0)
        footer.pack(side="bottom", fill="x", padx=12, pady=12)
        self._tw_add(footer, fg_color="WHITE")

        self.bt_logout = ctk.CTkButton(
            footer,
            text="  Sair",
            text_color=L.RED,
            font=(L.FONT, 12),
            width=196,
            height=34,
            fg_color=L.WHITE,
            hover_color=L.RED_LIGHT,
            border_color=L.GRAY_LIGHT,
            border_width=1,
            corner_radius=8,
            anchor="w",
            command=L._logout
        )
        self.bt_logout.pack(fill="x")
        self._tw_add(self.bt_logout,
                     text_color="RED",
                     fg_color="WHITE",
                     hover_color="RED_LIGHT",
                     border_color="GRAY_LIGHT")

    def _nav_section(self, parent, label):
        lbl = ctk.CTkLabel(
            parent,
            text=label,
            text_color=L.GRAY,
            font=(L.FONT, 10, "bold")
        )
        lbl.pack(anchor="w", padx=20, pady=(12, 4))
        self._tw_add(lbl, text_color="GRAY")

    def _nav_button(self, parent, text, icon_path=None, active=False, command=None):
        icon = None
        if icon_path:
            try:
                icon = ctk.CTkImage(Image.open(icon_path))
            except Exception:
                icon = None

        fg = self.BLUE if active else self.WHITE
        tc = self.TOPBAR_TEXT if active else self.GRAY_DARK
        hc = self.DARK_BLUE if active else self.BLUE_XL

        btn = ctk.CTkButton(
            parent,
            image=icon,
            compound="left",
            text=text,
            text_color=tc,
            font=(L.FONT, 13),
            width=196,
            height=38,
            fg_color=fg,
            hover_color=hc,
            corner_radius=8,
            anchor="w",
            command=command
        )
        btn.pack(padx=12, pady=2)

        self._tw_add(btn,
                     fg_color="BLUE" if active else "WHITE",
                     text_color="TOPBAR_TEXT" if active else "GRAY_DARK",
                     hover_color="DARK_BLUE" if active else "BLUE_XL")

        return btn

    # ───────────────────────────────
    # TOPBAR
    # ───────────────────────────────
    def _build_topbar(self):
        topbar = ctk.CTkFrame(self, height=56, fg_color=L.TOPBAR_BG, corner_radius=0)
        topbar.place(x=220, y=0, relwidth=1)
        self._tw_add(topbar, fg_color="TOPBAR_BG")

        ctk.CTkLabel(
            topbar,
            text="Início /",
            text_color=L.TOPBAR_MUTED,
            font=(L.FONT, 13)
        ).place(x=24, y=18)

        ctk.CTkLabel(
            topbar,
            text="Dashboard",
            text_color=L.TOPBAR_TEXT,
            font=(L.FONT, 14, "bold")
        ).place(x=80, y=18)

        self._theme_btn = ctk.CTkButton(
            topbar,
            text=L._theme_icon(),
            width=38,
            height=32,
            font=(L.FONT, 16),
            fg_color=L.TOPBAR_BG,
            hover_color=L.BLUE,
            text_color=L.TOPBAR_TEXT,
            corner_radius=8,
            command=L._toggle_theme
        )
        self._theme_btn.place(relx=1.0, x=-56, y=12)

    def _theme_icon(self):
        return "☀️" if self._tm.is_dark else "🌙"

    def _toggle_theme(self):
        self._tm.toggle()

    # ───────────────────────────────
    # DASHBOARD
    # ───────────────────────────────
    def _build_dashboard(self):
        x_start = 240
        y_start = 80

        ctk.CTkLabel(
            self,
            text="Visão geral",
            text_color=L.BLACK,
            font=(L.FONT, 20, "bold")
        ).place(x=x_start, y=y_start)

        ctk.CTkLabel(
            self,
            text="Bem-vindo de volta, Bruno",
            text_color=L.GRAY_DARK,
            font=(L.FONT, 13)
        ).place(x=x_start, y=y_start + 30)

    # ───────────────────────────────
    # THEME UPDATE
    # ───────────────────────────────
    def _on_theme_change(self, colors: dict):
        self.configure(fg_color=colors["GRAY_BG"])

        for entry in self._themed_widgets:
            widget = entry["widget"]
            keys = entry["keys"]
            try:
                widget.configure(**{
                    param: colors[color_key]
                    for param, color_key in keys.items()
                })
            except Exception:
                pass

        self._theme_btn.configure(
            text=L._theme_icon(),
            fg_color=colors["TOPBAR_BG"],
            hover_color=colors["BLUE"],
            text_color=colors["TOPBAR_TEXT"]
        )

    # ───────────────────────────────
    # CALLBACKS
    # ───────────────────────────────
    def _open_cadastro(self):
        self.controller.abrir_cadastro(self)

    def _open_consulta(self):
        self.controller.abrir_consulta(self)

    def _close_window(self):
        self._tm.unsubscribe(self._on_theme_change)
        self.quit()

    def _logout(self):
        self._tm.unsubscribe(self._on_theme_change)
        self.controller.realizar_logout(self)