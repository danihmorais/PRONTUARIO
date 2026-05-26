import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from datetime import datetime
from theme_manager import ThemeManager
from config import DB_PATH

class RecordWindow(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self._tm = ThemeManager.get()
        self.paciente_id_selecionado = None
        self._build_ui()

    def _build_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        title = ctk.CTkLabel(header, text="Prontuário Fisioterapêutico", font=(self._tm.font, 24, "bold"), text_color=self._tm.c("BLACK"))
        title.pack(anchor="w")
        subtitle = ctk.CTkLabel(header, text="Evolução, relatos e prescrições do paciente", font=(self._tm.font, 13), text_color=self._tm.c("GRAY"))
        subtitle.pack(anchor="w", pady=(4, 0))
        
        search_frame = ctk.CTkFrame(self, fg_color=self._tm.c("WHITE"), corner_radius=10, border_color=self._tm.c("GRAY_LIGHT"), border_width=1)
        search_frame.pack(fill="x", pady=(0, 10))
        lbl_busca = ctk.CTkLabel(search_frame, text="Buscar Paciente (CPF):", font=(self._tm.font, 12, "bold"), text_color=self._tm.c("BLACK"))
        lbl_busca.pack(side="left", padx=10, pady=10)
        self.ent_busca_cpf = ctk.CTkEntry(search_frame, width=200, fg_color=self._tm.c("GRAY_BG"), text_color=self._tm.c("BLACK"))
        self.ent_busca_cpf.pack(side="left", padx=10, pady=10)
        btn_buscar = ctk.CTkButton(search_frame, text="Buscar e Carregar", fg_color=self._tm.c("BLUE"), hover_color=self._tm.c("DARK_BLUE"), text_color=self._tm.c("TOPBAR_TEXT"), font=(self._tm.font, 12, "bold"), command=self.buscar_paciente)
        btn_buscar.pack(side="left", padx=10, pady=10)
        
        self.lbl_paciente_nome = ctk.CTkLabel(search_frame, text="Nenhum paciente selecionado", font=(self._tm.font, 14, "bold"), text_color=self._tm.c("GRAY_DARK"))
        self.lbl_paciente_nome.pack(side="right", padx=20, pady=10)

        self.tbv_prontuario = ctk.CTkTabview(self, fg_color=self._tm.c("WHITE"), bg_color="transparent", border_color=self._tm.c("GRAY_LIGHT"), border_width=1, corner_radius=10, text_color=self._tm.c("BLACK"))
        self.tbv_prontuario.pack(fill="both", expand=True)
        
        self.tab_novo = self.tbv_prontuario.add("Novo Registro")
        self.tab_hist = self.tbv_prontuario.add("Histórico do Paciente")
        self.tab_novo.grid_columnconfigure(0, weight=1)
        self.tab_hist.grid_columnconfigure(0, weight=1)

        self._build_novo_registro()
        self._build_historico()

    def _build_novo_registro(self):
        self.container_novo = ctk.CTkScrollableFrame(self.tab_novo, fg_color="transparent")
        self.container_novo.pack(fill="both", expand=True)
        self.txt_queixa = self._add_textbox(self.container_novo, "Motivo da Consulta / Queixa Principal")
        self.txt_exame = self._add_textbox(self.container_novo, "Avaliação Fisioterapêutica / Exame Físico")
        self.txt_diagnostico = self._add_textbox(self.container_novo, "Diagnóstico Cinesiológico Funcional / Conduta")
        self.txt_prescricao = self._add_textbox(self.container_novo, "Prescrição de Exercícios / Orientações")
        footer = ctk.CTkFrame(self.container_novo, fg_color="transparent")
        footer.pack(fill="x", padx=20, pady=20)
        ctk.CTkButton(footer, text="Salvar Prontuário", fg_color=self._tm.c("BLUE"), hover_color=self._tm.c("DARK_BLUE"), text_color=self._tm.c("TOPBAR_TEXT"), font=(self._tm.font, 12, "bold"), height=40, command=self.salvar_prontuario).pack(side="right")
        ctk.CTkButton(footer, text="Limpar", fg_color=self._tm.c("BLUE_XL"), hover_color=self._tm.c("GRAY_LIGHT"), text_color=self._tm.c("BLUE"), font=(self._tm.font, 12, "bold"), height=40, command=self._limpar).pack(side="right", padx=10)

    def _build_historico(self):
        self.container_hist = ctk.CTkScrollableFrame(self.tab_hist, fg_color="transparent")
        self.container_hist.pack(fill="both", expand=True)
        self.lbl_historico_vazio = ctk.CTkLabel(self.container_hist, text="Busque um paciente pelo CPF para ver o histórico.", font=(self._tm.font, 14), text_color=self._tm.c("GRAY"))
        self.lbl_historico_vazio.pack(pady=40)

    def _add_textbox(self, parent, label_text):
        fr = ctk.CTkFrame(parent, fg_color="transparent")
        fr.pack(fill="x", padx=20, pady=10)
        lbl = ctk.CTkLabel(fr, text=label_text, font=(self._tm.font, 13, "bold"), text_color=self._tm.c("BLACK"))
        lbl.pack(anchor="w", pady=(0, 5))
        txt = ctk.CTkTextbox(fr, height=100, fg_color=self._tm.c("GRAY_BG"), border_color=self._tm.c("GRAY_LIGHT"), border_width=1, text_color=self._tm.c("BLACK"), font=(self._tm.font, 13))
        txt.pack(fill="x")
        return txt

    def buscar_paciente(self):
        cpf = self.ent_busca_cpf.get().strip()
        if not cpf:
            messagebox.showwarning("Atenção", "Digite o CPF do paciente para buscar.")
            return
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome FROM pacientes WHERE cpf = ?", (cpf,))
            paciente = cursor.fetchone()
            if paciente:
                self.paciente_id_selecionado = paciente[0]
                self.lbl_paciente_nome.configure(text=f"Paciente: {paciente[1]}", text_color=self._tm.c("BLUE"))
                self.carregar_historico(cursor, self.paciente_id_selecionado)
            else:
                self.paciente_id_selecionado = None
                self.lbl_paciente_nome.configure(text="Paciente não encontrado", text_color=self._tm.c("RED"))
                self.limpar_historico()
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar paciente: {str(e)}")

    def carregar_historico(self, cursor, paciente_id):
        self.limpar_historico()
        cursor.execute("SELECT data_registro, queixa, exame, diagnostico, prescricao FROM prontuarios WHERE id_paciente = ? ORDER BY id DESC", (paciente_id,))
        registros = cursor.fetchall()
        if not registros:
            lbl = ctk.CTkLabel(self.container_hist, text="Nenhum registro encontrado para este paciente.", font=(self._tm.font, 14), text_color=self._tm.c("GRAY"))
            lbl.pack(pady=40)
            return
        for reg in registros:
            data_reg, queixa, exame, diag, presc = reg
            card = ctk.CTkFrame(self.container_hist, fg_color=self._tm.c("GRAY_BG"), corner_radius=8, border_color=self._tm.c("GRAY_LIGHT"), border_width=1)
            card.pack(fill="x", padx=20, pady=10)
            lbl_data = ctk.CTkLabel(card, text=f"Data: {data_reg}", font=(self._tm.font, 12, "bold"), text_color=self._tm.c("BLUE"))
            lbl_data.pack(anchor="w", padx=10, pady=(10, 5))
            self._add_hist_label(card, "Motivo / Queixa:", queixa)
            self._add_hist_label(card, "Avaliação Fisioterapêutica:", exame)
            self._add_hist_label(card, "Diagnóstico / Conduta:", diag)
            self._add_hist_label(card, "Prescrição / Orientações:", presc)

    def _add_hist_label(self, parent, title, content):
        if content and content.strip():
            fr = ctk.CTkFrame(parent, fg_color="transparent")
            fr.pack(fill="x", padx=10, pady=2)
            lbl_title = ctk.CTkLabel(fr, text=title, font=(self._tm.font, 12, "bold"), text_color=self._tm.c("BLACK"))
            lbl_title.pack(anchor="w")
            lbl_content = ctk.CTkLabel(fr, text=content, font=(self._tm.font, 12), text_color=self._tm.c("GRAY_DARK"), justify="left", wraplength=800)
            lbl_content.pack(anchor="w", padx=10)

    def limpar_historico(self):
        for widget in self.container_hist.winfo_children():
            widget.destroy()

    def salvar_prontuario(self):
        if not self.paciente_id_selecionado:
            messagebox.showwarning("Atenção", "Busque e selecione um paciente primeiro.")
            return
        queixa = self.txt_queixa.get("1.0", "end").strip()
        exame = self.txt_exame.get("1.0", "end").strip()
        diag = self.txt_diagnostico.get("1.0", "end").strip()
        presc = self.txt_prescricao.get("1.0", "end").strip()
        if not queixa and not exame and not diag and not presc:
            messagebox.showwarning("Atenção", "Preencha ao menos um dos campos para salvar o prontuário.")
            return
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO prontuarios (id_paciente, data_registro, queixa, exame, diagnostico, prescricao) VALUES (?, ?, ?, ?, ?, ?)", (self.paciente_id_selecionado, data_atual, queixa, exame, diag, presc))
            conn.commit()
            self.carregar_historico(cursor, self.paciente_id_selecionado)
            conn.close()
            messagebox.showinfo("Sucesso", "Registro do prontuário salvo com sucesso!")
            self._limpar()
            self.tbv_prontuario.set("Histórico do Paciente")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar prontuário: {str(e)}")

    def _limpar(self):
        self.txt_queixa.delete("1.0", "end")
        self.txt_exame.delete("1.0", "end")
        self.txt_diagnostico.delete("1.0", "end")
        self.txt_prescricao.delete("1.0", "end")