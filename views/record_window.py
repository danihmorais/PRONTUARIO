import customtkinter as ctk
from theme_manager import ThemeManager

class RecordWindow(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self._tm = ThemeManager.get()
        self._build_ui()

    def _build_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        title = ctk.CTkLabel(
            header, 
            text="Prontuário Eletrônico", 
            font=(self._tm.font, 24, "bold"), 
            text_color=self._tm.c("BLACK")
        )
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            header, 
            text="Evolução, relatos e prescrições do paciente", 
            font=(self._tm.font, 13), 
            text_color=self._tm.c("GRAY")
        )
        subtitle.pack(anchor="w", pady=(4, 0))

        self.container = ctk.CTkScrollableFrame(
            self, 
            fg_color=self._tm.c("WHITE"), 
            corner_radius=10, 
            border_color=self._tm.c("GRAY_LIGHT"), 
            border_width=1
        )
        self.container.pack(fill="both", expand=True)

        pac_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        pac_frame.pack(fill="x", padx=20, pady=20)
        
        lbl_pac = ctk.CTkLabel(
            pac_frame, 
            text="Paciente Selecionado:", 
            font=(self._tm.font, 14, "bold"), 
            text_color=self._tm.c("BLACK")
        )
        lbl_pac.pack(side="left")
        
        self.lbl_paciente_nome = ctk.CTkLabel(
            pac_frame, 
            text="Nenhum paciente selecionado", 
            font=(self._tm.font, 14), 
            text_color=self._tm.c("GRAY")
        )
        self.lbl_paciente_nome.pack(side="left", padx=10)
        
        btn_buscar = ctk.CTkButton(
            pac_frame, 
            text="Buscar Paciente", 
            fg_color=self._tm.c("BLUE"), 
            hover_color=self._tm.c("DARK_BLUE"), 
            text_color=self._tm.c("TOPBAR_TEXT"),
            font=(self._tm.font, 12, "bold")
        )
        btn_buscar.pack(side="right")

        self.txt_queixa = self._add_textbox("Motivo da Consulta / Queixa Principal (Relato do Paciente)")
        self.txt_exame = self._add_textbox("Exame Físico / Procedimentos Realizados")
        self.txt_diagnostico = self._add_textbox("Diagnóstico / Conduta Clínica")
        self.txt_prescricao = self._add_textbox("Prescrição Médica")

        footer = ctk.CTkFrame(self.container, fg_color="transparent")
        footer.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(
            footer, 
            text="Salvar Prontuário", 
            fg_color=self._tm.c("BLUE"), 
            hover_color=self._tm.c("DARK_BLUE"), 
            text_color=self._tm.c("TOPBAR_TEXT"),
            font=(self._tm.font, 12, "bold"),
            height=40
        ).pack(side="right")
        
        ctk.CTkButton(
            footer, 
            text="Limpar", 
            fg_color=self._tm.c("BLUE_XL"), 
            hover_color=self._tm.c("GRAY_LIGHT"), 
            text_color=self._tm.c("BLUE"),
            font=(self._tm.font, 12, "bold"),
            height=40,
            command=self._limpar
        ).pack(side="right", padx=10)

    def _add_textbox(self, label_text):
        fr = ctk.CTkFrame(self.container, fg_color="transparent")
        fr.pack(fill="x", padx=20, pady=10)
        
        lbl = ctk.CTkLabel(
            fr, 
            text=label_text, 
            font=(self._tm.font, 13, "bold"), 
            text_color=self._tm.c("BLACK")
        )
        lbl.pack(anchor="w", pady=(0, 5))
        
        txt = ctk.CTkTextbox(
            fr, 
            height=100, 
            fg_color=self._tm.c("GRAY_BG"), 
            border_color=self._tm.c("GRAY_LIGHT"), 
            border_width=1, 
            text_color=self._tm.c("BLACK"),
            font=(self._tm.font, 13)
        )
        txt.pack(fill="x")
        return txt

    def _limpar(self):
        self.txt_queixa.delete("1.0", "end")
        self.txt_exame.delete("1.0", "end")
        self.txt_diagnostico.delete("1.0", "end")
        self.txt_prescricao.delete("1.0", "end")