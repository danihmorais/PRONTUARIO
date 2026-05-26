import os
import csv
import sqlite3
import customtkinter as ctk
from tkinter import filedialog, messagebox
from theme_manager import ThemeManager
from config import DB_PATH

class ExportView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self._tm = ThemeManager.get()
        self._build_ui()

    def _build_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        title = ctk.CTkLabel(
            header, 
            text="Exportar Dados", 
            font=(self._tm.font, 24, "bold"), 
            text_color=self._tm.c("BLACK")
        )
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            header, 
            text="Exporte as informações do sistema para planilhas CSV", 
            font=(self._tm.font, 13), 
            text_color=self._tm.c("GRAY")
        )
        subtitle.pack(anchor="w", pady=(4, 0))

        container = ctk.CTkFrame(
            self, 
            fg_color=self._tm.c("WHITE"), 
            corner_radius=10, 
            border_color=self._tm.c("GRAY_LIGHT"), 
            border_width=1
        )
        container.pack(fill="both", expand=True)

        self.chk_pacientes = ctk.CTkCheckBox(
            container, 
            text="Pacientes", 
            font=(self._tm.font, 14), 
            fg_color=self._tm.c("BLUE"), 
            hover_color=self._tm.c("DARK_BLUE"), 
            text_color=self._tm.c("BLACK")
        )
        self.chk_pacientes.pack(anchor="w", padx=20, pady=(20, 10))
        self.chk_pacientes.select()

        self.chk_fisioterapeutas = ctk.CTkCheckBox(
            container, 
            text="Fisioterapeutas", 
            font=(self._tm.font, 14), 
            fg_color=self._tm.c("BLUE"), 
            hover_color=self._tm.c("DARK_BLUE"), 
            text_color=self._tm.c("BLACK")
        )
        self.chk_fisioterapeutas.pack(anchor="w", padx=20, pady=10)
        self.chk_fisioterapeutas.select()

        self.chk_consultas = ctk.CTkCheckBox(
            container, 
            text="Consultas", 
            font=(self._tm.font, 14), 
            fg_color=self._tm.c("BLUE"), 
            hover_color=self._tm.c("DARK_BLUE"), 
            text_color=self._tm.c("BLACK")
        )
        self.chk_consultas.pack(anchor="w", padx=20, pady=10)
        self.chk_consultas.select()

        btn_exportar = ctk.CTkButton(
            container, 
            text="Exportar Selecionados", 
            fg_color=self._tm.c("BLUE"), 
            hover_color=self._tm.c("DARK_BLUE"), 
            text_color=self._tm.c("TOPBAR_TEXT"), 
            font=(self._tm.font, 14, "bold"), 
            height=45, 
            command=self._exportar
        )
        btn_exportar.pack(anchor="w", padx=20, pady=30)

    def _exportar(self):
        tabelas = []
        if self.chk_pacientes.get(): 
            tabelas.append("pacientes")
        if self.chk_fisioterapeutas.get(): 
            tabelas.append("fisioterapeutas")
        if self.chk_consultas.get(): 
            tabelas.append("consultas")

        if not tabelas:
            messagebox.showwarning("Aviso", "Selecione pelo menos uma tabela para exportar.")
            return

        diretorio = filedialog.askdirectory(title="Selecione a pasta para salvar os arquivos")
        if not diretorio:
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            for tabela in tabelas:
                cursor.execute(f"SELECT * FROM {tabela}")
                colunas = [desc[0] for desc in cursor.description]
                linhas = cursor.fetchall()
                
                caminho = os.path.join(diretorio, f"{tabela}_export.csv")
                with open(caminho, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(colunas)
                    writer.writerows(linhas)
                    
            conn.close()
            messagebox.showinfo("Sucesso", "Dados exportados com sucesso!")
        except Exception:
            messagebox.showerror("Erro", "Ocorreu um erro ao exportar os dados.")