import shutil
import customtkinter as ctk
from tkinter import filedialog, messagebox
from theme_manager import ThemeManager
from config import DB_PATH

class ConfigView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self._tm = ThemeManager.get()
        self._build_ui()

    def _build_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        title = ctk.CTkLabel(
            header, 
            text="Configurações", 
            font=(self._tm.font, 24, "bold"), 
            text_color=self._tm.c("BLACK")
        )
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            header, 
            text="Ajustes do sistema e backup de dados", 
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

        lbl_backup = ctk.CTkLabel(
            container, 
            text="Backup do Banco de Dados", 
            font=(self._tm.font, 16, "bold"), 
            text_color=self._tm.c("BLACK")
        )
        lbl_backup.pack(anchor="w", padx=20, pady=(20, 5))
        
        desc_backup = ctk.CTkLabel(
            container, 
            text="Salve uma cópia de segurança de todos os dados do sistema.", 
            font=(self._tm.font, 13), 
            text_color=self._tm.c("GRAY")
        )
        desc_backup.pack(anchor="w", padx=20, pady=(0, 15))

        btn_backup = ctk.CTkButton(
            container, 
            text="Gerar Backup", 
            fg_color=self._tm.c("BLUE"), 
            hover_color=self._tm.c("DARK_BLUE"), 
            text_color=self._tm.c("TOPBAR_TEXT"), 
            font=(self._tm.font, 14, "bold"), 
            height=40, 
            command=self._gerar_backup
        )
        btn_backup.pack(anchor="w", padx=20, pady=(0, 30))

        div = ctk.CTkFrame(container, height=1, fg_color=self._tm.c("GRAY_LIGHT"))
        div.pack(fill="x", padx=20, pady=10)

        lbl_info = ctk.CTkLabel(
            container, 
            text="Informações do Sistema", 
            font=(self._tm.font, 16, "bold"), 
            text_color=self._tm.c("BLACK")
        )
        lbl_info.pack(anchor="w", padx=20, pady=(20, 5))

        info_text = f"Versão do Sistema: 1.0.0\nCaminho do Banco: {DB_PATH}"
        lbl_info_det = ctk.CTkLabel(
            container, 
            text=info_text, 
            font=(self._tm.font, 13), 
            text_color=self._tm.c("GRAY"), 
            justify="left"
        )
        lbl_info_det.pack(anchor="w", padx=20, pady=(0, 20))

    def _gerar_backup(self):
        caminho_destino = filedialog.asksaveasfilename(
            defaultextension=".db",
            initialfile="prontuario_backup.db",
            title="Salvar Backup Como",
            filetypes=[("Database Files", "*.db"), ("All Files", "*.*")]
        )
        
        if not caminho_destino:
            return
        
        try:
            shutil.copy2(DB_PATH, caminho_destino)
            messagebox.showinfo("Sucesso", "Backup gerado com sucesso!")
        except Exception:
            messagebox.showerror("Erro", "Não foi possível gerar o backup.")