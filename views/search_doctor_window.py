import customtkinter as ctk
import sqlite3
from theme_manager import ThemeManager
from config import DB_PATH

class SearchDoctorView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self._tm = ThemeManager.get()
        self._build_ui()

    def _build_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        title = ctk.CTkLabel(header, text="Equipe Clínica e Funcionários", font=(self._tm.font, 24, "bold"), text_color=self._tm.c("BLACK"))
        title.pack(anchor="w")
        subtitle = ctk.CTkLabel(header, text="Consulte os fisioterapeutas e funcionários cadastrados", font=(self._tm.font, 13), text_color=self._tm.c("GRAY"))
        subtitle.pack(anchor="w", pady=(4, 0))

        search_frame = ctk.CTkFrame(self, fg_color=self._tm.c("WHITE"), corner_radius=10, border_color=self._tm.c("GRAY_LIGHT"), border_width=1)
        search_frame.pack(fill="x", pady=(0, 20))

        self.ent_busca = ctk.CTkEntry(search_frame, placeholder_text="Buscar por nome ou CPF...", fg_color=self._tm.c("GRAY_BG"), border_color=self._tm.c("GRAY_LIGHT"), text_color=self._tm.c("BLACK"), width=300, height=36)
        self.ent_busca.pack(side="left", padx=20, pady=20)

        self.cb_tipo = ctk.CTkComboBox(search_frame, values=["Fisioterapeutas", "Funcionários"], fg_color=self._tm.c("GRAY_BG"), border_color=self._tm.c("GRAY_LIGHT"), text_color=self._tm.c("BLACK"), button_color=self._tm.c("BLUE"), height=36)
        self.cb_tipo.pack(side="left", padx=10, pady=20)

        btn_buscar = ctk.CTkButton(search_frame, text="Buscar", fg_color=self._tm.c("BLUE"), hover_color=self._tm.c("DARK_BLUE"), text_color=self._tm.c("TOPBAR_TEXT"), font=(self._tm.font, 12, "bold"), height=36, command=self.buscar)
        btn_buscar.pack(side="left", padx=10, pady=20)

        self.tabela = ctk.CTkScrollableFrame(self, fg_color=self._tm.c("WHITE"), corner_radius=10, border_color=self._tm.c("GRAY_LIGHT"), border_width=1)
        self.tabela.pack(fill="both", expand=True)

        self.buscar()

    def buscar(self):
        termo = f"%{self.ent_busca.get().strip()}%"
        tipo = self.cb_tipo.get()

        for widget in self.tabela.winfo_children():
            widget.destroy()

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            if tipo == "Fisioterapeutas":
                cursor.execute("SELECT id, nome, crefito, especialidade, celular FROM fisioterapeutas WHERE nome LIKE ? OR cpf LIKE ?", (termo, termo))
                resultados = cursor.fetchall()
                headers = ["ID", "Nome", "CREFITO", "Especialidade", "Celular"]
            else:
                cursor.execute("SELECT id, nome, cargo, cpf, celular FROM funcionarios WHERE nome LIKE ? OR cpf LIKE ?", (termo, termo))
                resultados = cursor.fetchall()
                headers = ["ID", "Nome", "Cargo", "CPF", "Celular"]

            header_frame = ctk.CTkFrame(self.tabela, fg_color=self._tm.c("GRAY_LIGHT"), corner_radius=5)
            header_frame.pack(fill="x", padx=10, pady=10)

            for i, h in enumerate(headers):
                ctk.CTkLabel(header_frame, text=h, font=(self._tm.font, 12, "bold"), text_color=self._tm.c("BLACK"), width=150, anchor="w").grid(row=0, column=i, padx=10, pady=5)

            for r_data in resultados:
                row_frame = ctk.CTkFrame(self.tabela, fg_color="transparent")
                row_frame.pack(fill="x", padx=10, pady=2)
                for col_idx, valor in enumerate(r_data):
                    ctk.CTkLabel(row_frame, text=str(valor), font=(self._tm.font, 12), text_color=self._tm.c("BLACK"), width=150, anchor="w").grid(row=0, column=col_idx, padx=10, pady=5)

            conn.close()
        except Exception as e:
            pass