"""
consulta_window.py
Janela de consultas do MediSystem com suporte a modo claro/escuro.
"""

from customtkinter import *
from PIL import Image
from layout import layout
from theme_manager import ThemeManager


class ConsultaWindows(CTkToplevel, layout):

    def __init__(self, parent, controller):
        self._themed_widgets: list[dict] = []
        self._tm = ThemeManager.get()

        super().__init__(parent)
        self.controller = controller

        self.title("Consultas")
        self.geometry("1550x674+170+130")
        self.resizable(False, False)

        self._tm.subscribe(self._on_theme_change)
        self.configure(fg_color=self.GRAY_BG)

        self._build_topbar()
        self._build_tabview()
        self.agendar_consulta()

        self.protocol("WM_DELETE_WINDOW", self.fechar_consulta)

    # ── Registro ─────────────────────────────────────────────────────────────

    def _tw_add(self, widget, **color_keys):
        self._themed_widgets.append({"widget": widget, "keys": color_keys})

    # ── Helpers ──────────────────────────────────────────────────────────────

    def _label(self, parent, text, font_size=12, bold=False, **place_kwargs):
        weight = "bold" if bold else "normal"
        lbl = CTkLabel(parent, text=text, text_color=self.BLACK,
                       font=("Segoe UI", font_size, weight))
        lbl.place(**place_kwargs)
        self._tw_add(lbl, text_color="BLACK")
        return lbl

    def _entry(self, parent, width, height=32, placeholder="", **place_kwargs):
        ent = CTkEntry(
            parent, width=width, height=height,
            fg_color=self.WHITE, bg_color=self.BLUE_XL,
            corner_radius=6,
            border_color=self.GRAY_DARK, border_width=1,
            text_color=self.BLACK,
            font=("Segoe UI", 14, "normal"),
            placeholder_text=placeholder,
            placeholder_text_color=self.GRAY,
        )
        ent.place(**place_kwargs)
        self._tw_add(ent, fg_color="WHITE", bg_color="BLUE_XL",
                       border_color="GRAY_DARK", text_color="BLACK")
        return ent

    def _combo(self, parent, width, values, **place_kwargs):
        cb = CTkComboBox(
            parent, width=width, height=32,
            fg_color=self.WHITE, bg_color=self.BLUE_XL,
            corner_radius=6,
            border_color=self.GRAY_DARK, border_width=1,
            button_color=self.BLUE, button_hover_color=self.DARK_BLUE,
            dropdown_fg_color=self.WHITE,
            dropdown_hover_color=self.BLUE_XL,
            dropdown_text_color=self.BLACK,
            dropdown_font=("Segoe UI", 14, "normal"),
            text_color=self.BLACK,
            font=("Segoe UI", 14, "normal"),
            values=values,
        )
        cb.place(**place_kwargs)
        self._tw_add(cb,
                       fg_color="WHITE", bg_color="BLUE_XL",
                       border_color="GRAY_DARK", text_color="BLACK",
                       button_color="BLUE", button_hover_color="DARK_BLUE",
                       dropdown_fg_color="WHITE",
                       dropdown_hover_color="BLUE_XL",
                       dropdown_text_color="BLACK")
        return cb

    def _cal_button(self, parent, **place_kwargs):
        icon = CTkImage(Image.open("assets/icons/calendar-search.png"), size=(20, 20))
        btn = CTkButton(
            parent, width=32, height=32, text="", image=icon,
            compound="left",
            fg_color=self.BLUE, bg_color=self.BLUE_XL,
            hover_color=self.DARK_BLUE, corner_radius=6,
        )
        btn.place(**place_kwargs)
        self._tw_add(btn, fg_color="BLUE", bg_color="BLUE_XL",
                       hover_color="DARK_BLUE")
        return btn

    def _search_button(self, parent, text, **place_kwargs):
        btn = CTkButton(
            parent, width=131, height=32, text=text,
            compound="left",
            fg_color=self.BLUE, bg_color=self.BLUE_XL,
            hover_color=self.DARK_BLUE, corner_radius=6,
        )
        btn.place(**place_kwargs)
        self._tw_add(btn, fg_color="BLUE", bg_color="BLUE_XL",
                       hover_color="DARK_BLUE")
        return btn

    # ── Topbar ───────────────────────────────────────────────────────────────

    def _build_topbar(self):
        self.fr_topbar = CTkFrame(self, width=1550, height=53,
                                  fg_color=self.TOPBAR_BG, corner_radius=0)
        self.fr_topbar.place(x=0, y=0)
        self._tw_add(self.fr_topbar, fg_color="TOPBAR_BG")

        try:
            img_bg = CTkImage(Image.open("assets/bg_topbar.png"), size=(691, 52))
            lb_bg = CTkLabel(self.fr_topbar, image=img_bg, text="",
                             fg_color=self.TOPBAR_BG)
            lb_bg.place(x=858, y=0)
            self._tw_add(lb_bg, fg_color="TOPBAR_BG")
        except Exception:
            pass

        try:
            icon_user = CTkImage(Image.open("assets/icons/user.png"), size=(32, 32))
            lb_icon = CTkLabel(self.fr_topbar, image=icon_user, text="",
                               fg_color=self.TOPBAR_BG)
            lb_icon.place(x=24, y=10)
            self._tw_add(lb_icon, fg_color="TOPBAR_BG")
        except Exception:
            pass

        lbl_nome = CTkLabel(self.fr_topbar, text="Bruno Álex",
                            text_color=self.TOPBAR_TEXT,
                            font=("Segoe UI", 12, "bold"), height=12)
        lbl_nome.place(x=64, y=10)
        self._tw_add(lbl_nome, text_color="TOPBAR_TEXT", fg_color="TOPBAR_BG")

        lbl_nivel = CTkLabel(self.fr_topbar, text="Admin",
                             text_color=self.TOPBAR_TEXT,
                             font=("Segoe UI", 12, "normal"), height=12)
        lbl_nivel.place(x=64, y=28)
        self._tw_add(lbl_nivel, text_color="TOPBAR_TEXT", fg_color="TOPBAR_BG")

        # Botão de tema
        self._theme_btn = CTkButton(
            self.fr_topbar,
            text=self._theme_icon(),
            width=32, height=28,
            font=("Segoe UI", 14),
            fg_color=self.TOPBAR_BG,
            hover_color=self.BLUE,
            text_color=self.TOPBAR_TEXT,
            corner_radius=8,
            command=self._toggle_theme,
        )
        self._theme_btn.place(relx=1.0, x=-48, y=12)

    # ── TabView ──────────────────────────────────────────────────────────────

    def _build_tabview(self):
        self.tbv_consulta = CTkTabview(
            self, width=1502, height=580,
            fg_color=self.WHITE, bg_color=self.GRAY_BG,
            border_color=self.GRAY_LIGHT, border_width=1.5,
            corner_radius=8,
            text_color=self.TOPBAR_TEXT,
            segmented_button_fg_color=self.GRAY,
            segmented_button_selected_color=self.BLUE,
            segmented_button_selected_hover_color=self.DARK_BLUE,
            segmented_button_unselected_color=self.GRAY_DARK,
        )
        self.tbv_consulta.place(x=24, y=66)
        self._tw_add(self.tbv_consulta,
                       fg_color="WHITE", bg_color="GRAY_BG",
                       border_color="GRAY_LIGHT",
                       text_color="TOPBAR_TEXT",
                       segmented_button_fg_color="GRAY",
                       segmented_button_selected_color="BLUE",
                       segmented_button_selected_hover_color="DARK_BLUE",
                       segmented_button_unselected_color="GRAY_DARK")

        self.tab_agendar_consulta = self.tbv_consulta.add("Agendar Consulta")
        self.tab_buscar_consulta  = self.tbv_consulta.add("Buscar Consulta")

    # ── Aba Agendar ───────────────────────────────────────────────────────────

    def agendar_consulta(self):
        fr = CTkFrame(self.tab_agendar_consulta,
                      width=1458, height=418,
                      fg_color=self.BLUE_XL,
                      border_color=self.BLUE, border_width=1,
                      corner_radius=6)
        fr.place(x=14, y=10)
        self._tw_add(fr, fg_color="BLUE_XL", border_color="BLUE")

        # ── DADOS DO PACIENTE ─────────────────────────────────────────────
        self._label(fr, "DADOS DO PACIENTE", 14, bold=True, x=16, y=18)

        self._search_button(fr, "Buscar paciente", x=16, y=72)

        self._label(fr, "Nome completo",       x=163, y=46)
        self.ent_nome_paciente_agendamento = self._entry(fr, 342, x=163, y=72)

        self._label(fr, "Data de nascimento",  x=521, y=46)
        self.ent_nascimento_paciente_agendamento = self._entry(
            fr, 150, placeholder="dd/mm/aaaa", x=521, y=72)
        self._cal_button(fr, x=678, y=72)

        self._label(fr, "CPF",  x=730, y=46)
        self.ent_cpf_paciente_agendamento = self._entry(fr, 178, x=730, y=72)

        self._label(fr, "Sexo", x=924, y=46)
        self.cb_sexo_paciente_agendamento = self._combo(
            fr, 176,
            ["Masculino", "Feminino", "Não-binário",
             "Agênero", "Gênero fluido", "Não declarado"],
            x=924, y=72)

        self._label(fr, "E-Mail", x=1116, y=46)
        self.ent_email_paciente_agendamento = self._entry(fr, 324, x=1116, y=72)

        self._label(fr, "Celular/Telefone", x=16,  y=108)
        self._combo(fr, 228,
                    ["Celular", "Celular/WhatsApp", "Telefone"], x=16, y=134)

        self._label(fr, "Tipo de contato", x=262, y=108)
        self._combo(fr, 228,
                    ["Pessoal", "Residencial", "Comercial"], x=262, y=134)

        self._label(fr, "Número", x=508, y=108)
        self.ent_celular_paciente_agendamento = self._entry(
            fr, 200, placeholder="Ex. 7190000-0000", x=508, y=134)

        self._label(fr, "Observação", x=725, y=108)
        self.ent_obsevacao_celular_paciente_agendamento = self._entry(
            fr, 716, x=725, y=134)

        # ── DADOS DO MÉDICO ───────────────────────────────────────────────
        self._label(fr, "DADOS DO MÉDICO", 14, bold=True, x=16, y=190)

        self._search_button(fr, "Buscar médico", x=16, y=244)

        self._label(fr, "Nome do médico",   x=164, y=218)
        self.ent_nome_medico_agendamento = self._entry(fr, 434, x=164, y=244)

        self._label(fr, "Especialidade 1",  x=618, y=218)
        self.ent_especialidade1_medico_agendamento = self._entry(fr, 272, x=618, y=244)

        self._label(fr, "Especialidade 2",  x=908, y=218)
        self.ent_especialidade2_medico_agendamento = self._entry(fr, 272, x=908, y=244)

        self._label(fr, "CRM/CFM",          x=1198, y=218)
        self.ent_crm_medico_agendamento = self._entry(fr, 242, x=1198, y=244)

        # ── DADOS DA CONSULTA ─────────────────────────────────────────────
        self._label(fr, "DADOS DA CONSULTA", 14, bold=True, x=16, y=300)

        self._label(fr, "Convênio médico",   x=16,  y=328)
        self.cb_convenio_agendamento = self._combo(
            fr, 150, ["Sim", "Não"], x=16, y=354)

        self._label(fr, "Plano de saúde",    x=184, y=328)
        self.cb_plano_saude_agendamento = self._combo(
            fr, 350,
            ["Amil", "Bradesco Saúde", "SulAmérica Saúde", "Unimed",
             "Golden Cross", "Hapvida", "NotreDame Intermédica",
             "Porto Seguro Saúde", "São Francisco Saúde", "Medial Saúde", "SUS"],
            x=184, y=354)

        self._label(fr, "Data da consulta",   x=554, y=328)
        self.ent_data_consulta_agendamento = self._entry(
            fr, 170, placeholder="dd/mm/aaaa", x=554, y=354)
        self._cal_button(fr, x=732, y=354)

        self._label(fr, "Horário da consulta", x=788, y=328)
        self.ent_hora_consulta_agendamento = self._entry(
            fr, 170, placeholder="Ex. 09:30", x=788, y=354)

        self._label(fr, "Observação",          x=978, y=328)
        self.ent_observacao_convenio_agendamento = self._entry(fr, 462, x=978, y=354)

        # ── Botões de ação ────────────────────────────────────────────────
        bt_cancel = CTkButton(
            self.tbv_consulta, width=148, height=40, text="Cancelar",
            text_color=self.BLUE, font=("Segoe UI", 12, "bold"),
            fg_color=self.WHITE, hover_color=self.BLUE_XL,
            border_color=self.BLUE, border_width=1.5,
            corner_radius=8, command=self.fechar_consulta,
        )
        bt_cancel.place(x=38, y=510)
        self._tw_add(bt_cancel, text_color="BLUE", fg_color="WHITE",
                       hover_color="BLUE_XL", border_color="BLUE")

        bt_clear = CTkButton(
            self.tbv_consulta, width=148, height=40, text="Limpar",
            text_color=self.BLUE, font=("Segoe UI", 12, "bold"),
            fg_color=self.BLUE_XL, hover_color=self.GRAY_LIGHT,
            corner_radius=8,
        )
        bt_clear.place(x=1144, y=510)
        self._tw_add(bt_clear, text_color="BLUE", fg_color="BLUE_XL",
                       hover_color="GRAY_LIGHT")

        bt_save = CTkButton(
            self.tbv_consulta, width=148, height=40, text="Agendar",
            text_color=self.TOPBAR_TEXT, font=("Segoe UI", 12, "bold"),
            fg_color=self.BLUE, hover_color=self.DARK_BLUE,
            corner_radius=8,
        )
        bt_save.place(x=1312, y=510)
        self._tw_add(bt_save, text_color="TOPBAR_TEXT",
                       fg_color="BLUE", hover_color="DARK_BLUE")

    # ── Callback de tema ──────────────────────────────────────────────────────

    def _theme_icon(self) -> str:
        return "☀️" if self._tm.is_dark else "🌙"

    def _toggle_theme(self):
        self._tm.toggle()

    def _on_theme_change(self, colors: dict):
        self.configure(fg_color=colors["GRAY_BG"])

        for entry in self._themed_widgets:
            widget = entry["widget"]
            keys   = entry["keys"]
            try:
                kwargs = {param: colors[ck] for param, ck in keys.items()}
                widget.configure(**kwargs)
            except Exception as e:
                print(f"[ConsultaWindows] erro ao reconfigurar {widget}: {e}")

        self._theme_btn.configure(
            text=self._theme_icon(),
            fg_color=colors["TOPBAR_BG"],
            hover_color=colors["BLUE"],
            text_color=colors["TOPBAR_TEXT"],
        )

    # ── Fechar ────────────────────────────────────────────────────────────────

    def fechar_consulta(self):
        self._tm.unsubscribe(self._on_theme_change)
        self.destroy()