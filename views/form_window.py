from customtkinter import *
from tkinter import END
from PIL import Image
from tkcalendar import Calendar
from theme_manager import ThemeManager


class FormWindow(CTkToplevel):

    def __init__(self, parent, controller):
        self._themed_widgets: list[dict] = []
        self._tm = ThemeManager.get()

        super().__init__(parent)
        self.controller = controller

        self.title("Cadastro")
        self.geometry("1200x700+300+130")
        self.resizable(False, False)

        self._tm.subscribe(self._on_theme_change)
        self.configure(fg_color=self._tm.c("GRAY_BG"))

        self._build_topbar()
        self._build_tabview()
        self.cadastro_paciente()
        self.cadastro_medico()

        self.protocol("WM_DELETE_WINDOW", self.fechar_cadastro)

    # ── Registro de widgets temáticos ────────────────────────────────────────

    def _tw_add(self, widget, **color_keys):
        self._themed_widgets.append({"widget": widget, "keys": color_keys})

    # ── Helpers de construção ────────────────────────────────────────────────

    def _label(self, parent, text, font_size=12, bold=False, **place_kwargs):
        """Label padrão com registro automático de tema."""
        weight = "bold" if bold else "normal"
        lbl = CTkLabel(parent, text=text, text_color=self._tm.c("BLACK"),
                       font=(self._tm.font, font_size, weight))
        lbl.place(**place_kwargs)
        self._tw_add(lbl, text_color="BLACK")
        return lbl

    def _entry(self, parent, width, height=32, disabled=False,
               placeholder="", **place_kwargs):
        """Entry padrão com registro automático de tema."""
        state = "disabled" if disabled else "normal"
        fg = self._tm.c("GRAY_LIGHT") if disabled else self._tm.c("WHITE")
        ent = CTkEntry(
            parent, width=width, height=height,
            fg_color=fg, bg_color=self._tm.c("BLUE_XL"),
            corner_radius=6,
            border_color=self._tm.c("GRAY_DARK"), border_width=1,
            text_color=self._tm.c("BLACK"),
            font=(self._tm.font, 14, "normal"),
            placeholder_text=placeholder,
            placeholder_text_color=self._tm.c("GRAY"),
            state=state,
        )
        ent.place(**place_kwargs)
        if disabled:
            self._tw_add(ent, fg_color="GRAY_LIGHT", bg_color="BLUE_XL",
                           border_color="GRAY_DARK", text_color="BLACK")
        else:
            self._tw_add(ent, fg_color="WHITE", bg_color="BLUE_XL",
                           border_color="GRAY_DARK", text_color="BLACK")
        return ent

    def _combo(self, parent, width, values, **place_kwargs):
        """ComboBox padrão com registro automático de tema."""
        cb = CTkComboBox(
            parent, width=width, height=32,
            fg_color=self._tm.c("WHITE"), bg_color=self._tm.c("BLUE_XL"),
            corner_radius=6,
            border_color=self._tm.c("GRAY_DARK"), border_width=1,
            button_color=self._tm.c("BLUE"), button_hover_color=self._tm.c("DARK_BLUE"),
            dropdown_fg_color=self._tm.c("WHITE"),
            dropdown_hover_color=self._tm.c("BLUE_XL"),
            dropdown_text_color=self._tm.c("BLACK"),
            dropdown_font=(self._tm.font, 14, "normal"),
            text_color=self._tm.c("BLACK"),
            font=(self._tm.font, 14, "normal"),
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

    def _section_frame(self, parent, width=1117, height=458):
        """Frame de seção com fundo azul claro."""
        fr = CTkFrame(parent, width=width, height=height,
                      fg_color=self._tm.c("BLUE_XL"),
                      border_color=self._tm.c("BLUE"), border_width=1,
                      corner_radius=6)
        fr.place(x=10, y=10)
        self._tw_add(fr, fg_color="BLUE_XL", border_color="BLUE")
        return fr

    def _cal_button(self, parent, command, **place_kwargs):
        icon = CTkImage(Image.open("assets/icons/calendar-search.png"), size=(20, 20))
        btn = CTkButton(
            parent, width=32, height=32, text="", image=icon,
            compound="left",
            fg_color=self._tm.c("BLUE"), bg_color=self._tm.c("BLUE_XL"),
            hover_color=self._tm.c("DARK_BLUE"), corner_radius=6,
            command=command,
        )
        btn.place(**place_kwargs)
        self._tw_add(btn, fg_color="BLUE", bg_color="BLUE_XL",
                       hover_color="DARK_BLUE")
        return btn

    def _action_buttons(self, parent, limpar_cmd, y=500):
        """Trio de botões Cancelar / Limpar / Cadastrar."""
        bt_cancel = CTkButton(
            parent, width=148, height=40, text="Cancelar",
            text_color=self._tm.c("BLUE"), font=(self._tm.font, 12, "bold"),
            fg_color=self._tm.c("WHITE"), hover_color=self._tm.c("BLUE_XL"),
            border_color=self._tm.c("BLUE"), border_width=1.5,
            corner_radius=8, command=self.fechar_cadastro,
        )
        bt_cancel.place(x=26, y=y)
        self._tw_add(bt_cancel, text_color="BLUE", fg_color="WHITE",
                       hover_color="BLUE_XL", border_color="BLUE")

        bt_clear = CTkButton(
            parent, width=148, height=40, text="Limpar",
            text_color=self._tm.c("BLUE"), font=(self._tm.font, 12, "bold"),
            fg_color=self._tm.c("BLUE_XL"), hover_color=self._tm.c("GRAY_LIGHT"),
            corner_radius=8, command=limpar_cmd,
        )
        bt_clear.place(x=792, y=y)
        self._tw_add(bt_clear, text_color="BLUE", fg_color="BLUE_XL",
                       hover_color="GRAY_LIGHT")

        bt_save = CTkButton(
            parent, width=148, height=40, text="Cadastrar",
            text_color=self._tm.c("TOPBAR_TEXT"), font=(self._tm.font, 12, "bold"),
            fg_color=self._tm.c("BLUE"), hover_color=self._tm.c("DARK_BLUE"),
            corner_radius=8,
        )
        bt_save.place(x=962, y=y)
        self._tw_add(bt_save, text_color="TOPBAR_TEXT",
                       fg_color="BLUE", hover_color="DARK_BLUE")

        return bt_cancel, bt_clear, bt_save

    # ── Topbar ───────────────────────────────────────────────────────────────

    def _build_topbar(self):
        self.fr_topbar = CTkFrame(self, width=1200, height=53,
                                  fg_color=self.TOPBAR_BG, corner_radius=0)
        self.fr_topbar.place(x=0, y=0)
        self._tw_add(self.fr_topbar, fg_color="TOPBAR_BG")

        try:
            img_bg = CTkImage(Image.open("assets/bg_topbar.png"), size=(691, 52))
            lb_bg = CTkLabel(self.fr_topbar, image=img_bg, text="",
                             fg_color=self.TOPBAR_BG)
            lb_bg.place(x=515, y=0)
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
            fg_color=self._tm.c("TOPBAR_BG"),
            hover_color=self._tm.c("BLUE"),
            text_color=self._tm.c("TOPBAR_TEXT"),
            corner_radius=8,
            command=self._toggle_theme,
        )
        self._theme_btn.place(relx=1.0, x=-48, y=12)

    # ── TabView ──────────────────────────────────────────────────────────────

    def _build_tabview(self):
        self.tbv_cadastros = CTkTabview(
            self, width=1152, height=610,
            fg_color=self._tm.c("WHITE"), bg_color=self._tm.c("GRAY_BG"),
            border_color=self._tm.c("GRAY_LIGHT"), border_width=1.5,
            corner_radius=8,
            text_color=self._tm.c("TOPBAR_TEXT"),
            segmented_button_fg_color=self._tm.c("GRAY"),
            segmented_button_selected_color=self._tm.c("BLUE"),
            segmented_button_selected_hover_color=self._tm.c("DARK_BLUE"),
            segmented_button_unselected_color=self._tm.c("GRAY_DARK"),
        )
        self.tbv_cadastros.place(x=24, y=66)
        self._tw_add(self.tbv_cadastros,
                       fg_color=self._tm.c("WHITE"), bg_color=self._tm.c("GRAY_BG"),
                       border_color=self._tm.c("GRAY_LIGHT"),
                       text_color=self._tm.c("TOPBAR_TEXT"),
                       segmented_button_fg_color=self._tm.c("GRAY"),
                       segmented_button_selected_color=self._tm.c("BLUE"),
                       segmented_button_selected_hover_color=self._tm.c("DARK_BLUE"),
                       segmented_button_unselected_color=self._tm.c("GRAY_DARK"))

        self.tab_cadastro_paciente = self.tbv_cadastros.add("Cadastro de Pacientes")
        self.tab_cadastro_medicos  = self.tbv_cadastros.add("Cadastro de Médicos")

    # ── Aba Pacientes ─────────────────────────────────────────────────────────

    def cadastro_paciente(self):
        fr = self._section_frame(self.tab_cadastro_paciente)

        # GERAL
        self._label(fr, "GERAL", 14, bold=True, x=16, y=18)
        self._label(fr, "Nome completo", x=16, y=46)
        self.ent_nome_paciente_cadastro = self._entry(fr, 381, x=16, y=72)

        self._label(fr, "Data de nascimento", x=413, y=46)
        self.ent_nascimento_paciente_cadastro = self._entry(
            fr, 214, placeholder="dd/mm/aaaa", x=413, y=72)
        self._cal_button(fr, self.pop_calendario, x=634, y=72)

        self._label(fr, "CPF", x=687, y=46)
        self.ent_cpf_paciente_cadastro = self._entry(fr, 210, x=687, y=72)

        self._label(fr, "Sexo", x=913, y=46)
        self.cb_sexo_paciente_cadastro = self._combo(
            fr, 186,
            ["Masculino", "Feminino", "Não-binário",
             "Agênero", "Gênero fluido", "Não declarado"],
            x=913, y=72)

        # ENDEREÇO
        self._label(fr, "ENDEREÇO", 14, bold=True, x=16, y=124)
        self._label(fr, "CEP", x=16, y=148)
        self.ent_cep_paciente_cadastro = self._entry(fr, 200, x=16, y=176)

        self._label(fr, "Endereço", x=232, y=148)
        self.ent_endereco_paciente_cadastro = self._entry(fr, 867, x=232, y=176)

        self._label(fr, "Bairro", x=16, y=212)
        self.ent_bairro_paciente_cadastro = self._entry(fr, 373, x=16, y=238)

        self._label(fr, "Cidade", x=405, y=212)
        self.ent_cidade_paciente_cadastro = self._entry(fr, 357, x=405, y=238)

        self._label(fr, "Estado", x=778, y=212)
        self.ent_estado_paciente_cadastro = self._entry(fr, 320, x=778, y=238)

        # CONTATOS
        self._label(fr, "CONTATOS", 14, bold=True, x=16, y=292)
        self._label(fr, "E-Mail", x=16, y=316)
        self.ent_email_paciente_cadastro = self._entry(fr, 341, x=16, y=342)

        self._label(fr, "Observação", x=373, y=316)
        self.ent_observacao_email_paciente_cadastro = self._entry(fr, 726, x=373, y=342)

        self._label(fr, "Celular/Telefone", x=16, y=380)
        self._combo(fr, 228, ["Celular", "Celular/WhatsApp", "Telefone"], x=16, y=406)

        self._label(fr, "Tipo de contato", x=262, y=380)
        self._combo(fr, 228, ["Pessoal", "Residencial", "Comercial"], x=262, y=406)

        self._label(fr, "Número", x=508, y=380)
        self.ent_celular_paciente_cadastro = self._entry(
            fr, 200, placeholder="Ex. 7190000-0000", x=508, y=406)

        self._label(fr, "Observação", x=724, y=380)
        self.ent_obsevacao_celular_paciente_cadastro = self._entry(fr, 376, x=724, y=406)

        self._action_buttons(
            self.tab_cadastro_paciente,
            limpar_cmd=self.limpar_cadastro_paciente,
        )

    # ── Aba Médicos ───────────────────────────────────────────────────────────

    def cadastro_medico(self):
        fr = self._section_frame(self.tab_cadastro_medicos)

        # GERAL
        self._label(fr, "GERAL", 14, bold=True, x=16, y=18)
        self._label(fr, "Código", x=16, y=46)
        self.ent_codigo_paciente_cadastro = self._entry(
            fr, 90, disabled=True, x=16, y=72)

        self._label(fr, "Nome completo", x=122, y=46)
        self.ent_nome_medico_cadastro = self._entry(fr, 363, x=122, y=72)

        self._label(fr, "CRM/CFM", x=501, y=46)
        self.cb_especialidade_paciente_cadastro = self._combo(
            fr, 200,
            ["Clinico", "Obstetra", "Pediatra", "Ortopedista",
             "Dermatologista", "Cardiologista", "Ginecologista"],
            x=501, y=72)

        self._label(fr, "Especialidade", x=717, y=46)
        self.cb_crm_paciente_cadastro = self._combo(
            fr, 128, ["CRM", "CFM"], x=717, y=72)

        self._label(fr, "Número", x=861, y=46)
        self.ent_numero_crm_medico_cadastro = self._entry(fr, 122, x=861, y=72)

        self._label(fr, "UF", x=999, y=46)
        self.cb_uf_crm_paciente_cadastro = self._combo(
            fr, 100, self._ufs(), x=999, y=72)

        self._label(fr, "CPF", x=16, y=110)
        self.ent_cpf_medico_cadastro = self._entry(fr, 186, x=16, y=134)

        self._label(fr, "RG", x=218, y=110)
        self.ent_rg_medico_cadastro = self._entry(fr, 186, x=218, y=134)

        self._label(fr, "Órgão", x=420, y=110)
        self.cb_orgao_rg_paciente_cadastro = self._combo(
            fr, 117, ["SSP"], x=420, y=134)

        self._label(fr, "UF", x=553, y=110)
        self.cb_uf_rg_paciente_cadastro = self._combo(
            fr, 100, self._ufs(), x=553, y=134)

        self._label(fr, "Sexo", x=669, y=110)
        self.cb_sexo_medico_cadastro = self._combo(
            fr, 162,
            ["Masculino", "Feminino", "Não-binário",
             "Agênero", "Gênero fluido", "Não declarado"],
            x=669, y=134)

        self._label(fr, "Data de nascimento", x=847, y=110)
        self.ent_nascimento_medico_cadastro = self._entry(
            fr, 210, placeholder="dd/mm/aaaa", x=847, y=134)
        self._cal_button(fr, self.pop_calendario, x=1063, y=134)

        # ENDEREÇO
        self._label(fr, "ENDEREÇO", 14, bold=True, x=16, y=186)
        self._label(fr, "CEP", x=16, y=208)
        self.ent_cep_medico_cadastro = self._entry(fr, 141, x=16, y=232)

        self._label(fr, "Endereço", x=173, y=208)
        self.ent_endereco_medico_cadastro = self._entry(fr, 352, x=173, y=232)

        self._label(fr, "Número", x=541, y=208)
        self.ent_numero_medico_cadastro = self._entry(fr, 70, x=541, y=232)

        self._label(fr, "Bairro", x=627, y=208)
        self.ent_bairro_medico_cadastro = self._entry(fr, 170, x=627, y=232)

        self._label(fr, "Cidade", x=813, y=208)
        self.ent_cidade_medico_cadastro = self._entry(fr, 177, x=813, y=232)

        self._label(fr, "Estado", x=1006, y=208)
        self.cb_estado_paciente_cadastro = self._combo(
            fr, 95, self._ufs(), x=1006, y=232)

        # CONTATOS
        self._label(fr, "CONTATOS", 14, bold=True, x=16, y=292)
        self._label(fr, "E-Mail", x=16, y=316)
        self.ent_email_medico_cadastro = self._entry(fr, 341, x=16, y=342)

        self._label(fr, "Observação", x=373, y=316)
        self.ent_observacao_email_medico_cadastro = self._entry(fr, 726, x=373, y=342)

        self._label(fr, "Celular/Telefone", x=16, y=380)
        self._combo(fr, 228, ["Celular", "Celular/WhatsApp", "Telefone"], x=16, y=406)

        self._label(fr, "Tipo de contato", x=262, y=380)
        self._combo(fr, 228, ["Pessoal", "Residencial", "Comercial"], x=262, y=406)

        self._label(fr, "Número", x=508, y=380)
        self.ent_celular_medico_cadastro = self._entry(
            fr, 200, placeholder="Ex. 7190000-0000", x=508, y=406)

        self._label(fr, "Observação", x=724, y=380)
        self.ent_obsevacao_celular_medico_cadastro = self._entry(fr, 376, x=724, y=406)

        self._action_buttons(
            self.tab_cadastro_medicos,
            limpar_cmd=self.limpar_cadastro_medico,
        )

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
                print(f"[CadastroWindow] erro ao reconfigurar {widget}: {e}")

        self._theme_btn.configure(
            text=self._theme_icon(),
            fg_color=colors["TOPBAR_BG"],
            hover_color=colors["BLUE"],
            text_color=colors["TOPBAR_TEXT"],
        )

    # ── Utilidades ────────────────────────────────────────────────────────────

    @staticmethod
    def _ufs():
        return ["AC","AL","AP","AM","BA","CE","DF","ES","GO","MA",
                "MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN",
                "RS","RO","RR","SC","SP","SE","TO"]

    # ── Limpar ────────────────────────────────────────────────────────────────

    def limpar_cadastro_paciente(self):
        for w in [
            self.ent_nome_paciente_cadastro,
            self.ent_nascimento_paciente_cadastro,
            self.ent_cpf_paciente_cadastro,
            self.ent_cep_paciente_cadastro,
            self.ent_endereco_paciente_cadastro,
            self.ent_bairro_paciente_cadastro,
            self.ent_cidade_paciente_cadastro,
            self.ent_estado_paciente_cadastro,
            self.ent_email_paciente_cadastro,
            self.ent_observacao_email_paciente_cadastro,
            self.ent_celular_paciente_cadastro,
            self.ent_obsevacao_celular_paciente_cadastro,
        ]:
            w.delete(0, END)

    def limpar_cadastro_medico(self):
        for w in [
            self.ent_nome_medico_cadastro,
            self.ent_numero_crm_medico_cadastro,
            self.ent_cpf_medico_cadastro,
            self.ent_rg_medico_cadastro,
            self.ent_nascimento_medico_cadastro,
            self.ent_cep_medico_cadastro,
            self.ent_endereco_medico_cadastro,
            self.ent_numero_medico_cadastro,
            self.ent_bairro_medico_cadastro,
            self.ent_cidade_medico_cadastro,
            self.ent_email_medico_cadastro,
            self.ent_observacao_email_medico_cadastro,
            self.ent_celular_medico_cadastro,
            self.ent_obsevacao_celular_medico_cadastro,
        ]:
            w.delete(0, END)

    # ── Calendário ────────────────────────────────────────────────────────────

    def pop_calendario(self):
        colors = self._tm.colors
        self.pop = CTkToplevel(self, fg_color=colors["WHITE"])
        self.pop.geometry("386x287+780+350")
        self.pop.title("Calendário")
        self.pop.resizable(False, False)
        self.pop.grab_set()
        self.pop.focus_force()

        self.calendario = Calendar(self.pop, selectmode="day")
        self.calendario.place(x=0, y=0, width=386, height=207)

        self.bt_confirmar = CTkButton(
            self.pop, text="Confirmar",
            text_color=colors["TOPBAR_TEXT"],
            font=(self._tm.font, 12, "bold"),
            width=167, height=36,
            fg_color=colors["BLUE"],
            hover_color=colors["DARK_BLUE"],
            command=self.get_data,
        )
        self.bt_confirmar.place(x=18, y=231)

        self.bt_cancelar_cal = CTkButton(
            self.pop, text="Cancelar",
            text_color=colors["BLUE"],
            font=(self._tm.font, 12, "bold"),
            width=167, height=36,
            fg_color=colors["BLUE_XL"],
            hover_color=colors["GRAY_LIGHT"],
            command=self.fecha_calendario,
        )
        self.bt_cancelar_cal.place(x=201, y=231)

    def get_data(self):
        self.ent_nascimento_paciente_cadastro.delete(0, END)
        self.ent_nascimento_paciente_cadastro.insert(END, self.calendario.get_date())
        self.pop.destroy()

    def fecha_calendario(self):
        self.pop.destroy()

    def fechar_cadastro(self):
        self._tm.unsubscribe(self._on_theme_change)
        self.destroy()