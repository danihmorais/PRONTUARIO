import customtkinter as ctk
from theme_manager import ThemeManager

class AppointmentWindow(ctk.CTkFrame):
    def __init__(self, parent, controller=None, usuario=None):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self._tm = ThemeManager.get()
        self._build_ui()

    def _build_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        title = ctk.CTkLabel(
            header, 
            text="Consultas", 
            font=(self._tm.font, 24, "bold"), 
            text_color=self._tm.c("BLACK")
        )
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            header, 
            text="Agendamento e gerenciamento de consultas", 
            font=(self._tm.font, 13), 
            text_color=self._tm.c("GRAY")
        )
        subtitle.pack(anchor="w", pady=(4, 0))

        self.tbv_consulta = ctk.CTkTabview(
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
        self.tbv_consulta.pack(fill="both", expand=True)

        self.tab_agendar = self.tbv_consulta.add("Agendar Consulta")
        self.tab_buscar = self.tbv_consulta.add("Buscar Consultas")

        self.tab_agendar.grid_columnconfigure(0, weight=1)
        self.tab_buscar.grid_columnconfigure(0, weight=1)

        self.agendar_consulta()

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

    def _combo_field(self, parent, label, row, col, values, colspan=1):
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

    def agendar_consulta(self):
        container = ctk.CTkScrollableFrame(self.tab_agendar, fg_color="transparent")
        container.pack(fill="both", expand=True)

        pac = self._section(container, "DADOS DO PACIENTE")
        pac.pack(fill="x", padx=10)
        self.ent_nome_pac = self._field(pac, "Nome do Paciente", 0, 0, 3)
        self.ent_cpf_pac = self._field(pac, "CPF", 0, 3)

        med = self._section(container, "DADOS DO MÉDICO")
        med.pack(fill="x", padx=10)
        self.ent_nome_med = self._field(med, "Nome do Médico", 0, 0, 3)
        self.ent_esp_med = self._field(med, "Especialidade", 0, 3)

        con = self._section(container, "DADOS DA CONSULTA")
        con.pack(fill="x", padx=10)
        self.cb_convenio = self._combo_field(con, "Convênio", 0, 0, ["Particular", "Unimed", "Bradesco", "SulAmérica"], 2)
        self.ent_data = self._field(con, "Data", 0, 2, calendar=True)
        self.ent_hora = self._field(con, "Horário", 0, 3)
        self.ent_obs = self._field(con, "Observação", 1, 0, 4)

        fr = ctk.CTkFrame(container, fg_color="transparent")
        fr.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(
            fr, 
            text="Confirmar Agendamento", 
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
            command=self.limpar_campos
        ).pack(side="right", padx=10)

    def limpar_campos(self):
        for attr in dir(self):
            w = getattr(self, attr)
            if isinstance(w, ctk.CTkEntry):
                w.delete(0, "end")

    def pop_calendario(self, entry):
        entry.delete(0, "end")
        entry.insert(0, "01/01/2026") # Implementação simplificada para o popup