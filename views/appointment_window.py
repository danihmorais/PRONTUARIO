import customtkinter as ctk
import os
from views.components.base_window import BaseWindow
from config import BASE_DIR


class AppointmentWindow(BaseWindow):

    def __init__(self, parent, controller, usuario=None):
        super().__init__(
            parent=parent,
            controller=controller,
            title="Prontuário - Consulta",
            usuario=usuario,
        )

        self.minsize(1280, 720)
        self.iconbitmap(os.path.join(BASE_DIR, "assets", "icon.ico"))

        self.after(10, self._maximize)
        self.transient(parent)
        self.grab_set()

        self._build_tabview()
        self.agendar_consulta()

        self.protocol("WM_DELETE_WINDOW", self._fechar)

    # =========================================================
    # TABVIEW
    # =========================================================
    def _build_tabview(self):

        self.tbv_consulta = ctk.CTkTabview(
            self,
            fg_color=self._tm.c("WHITE"),
            border_width=1.5,
        )

        self.tbv_consulta.grid(
            row=1, column=0, sticky="nsew", padx=20, pady=(66, 10)
        )

        self.tab_agendar_consulta = self.tbv_consulta.add("Agendar Consulta")
        self.tab_buscar_consulta = self.tbv_consulta.add("Buscar Consulta")

        self.tab_agendar_consulta.grid_columnconfigure(0, weight=1)

    # =========================================================
    # FORMULÁRIO PRINCIPAL
    # =========================================================
    def agendar_consulta(self):

        container = ctk.CTkScrollableFrame(self.tab_agendar_consulta)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        fr = ctk.CTkFrame(container)
        fr.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        fr.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="cols")

        # =========================================================
        # PACIENTE
        # =========================================================
        pac = self._section(fr, "DADOS DO PACIENTE")
        pac.grid(row=0, column=0, columnspan=4, sticky="ew", pady=10)

        self.ent_nome_paciente_agendamento = self._field(pac, "Nome", 0, 0, 2)
        self.ent_nascimento_paciente_agendamento = self._field(
            pac, "Nascimento", 0, 2, 1, calendar=True
        )
        self.ent_cpf_paciente_agendamento = self._field(pac, "CPF", 1, 0)
        self.cb_sexo_paciente_agendamento = self._combo(pac, "Sexo", 1, 1)
        self.ent_email_paciente_agendamento = self._field(pac, "Email", 1, 2)

        # =========================================================
        # MÉDICO
        # =========================================================
        med = self._section(fr, "DADOS DO MÉDICO")
        med.grid(row=1, column=0, columnspan=4, sticky="ew", pady=10)

        self.ent_nome_medico_agendamento = self._field(med, "Nome", 0, 0, 2)
        self.ent_especialidade1_medico_agendamento = self._field(med, "Especialidade 1", 0, 2)
        self.ent_especialidade2_medico_agendamento = self._field(med, "Especialidade 2", 1, 0)
        self.ent_crm_medico_agendamento = self._field(med, "CRM", 1, 1)

        # =========================================================
        # CONSULTA
        # =========================================================
        con = self._section(fr, "DADOS DA CONSULTA")
        con.grid(row=2, column=0, columnspan=4, sticky="ew", pady=10)

        self.cb_convenio_agendamento = self._combo(con, "Convênio", 0, 0)
        self.cb_plano_saude_agendamento = self._combo(con, "Plano", 0, 1)

        self.ent_data_consulta_agendamento = self._field(
            con, "Data", 0, 2, calendar=True
        )
        self.ent_hora_consulta_agendamento = self._field(con, "Hora", 0, 3)

        self.ent_observacao_convenio_agendamento = self._field(
            con, "Observação", 1, 0, 4
        )

        # =========================================================
        # BOTÕES
        # =========================================================
        btns = ctk.CTkFrame(fr)
        btns.grid(row=3, column=0, columnspan=4, sticky="ew", pady=20)

        ctk.CTkButton(btns, text="Cancelar", command=self._fechar).pack(
            side="left", padx=10
        )
        ctk.CTkButton(btns, text="Limpar", command=self.limpar_campos).pack(
            side="right", padx=10
        )
        ctk.CTkButton(btns, text="Agendar", command=self.salvar_consulta).pack(
            side="right", padx=10
        )

    # =========================================================
    # HELPERS
    # =========================================================
    def _section(self, parent, title):
        frame = ctk.CTkFrame(parent)
        frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="cols")

        label = ctk.CTkLabel(
            frame,
            text=title,
            font=(self._tm.font, 14, "bold"),
        )
        label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5), columnspan=4)

        return frame

    def _field(self, parent, label, row, col, colspan=1, calendar=False):

        lbl = ctk.CTkLabel(parent, text=label)
        lbl.grid(row=row * 2 + 1, column=col, sticky="w", padx=10)

        entry = ctk.CTkEntry(parent)
        entry.grid(
            row=row * 2 + 2,
            column=col,
            columnspan=colspan,
            sticky="ew",
            padx=10,
            pady=(0, 10),
        )

        if calendar:
            btn = ctk.CTkButton(
                parent,
                text="📅",
                width=30,
                command=lambda: self.pop_calendario(entry),
            )
            btn.grid(row=row * 2 + 2, column=col + 1, sticky="w")

        return entry

    def _combo(self, parent, label, row, col):

        lbl = ctk.CTkLabel(parent, text=label)
        lbl.grid(row=row * 2 + 1, column=col, sticky="w", padx=10)

        combo = ctk.CTkComboBox(
            parent,
            values=["Sim", "Não", "N/A"],
        )
        combo.grid(row=row * 2 + 2, column=col, sticky="ew", padx=10, pady=(0, 10))

        return combo

    # =========================================================
    # AÇÕES
    # =========================================================
    def limpar_campos(self):
        for attr in dir(self):
            w = getattr(self, attr)
            if isinstance(w, (ctk.CTkEntry, ctk.CTkComboBox)):
                try:
                    w.delete(0, "end")
                except:
                    w.set("")

    def pop_calendario(self, entry):
        entry.delete(0, "end")
        entry.insert(0, "01/01/2026")

    def buscar_paciente(self):
        pass

    def buscar_medico(self):
        pass

    def salvar_consulta(self):
        pass