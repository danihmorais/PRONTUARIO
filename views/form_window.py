import customtkinter as ctk
from tkinter import END
from tkcalendar import Calendar

from views.components.base_window import BaseWindow


class FormWindow(BaseWindow):

    def __init__(self, parent, controller, usuario=None):

        super().__init__(
            parent=parent,
            controller=controller,
            title="Cadastro",
            geometry="1200x700",
            usuario=usuario,
        )

        self.transient(parent)
        self.grab_set()

        self._calendar_target = None

        self._build_tabview()

        self.cadastro_paciente()
        self.cadastro_medico()

        self.protocol("WM_DELETE_WINDOW", self._fechar)

    # ============================================================
    # TABVIEW
    # ============================================================

    def _build_tabview(self):

        self.tbv_cadastros = ctk.CTkTabview(
            self,
            fg_color=self._tm.c("WHITE"),
            bg_color=self._tm.c("GRAY_BG"),
            border_color=self._tm.c("GRAY_LIGHT"),
            border_width=1.5,
            corner_radius=8,
            segmented_button_fg_color=self._tm.c("GRAY"),
            segmented_button_selected_color=self._tm.c("BLUE"),
            segmented_button_selected_hover_color=self._tm.c("DARK_BLUE"),
            segmented_button_unselected_color=self._tm.c("GRAY_DARK"),
            segmented_button_unselected_hover_color=self._tm.c("GRAY"),
            text_color=self._tm.c("TOPBAR_TEXT"),
        )
        self.minsize(1280, 720)

        self.after(10, self._maximize)
        self.tbv_cadastros.place(x=24, y=66)

        self._tw_add(
            self.tbv_cadastros,
            fg_color="WHITE",
            bg_color="GRAY_BG",
            border_color="GRAY_LIGHT",
            segmented_button_fg_color="GRAY",
            segmented_button_selected_color="BLUE",
            segmented_button_selected_hover_color="DARK_BLUE",
            segmented_button_unselected_color="GRAY_DARK",
            segmented_button_unselected_hover_color="GRAY",
            text_color="TOPBAR_TEXT",
        )

        self.tab_cadastro_paciente = self.tbv_cadastros.add(
            "Cadastro de Pacientes"
        )

        self.tab_cadastro_medicos = self.tbv_cadastros.add(
            "Cadastro de Médicos"
        )

    # ============================================================
    # HELPERS
    # ============================================================

    def _section_frame(self, parent, width=1117, height=458):

        fr = ctk.CTkFrame(
            parent,
            width=width,
            height=height,
            fg_color=self._tm.c("BLUE_XL"),
            border_color=self._tm.c("BLUE"),
            border_width=1,
            corner_radius=6,
        )

        fr.place(x=10, y=10)

        self._tw_add(
            fr,
            fg_color="BLUE_XL",
            border_color="BLUE",
        )

        return fr

    def _action_buttons(
        self,
        parent,
        limpar_cmd,
        salvar_cmd,
        y=500,
    ):

        bt_cancel = ctk.CTkButton(
            parent,
            width=148,
            height=40,
            text="Cancelar",
            text_color=self._tm.c("BLUE"),
            font=(self._tm.font, 12, "bold"),
            fg_color=self._tm.c("WHITE"),
            hover_color=self._tm.c("BLUE_XL"),
            border_color=self._tm.c("BLUE"),
            border_width=1.5,
            corner_radius=8,
            command=self._fechar,
        )

        bt_cancel.place(x=26, y=y)

        self._tw_add(
            bt_cancel,
            text_color="BLUE",
            fg_color="WHITE",
            hover_color="BLUE_XL",
            border_color="BLUE",
        )

        bt_clear = ctk.CTkButton(
            parent,
            width=148,
            height=40,
            text="Limpar",
            text_color=self._tm.c("BLUE"),
            font=(self._tm.font, 12, "bold"),
            fg_color=self._tm.c("BLUE_XL"),
            hover_color=self._tm.c("GRAY_LIGHT"),
            corner_radius=8,
            command=limpar_cmd,
        )

        bt_clear.place(x=792, y=y)

        self._tw_add(
            bt_clear,
            text_color="BLUE",
            fg_color="BLUE_XL",
            hover_color="GRAY_LIGHT",
        )

        bt_save = ctk.CTkButton(
            parent,
            width=148,
            height=40,
            text="Cadastrar",
            text_color=self._tm.c("TOPBAR_TEXT"),
            font=(self._tm.font, 12, "bold"),
            fg_color=self._tm.c("BLUE"),
            hover_color=self._tm.c("DARK_BLUE"),
            corner_radius=8,
            command=salvar_cmd,
        )

        bt_save.place(x=962, y=y)

        self._tw_add(
            bt_save,
            text_color="TOPBAR_TEXT",
            fg_color="BLUE",
            hover_color="DARK_BLUE",
        )

        return bt_cancel, bt_clear, bt_save

    # ============================================================
    # CADASTRO PACIENTE
    # ============================================================

    def cadastro_paciente(self):

        fr = self._section_frame(self.tab_cadastro_paciente)

        self._label(fr, "GERAL", 14, bold=True, x=16, y=18)

        self._label(fr, "Nome completo", x=16, y=46)

        self.ent_nome_paciente_cadastro = self._entry(
            fr,
            381,
            x=16,
            y=72,
        )

        self._label(fr, "Data de nascimento", x=413, y=46)

        self.ent_nascimento_paciente_cadastro = self._entry(
            fr,
            214,
            placeholder="dd/mm/aaaa",
            x=413,
            y=72,
        )

        self._cal_button(
            fr,
            command=lambda: self.pop_calendario(
                self.ent_nascimento_paciente_cadastro
            ),
            x=634,
            y=72,
        )

        self._label(fr, "CPF", x=687, y=46)

        self.ent_cpf_paciente_cadastro = self._entry(
            fr,
            210,
            x=687,
            y=72,
        )

        self._label(fr, "Sexo", x=913, y=46)

        self.cb_sexo_paciente_cadastro = self._combo(
            fr,
            186,
            [
                "Masculino",
                "Feminino",
                "Não-binário",
                "Agênero",
                "Gênero fluido",
                "Não declarado",
            ],
            x=913,
            y=72,
        )

        # ========================================================

        self._label(fr, "ENDEREÇO", 14, bold=True, x=16, y=124)

        self._label(fr, "CEP", x=16, y=148)

        self.ent_cep_paciente_cadastro = self._entry(
            fr,
            200,
            x=16,
            y=176,
        )

        self._label(fr, "Endereço", x=232, y=148)

        self.ent_endereco_paciente_cadastro = self._entry(
            fr,
            867,
            x=232,
            y=176,
        )

        self._label(fr, "Bairro", x=16, y=212)

        self.ent_bairro_paciente_cadastro = self._entry(
            fr,
            373,
            x=16,
            y=238,
        )

        self._label(fr, "Cidade", x=405, y=212)

        self.ent_cidade_paciente_cadastro = self._entry(
            fr,
            357,
            x=405,
            y=238,
        )

        self._label(fr, "Estado", x=778, y=212)

        self.cb_estado_paciente_cadastro = self._combo(
            fr,
            320,
            self._ufs(),
            x=778,
            y=238,
        )

        # ========================================================

        self._label(fr, "CONTATOS", 14, bold=True, x=16, y=292)

        self._label(fr, "E-Mail", x=16, y=316)

        self.ent_email_paciente_cadastro = self._entry(
            fr,
            341,
            x=16,
            y=342,
        )

        self._label(fr, "Observação", x=373, y=316)

        self.ent_observacao_email_paciente_cadastro = self._entry(
            fr,
            726,
            x=373,
            y=342,
        )

        self._label(fr, "Celular/Telefone", x=16, y=380)

        self.cb_tipo_numero_paciente = self._combo(
            fr,
            228,
            [
                "Celular",
                "Celular/WhatsApp",
                "Telefone",
            ],
            x=16,
            y=406,
        )

        self._label(fr, "Tipo de contato", x=262, y=380)

        self.cb_tipo_contato_paciente = self._combo(
            fr,
            228,
            [
                "Pessoal",
                "Residencial",
                "Comercial",
            ],
            x=262,
            y=406,
        )

        self._label(fr, "Número", x=508, y=380)

        self.ent_celular_paciente_cadastro = self._entry(
            fr,
            200,
            placeholder="Ex. 7190000-0000",
            x=508,
            y=406,
        )

        self._label(fr, "Observação", x=724, y=380)

        self.ent_obsevacao_celular_paciente_cadastro = self._entry(
            fr,
            376,
            x=724,
            y=406,
        )

        self._action_buttons(
            self.tab_cadastro_paciente,
            limpar_cmd=self.limpar_cadastro_paciente,
            salvar_cmd=self.salvar_paciente,
        )

    # ============================================================
    # CADASTRO MÉDICO
    # ============================================================

    def cadastro_medico(self):

        fr = self._section_frame(self.tab_cadastro_medicos)

        self._label(fr, "GERAL", 14, bold=True, x=16, y=18)

        self._label(fr, "Código", x=16, y=46)

        self.ent_codigo_medico_cadastro = self._entry(
            fr,
            90,
            disabled=True,
            x=16,
            y=72,
        )

        self._label(fr, "Nome completo", x=122, y=46)

        self.ent_nome_medico_cadastro = self._entry(
            fr,
            363,
            x=122,
            y=72,
        )

        self._label(fr, "Especialidade", x=501, y=46)

        self.cb_especialidade_medico_cadastro = self._combo(
            fr,
            200,
            [
                "Clínico",
                "Obstetra",
                "Pediatra",
                "Ortopedista",
                "Dermatologista",
                "Cardiologista",
                "Ginecologista",
            ],
            x=501,
            y=72,
        )

        self._label(fr, "CRM/CFM", x=717, y=46)

        self.cb_crm_medico_cadastro = self._combo(
            fr,
            128,
            ["CRM", "CFM"],
            x=717,
            y=72,
        )

        self._label(fr, "Número", x=861, y=46)

        self.ent_numero_crm_medico_cadastro = self._entry(
            fr,
            122,
            x=861,
            y=72,
        )

        self._label(fr, "UF", x=999, y=46)

        self.cb_uf_crm_medico_cadastro = self._combo(
            fr,
            100,
            self._ufs(),
            x=999,
            y=72,
        )

        # ========================================================

        self._label(fr, "CPF", x=16, y=110)

        self.ent_cpf_medico_cadastro = self._entry(
            fr,
            186,
            x=16,
            y=134,
        )

        self._label(fr, "RG", x=218, y=110)

        self.ent_rg_medico_cadastro = self._entry(
            fr,
            186,
            x=218,
            y=134,
        )

        self._label(fr, "Órgão", x=420, y=110)

        self.cb_orgao_rg_medico_cadastro = self._combo(
            fr,
            117,
            ["SSP"],
            x=420,
            y=134,
        )

        self._label(fr, "UF", x=553, y=110)

        self.cb_uf_rg_medico_cadastro = self._combo(
            fr,
            100,
            self._ufs(),
            x=553,
            y=134,
        )

        self._label(fr, "Sexo", x=669, y=110)

        self.cb_sexo_medico_cadastro = self._combo(
            fr,
            162,
            [
                "Masculino",
                "Feminino",
                "Não-binário",
                "Agênero",
                "Gênero fluido",
                "Não declarado",
            ],
            x=669,
            y=134,
        )

        self._label(fr, "Data de nascimento", x=847, y=110)

        self.ent_nascimento_medico_cadastro = self._entry(
            fr,
            210,
            placeholder="dd/mm/aaaa",
            x=847,
            y=134,
        )

        self._cal_button(
            fr,
            command=lambda: self.pop_calendario(
                self.ent_nascimento_medico_cadastro
            ),
            x=1063,
            y=134,
        )

        # ========================================================

        self._label(fr, "ENDEREÇO", 14, bold=True, x=16, y=186)

        self._label(fr, "CEP", x=16, y=208)

        self.ent_cep_medico_cadastro = self._entry(
            fr,
            141,
            x=16,
            y=232,
        )

        self._label(fr, "Endereço", x=173, y=208)

        self.ent_endereco_medico_cadastro = self._entry(
            fr,
            352,
            x=173,
            y=232,
        )

        self._label(fr, "Número", x=541, y=208)

        self.ent_numero_medico_cadastro = self._entry(
            fr,
            70,
            x=541,
            y=232,
        )

        self._label(fr, "Bairro", x=627, y=208)

        self.ent_bairro_medico_cadastro = self._entry(
            fr,
            170,
            x=627,
            y=232,
        )

        self._label(fr, "Cidade", x=813, y=208)

        self.ent_cidade_medico_cadastro = self._entry(
            fr,
            177,
            x=813,
            y=232,
        )

        self._label(fr, "Estado", x=1006, y=208)

        self.cb_estado_medico_cadastro = self._combo(
            fr,
            95,
            self._ufs(),
            x=1006,
            y=232,
        )

        # ========================================================

        self._label(fr, "CONTATOS", 14, bold=True, x=16, y=292)

        self._label(fr, "E-Mail", x=16, y=316)

        self.ent_email_medico_cadastro = self._entry(
            fr,
            341,
            x=16,
            y=342,
        )

        self._label(fr, "Observação", x=373, y=316)

        self.ent_observacao_email_medico_cadastro = self._entry(
            fr,
            726,
            x=373,
            y=342,
        )

        self._label(fr, "Celular/Telefone", x=16, y=380)

        self.cb_tipo_numero_medico = self._combo(
            fr,
            228,
            [
                "Celular",
                "Celular/WhatsApp",
                "Telefone",
            ],
            x=16,
            y=406,
        )

        self._label(fr, "Tipo de contato", x=262, y=380)

        self.cb_tipo_contato_medico = self._combo(
            fr,
            228,
            [
                "Pessoal",
                "Residencial",
                "Comercial",
            ],
            x=262,
            y=406,
        )

        self._label(fr, "Número", x=508, y=380)

        self.ent_celular_medico_cadastro = self._entry(
            fr,
            200,
            placeholder="Ex. 7190000-0000",
            x=508,
            y=406,
        )

        self._label(fr, "Observação", x=724, y=380)

        self.ent_obsevacao_celular_medico_cadastro = self._entry(
            fr,
            376,
            x=724,
            y=406,
        )

        self._action_buttons(
            self.tab_cadastro_medicos,
            limpar_cmd=self.limpar_cadastro_medico,
            salvar_cmd=self.salvar_medico,
        )

    # ============================================================
    # LIMPEZA
    # ============================================================

    def limpar_cadastro_paciente(self):

        for w in [
            self.ent_nome_paciente_cadastro,
            self.ent_nascimento_paciente_cadastro,
            self.ent_cpf_paciente_cadastro,
            self.ent_cep_paciente_cadastro,
            self.ent_endereco_paciente_cadastro,
            self.ent_bairro_paciente_cadastro,
            self.ent_cidade_paciente_cadastro,
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

    # ============================================================
    # CALENDÁRIO
    # ============================================================

    def pop_calendario(self, entry_destino):

        self._calendar_target = entry_destino

        colors = self._tm.colors

        self.pop = ctk.CTkToplevel(self)

        self.pop.configure(fg_color=colors["WHITE"])

        self.pop.geometry("386x287")
        self.pop.title("Calendário")
        self.pop.resizable(False, False)

        self.pop.transient(self)
        self.pop.grab_set()
        self.pop.focus_force()

        self.calendario = Calendar(
            self.pop,
            selectmode="day",
            date_pattern="dd/mm/yyyy",
        )

        self.calendario.place(
            x=0,
            y=0,
            width=386,
            height=207,
        )

        self.bt_confirmar = ctk.CTkButton(
            self.pop,
            text="Confirmar",
            text_color=colors["TOPBAR_TEXT"],
            font=(self._tm.font, 12, "bold"),
            width=167,
            height=36,
            fg_color=colors["BLUE"],
            hover_color=colors["DARK_BLUE"],
            command=self.get_data,
        )

        self.bt_confirmar.place(x=18, y=231)

        self.bt_cancelar_cal = ctk.CTkButton(
            self.pop,
            text="Cancelar",
            text_color=colors["BLUE"],
            font=(self._tm.font, 12, "bold"),
            width=167,
            height=36,
            fg_color=colors["BLUE_XL"],
            hover_color=colors["GRAY_LIGHT"],
            command=self.fecha_calendario,
        )

        self.bt_cancelar_cal.place(x=201, y=231)

    def get_data(self):

        if self._calendar_target is not None:

            self._calendar_target.delete(0, END)

            self._calendar_target.insert(
                END,
                self.calendario.get_date(),
            )

        self.pop.destroy()

    def fecha_calendario(self):

        if hasattr(self, "pop"):
            self.pop.destroy()

    # ============================================================
    # AÇÕES
    # ============================================================

    def salvar_paciente(self):
        pass

    def salvar_medico(self):
        pass