import customtkinter as ctk
from tkcalendar import Calendar
from theme_manager import ThemeManager

class FormWindow(ctk.CTkFrame):
    def __init__(self, parent, controller=None, usuario=None):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self._tm = ThemeManager.get()
        self._calendar_target = None
        self._build_ui()

    def _build_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        title = ctk.CTkLabel(
            header, 
            text="Cadastros", 
            font=(self._tm.font, 24, "bold"), 
            text_color=self._tm.c("BLACK")
        )
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            header, 
            text="Cadastre novos pacientes e médicos no sistema", 
            font=(self._tm.font, 13), 
            text_color=self._tm.c("GRAY")
        )
        subtitle.pack(anchor="w", pady=(4, 0))

        self.tbv_cadastros = ctk.CTkTabview(
            self,
            fg_color=self._tm.c("WHITE"),
            bg_color="transparent",
            border_color=self._tm.c("GRAY_LIGHT"),
            border_width=1,
            corner_radius=10,
            segmented_button_selected_color=self._tm.c("BLUE"),
            segmented_button_selected_hover_color=self._tm.c("DARK_BLUE"),
            segmented_button_unselected_color=self._tm.c("GRAY_BG"),
            segmented_button_unselected_hover_color=self._tm.c("GRAY_LIGHT"),
            text_color=self._tm.c("BLACK")
        )
        self.tbv_cadastros.pack(fill="both", expand=True)

        self.tab_paciente = self.tbv_cadastros.add("Pacientes")
        self.tab_medico = self.tbv_cadastros.add("Médicos")

        self.tab_paciente.grid_columnconfigure(0, weight=1)
        self.tab_medico.grid_columnconfigure(0, weight=1)

        self.cadastro_paciente()
        self.cadastro_medico()

    def _section(self, parent, title):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="cols")
        
        label = ctk.CTkLabel(
            frame, 
            text=title, 
            font=(self._tm.font, 14, "bold"), 
            text_color=self._tm.c("BLACK")
        )
        label.grid(row=0, column=0, sticky="w", padx=10, pady=(15, 5), columnspan=4)
        
        div = ctk.CTkFrame(frame, height=1, fg_color=self._tm.c("GRAY_LIGHT"))
        div.grid(row=1, column=0, columnspan=4, sticky="ew", padx=10, pady=(0, 15))
        
        return frame

    def _field(self, parent, label, row, col, colspan=1, calendar=False):
        lbl = ctk.CTkLabel(
            parent, 
            text=label, 
            text_color=self._tm.c("GRAY_DARK"), 
            font=(self._tm.font, 12, "bold")
        )
        lbl.grid(row=row * 2 + 2, column=col, sticky="w", padx=10)
        
        entry = ctk.CTkEntry(
            parent, 
            fg_color=self._tm.c("GRAY_BG"), 
            border_color=self._tm.c("GRAY_LIGHT"), 
            text_color=self._tm.c("BLACK"),
            font=(self._tm.font, 13),
            height=36
        )
        entry.grid(row=row * 2 + 3, column=col, columnspan=colspan, sticky="ew", padx=10, pady=(0, 15))
        
        if calendar:
            btn = ctk.CTkButton(
                parent, 
                text="📅", 
                width=36,
                height=36,
                fg_color=self._tm.c("BLUE"), 
                hover_color=self._tm.c("DARK_BLUE"),
                command=lambda: self.pop_calendario(entry)
            )
            btn.grid(row=row * 2 + 3, column=col + colspan - 1, sticky="e", padx=10, pady=(0, 15))
            
        return entry

    def _combo(self, parent, label, row, col, values, colspan=1):
        lbl = ctk.CTkLabel(
            parent, 
            text=label, 
            text_color=self._tm.c("GRAY_DARK"), 
            font=(self._tm.font, 12, "bold")
        )
        lbl.grid(row=row * 2 + 2, column=col, sticky="w", padx=10)
        
        combo = ctk.CTkComboBox(
            parent, 
            values=values, 
            fg_color=self._tm.c("GRAY_BG"), 
            border_color=self._tm.c("GRAY_LIGHT"), 
            text_color=self._tm.c("BLACK"), 
            button_color=self._tm.c("BLUE"),
            button_hover_color=self._tm.c("DARK_BLUE"),
            dropdown_fg_color=self._tm.c("WHITE"),
            dropdown_text_color=self._tm.c("BLACK"),
            font=(self._tm.font, 13),
            height=36
        )
        combo.grid(row=row * 2 + 3, column=col, columnspan=colspan, sticky="ew", padx=10, pady=(0, 15))
        return combo

    def cadastro_paciente(self):
        container = ctk.CTkScrollableFrame(self.tab_paciente, fg_color="transparent")
        container.pack(fill="both", expand=True)

        geral = self._section(container, "GERAL")
        geral.pack(fill="x", padx=10)
        self.ent_nome_pac = self._field(geral, "Nome completo", 0, 0, 2)
        self.ent_nascimento_pac = self._field(geral, "Data de nascimento", 0, 2, calendar=True)
        self.ent_cpf_pac = self._field(geral, "CPF", 0, 3)
        self.cb_sexo_pac = self._combo(geral, "Sexo", 1, 0, ["Masculino", "Feminino", "Não-binário", "Gênero fluido", "Não declarado"])

        end = self._section(container, "ENDEREÇO")
        end.pack(fill="x", padx=10)
        self.ent_cep_pac = self._field(end, "CEP", 0, 0)
        self.ent_end_pac = self._field(end, "Endereço", 0, 1, 3)
        self.ent_bairro_pac = self._field(end, "Bairro", 1, 0, 2)
        self.ent_cidade_pac = self._field(end, "Cidade", 1, 2)
        self.cb_estado_pac = self._combo(end, "Estado", 1, 3, ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"])

        contato = self._section(container, "CONTATOS")
        contato.pack(fill="x", padx=10)
        self.ent_email_pac = self._field(contato, "E-Mail", 0, 0, 2)
        self.cb_tipo_num_pac = self._combo(contato, "Tipo", 0, 2, ["Celular", "Fixo"])
        self.ent_celular_pac = self._field(contato, "Número", 0, 3)

        self._build_actions(container, self.limpar_cadastro_paciente)

    def cadastro_medico(self):
        container = ctk.CTkScrollableFrame(self.tab_medico, fg_color="transparent")
        container.pack(fill="both", expand=True)

        geral = self._section(container, "GERAL")
        geral.pack(fill="x", padx=10)
        self.ent_nome_med = self._field(geral, "Nome completo", 0, 0, 2)
        self.cb_crm_med = self._combo(geral, "Conselho", 0, 2, ["CRM", "CFM"])
        self.ent_num_crm_med = self._field(geral, "Número do Conselho", 0, 3)
        self.cb_esp_med = self._combo(geral, "Especialidade", 1, 0, ["Clínico", "Obstetra", "Pediatra", "Ortopedista", "Dermatologista", "Cardiologista", "Ginecologista"], 2)
        self.ent_cpf_med = self._field(geral, "CPF", 1, 2)
        self.ent_nasc_med = self._field(geral, "Data de nascimento", 1, 3, calendar=True)

        end = self._section(container, "ENDEREÇO")
        end.pack(fill="x", padx=10)
        self.ent_cep_med = self._field(end, "CEP", 0, 0)
        self.ent_end_med = self._field(end, "Endereço", 0, 1, 3)
        self.ent_bairro_med = self._field(end, "Bairro", 1, 0, 2)
        self.ent_cidade_med = self._field(end, "Cidade", 1, 2)
        self.cb_estado_med = self._combo(end, "Estado", 1, 3, ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"])

        contato = self._section(container, "CONTATOS")
        contato.pack(fill="x", padx=10)
        self.ent_email_med = self._field(contato, "E-Mail", 0, 0, 2)
        self.cb_tipo_num_med = self._combo(contato, "Tipo", 0, 2, ["Celular", "Fixo"])
        self.ent_celular_med = self._field(contato, "Número", 0, 3)

        self._build_actions(container, self.limpar_cadastro_medico)

    def _build_actions(self, parent, cmd_limpar):
        fr = ctk.CTkFrame(parent, fg_color="transparent")
        fr.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(
            fr, 
            text="Salvar Cadastro", 
            fg_color=self._tm.c("BLUE"), 
            hover_color=self._tm.c("DARK_BLUE"),
            text_color=self._tm.c("TOPBAR_TEXT"),
            font=(self._tm.font, 12, "bold"),
            height=40
        ).pack(side="right")
        
        ctk.CTkButton(
            fr, 
            text="Limpar", 
            fg_color=self._tm.c("BLUE_XL"), 
            hover_color=self._tm.c("GRAY_LIGHT"), 
            text_color=self._tm.c("BLUE"),
            font=(self._tm.font, 12, "bold"),
            height=40,
            command=cmd_limpar
        ).pack(side="right", padx=10)

    def limpar_cadastro_paciente(self):
        for attr in dir(self):
            if attr.endswith("_pac"):
                w = getattr(self, attr)
                if isinstance(w, ctk.CTkEntry):
                    w.delete(0, "end")

    def limpar_cadastro_medico(self):
        for attr in dir(self):
            if attr.endswith("_med"):
                w = getattr(self, attr)
                if isinstance(w, ctk.CTkEntry):
                    w.delete(0, "end")

    def pop_calendario(self, entry_destino):
        self._calendar_target = entry_destino
        colors = self._tm.colors

        self.pop = ctk.CTkToplevel(self)
        self.pop.configure(fg_color=colors["WHITE"])
        self.pop.geometry("386x287")
        self.pop.title("Calendário")
        self.pop.resizable(False, False)
        self.pop.transient(self.winfo_toplevel())
        self.pop.grab_set()
        self.pop.focus_force()

        self.calendario = Calendar(self.pop, selectmode="day", date_pattern="dd/mm/yyyy")
        self.calendario.place(x=0, y=0, width=386, height=207)

        bt_confirmar = ctk.CTkButton(
            self.pop, text="Confirmar", text_color=colors["TOPBAR_TEXT"], 
            font=(self._tm.font, 12, "bold"), width=167, height=36, 
            fg_color=colors["BLUE"], hover_color=colors["DARK_BLUE"], command=self.get_data
        )
        bt_confirmar.place(x=18, y=231)

        bt_cancelar = ctk.CTkButton(
            self.pop, text="Cancelar", text_color=colors["BLUE"], 
            font=(self._tm.font, 12, "bold"), width=167, height=36, 
            fg_color=colors["BLUE_XL"], hover_color=colors["GRAY_LIGHT"], command=self.pop.destroy
        )
        bt_cancelar.place(x=201, y=231)

    def get_data(self):
        if self._calendar_target is not None:
            self._calendar_target.delete(0, "end")
            self._calendar_target.insert("end", self.calendario.get_date())
        self.pop.destroy()