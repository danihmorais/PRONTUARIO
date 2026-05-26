import re
import sqlite3
import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import Calendar
from theme_manager import ThemeManager
from config import DB_PATH


def _only_digits(s):
    return re.sub(r"\D", "", str(s))


_STATUS_COLORS = {
    "Pendente":   ("#FEF3C7", "#92400E"),
    "Confirmada": ("#D1FAE5", "#065F46"),
    "Cancelada":  ("#FEE2E2", "#991B1B"),
    "Realizada":  ("#EDE9FE", "#5B21B6"),
}


class AppointmentWindow(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self._tm = ThemeManager.get()
        self._calendar_target = None
        self._selected_consulta_id = None

        self._tm.subscribe(self._apply_theme)
        self._build_ui()
        self.carregar_dados()

    # ── UI ────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))

        self.title_lbl = ctk.CTkLabel(
            header, text="Agendamento de Consultas",
            font=(self._tm.font, 24, "bold"),
            text_color=self._tm.c("BLACK"),
        )
        self.title_lbl.pack(anchor="w")

        self.subtitle_lbl = ctk.CTkLabel(
            header, text="Agende e gerencie as sessões de fisioterapia",
            font=(self._tm.font, 13),
            text_color=self._tm.c("GRAY"),
        )
        self.subtitle_lbl.pack(anchor="w", pady=(4, 0))

        # container scrollável
        self.container = ctk.CTkScrollableFrame(
            self,
            fg_color=self._tm.c("WHITE"),
            corner_radius=10,
            border_color=self._tm.c("GRAY_LIGHT"),
            border_width=1,
        )
        self.container.pack(fill="both", expand=True)

        self._build_form()
        self._build_lista()

    def _build_form(self):
        form = ctk.CTkFrame(self.container, fg_color="transparent")
        form.pack(fill="x", padx=20, pady=20)
        form.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Paciente
        self._lbl(form, "Paciente *", 0, 0)
        self.cb_paciente = self._combo_raw(form, 1, 0, 2)

        # Fisioterapeuta
        self._lbl(form, "Fisioterapeuta *", 0, 2)
        self.cb_fisio = self._combo_raw(form, 1, 2, 2)

        # Data
        self._lbl(form, "Data *", 2, 0)
        self.ent_data = ctk.CTkEntry(form, height=36)
        self.ent_data.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 12))
        ctk.CTkButton(
            form, text="📅", width=36, height=36,
            fg_color=self._tm.c("BLUE"),
            hover_color=self._tm.c("DARK_BLUE"),
            command=lambda: self.pop_calendario(self.ent_data)
        ).grid(row=3, column=0, sticky="e", padx=10, pady=(0, 12))

        # Horário
        self._lbl(form, "Horário * (HH:MM)", 2, 1)
        self.ent_hora = ctk.CTkEntry(form, height=36, placeholder_text="08:00")
        self.ent_hora.grid(row=3, column=1, sticky="ew", padx=10, pady=(0, 12))

        # Convênio
        self._lbl(form, "Convênio", 2, 2)
        self.cb_convenio = self._combo_raw(
            form, 3, 2, 1,
            values=["Particular", "Plano de Saúde", "SUS"]
        )

        # Plano
        self._lbl(form, "Nome do Plano", 2, 3)
        self.ent_plano = ctk.CTkEntry(form, height=36)
        self.ent_plano.grid(row=3, column=3, sticky="ew", padx=10, pady=(0, 12))

        # Observação
        self._lbl(form, "Observações", 4, 0)
        self.ent_obs = ctk.CTkEntry(form, height=36, placeholder_text="Observações adicionais")
        self.ent_obs.grid(row=5, column=0, columnspan=4, sticky="ew", padx=10, pady=(0, 12))

        # Botões
        btn_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkButton(
            btn_frame, text="✅  Agendar Consulta",
            height=40,
            fg_color=self._tm.c("BLUE"),
            hover_color=self._tm.c("DARK_BLUE"),
            text_color=self._tm.c("TOPBAR_TEXT"),
            font=(self._tm.font, 13, "bold"),
            command=self.agendar,
        ).pack(side="right")

        ctk.CTkButton(
            btn_frame, text="🔄  Atualizar",
            height=40,
            fg_color=self._tm.c("BLUE_XL"),
            hover_color=self._tm.c("GRAY_LIGHT"),
            text_color=self._tm.c("BLUE"),
            font=(self._tm.font, 13, "bold"),
            command=self.carregar_dados,
        ).pack(side="right", padx=10)

    def _build_lista(self):
        # Cabeçalho da lista
        lf = ctk.CTkFrame(self.container, fg_color="transparent")
        lf.pack(fill="x", padx=20, pady=(10, 0))

        ctk.CTkLabel(
            lf, text="Consultas Agendadas",
            font=(self._tm.font, 16, "bold"),
            text_color=self._tm.c("BLACK"),
        ).pack(side="left")

        # filtro de status
        self.cb_filtro = ctk.CTkComboBox(
            lf,
            values=["Todas", "Pendente", "Confirmada", "Cancelada", "Realizada"],
            width=160, height=32,
            fg_color=self._tm.c("GRAY_BG"),
            border_color=self._tm.c("GRAY_LIGHT"),
            text_color=self._tm.c("BLACK"),
            button_color=self._tm.c("BLUE"),
            command=lambda _: self.carregar_dados()
        )
        self.cb_filtro.set("Todas")
        self.cb_filtro.pack(side="right")

        ctk.CTkLabel(lf, text="Filtrar: ",
                     text_color=self._tm.c("GRAY"),
                     font=(self._tm.font, 12)).pack(side="right", padx=(0, 4))

        # header colunas
        hdr = ctk.CTkFrame(self.container,
                           fg_color=self._tm.c("BLUE_XL"), corner_radius=6)
        hdr.pack(fill="x", padx=20, pady=(8, 2))
        for txt, w in [("Paciente",200), ("Fisioterapeuta",180),
                       ("Data",100), ("Hora",70), ("Status",110), ("Ações",140)]:
            ctk.CTkLabel(hdr, text=txt, width=w, anchor="w",
                         font=(self._tm.font, 12, "bold"),
                         text_color=self._tm.c("DARK_BLUE")).pack(side="left", padx=6, pady=6)

        self.tabela_consultas = ctk.CTkScrollableFrame(
            self.container,
            fg_color=self._tm.c("GRAY_BG"),
            corner_radius=8,
            height=280,
        )
        self.tabela_consultas.pack(fill="x", padx=20, pady=(0, 20))

    # ── helpers ───────────────────────────────────────────────────────────────

    def _lbl(self, parent, text, row, col):
        ctk.CTkLabel(
            parent, text=text,
            font=(self._tm.font, 12, "bold"),
            text_color=self._tm.c("GRAY_DARK"),
        ).grid(row=row, column=col, sticky="w", padx=10)

    def _combo_raw(self, parent, row, col, colspan=1, values=None):
        cb = ctk.CTkComboBox(
            parent,
            values=values or [],
            fg_color=self._tm.c("GRAY_BG"),
            border_color=self._tm.c("GRAY_LIGHT"),
            dropdown_fg_color=self._tm.c("WHITE"),
            dropdown_text_color=self._tm.c("BLACK"),
            button_color=self._tm.c("BLUE"),
            button_hover_color=self._tm.c("DARK_BLUE"),
            text_color=self._tm.c("BLACK"),
            height=36,
        )
        cb.grid(row=row, column=col, columnspan=colspan,
                sticky="ew", padx=10, pady=(0, 12))
        cb.set(values[0] if values else "")
        return cb

    # ── tema reativo ──────────────────────────────────────────────────────────

    def _apply_theme(self, colors):
        self.container.configure(
            fg_color=colors["WHITE"],
            border_color=colors["GRAY_LIGHT"],
        )
        self.tabela_consultas.configure(fg_color=colors["GRAY_BG"])

    # ── dados ─────────────────────────────────────────────────────────────────

    def carregar_dados(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur  = conn.cursor()

            cur.execute("SELECT id, nome FROM pacientes ORDER BY nome")
            self.pacientes_list = cur.fetchall()
            self.cb_paciente.configure(
                values=[f"{p[0]} — {p[1]}" for p in self.pacientes_list]
            )

            cur.execute("SELECT id, nome FROM fisioterapeutas ORDER BY nome")
            self.fisios_list = cur.fetchall()
            self.cb_fisio.configure(
                values=[f"{f[0]} — {f[1]}" for f in self.fisios_list]
            )

            self._render_tabela(cur)
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _render_tabela(self, cursor):
        for w in self.tabela_consultas.winfo_children():
            w.destroy()

        filtro = self.cb_filtro.get()
        query = """
            SELECT c.id, p.nome, f.nome, c.data_consulta, c.horario, c.status
            FROM consultas c
            JOIN pacientes p       ON c.id_paciente        = p.id
            JOIN fisioterapeutas f ON c.id_fisioterapeuta  = f.id
        """
        params = ()
        if filtro != "Todas":
            query += " WHERE c.status = ?"
            params = (filtro,)
        query += " ORDER BY c.data_consulta DESC, c.horario DESC"

        cursor.execute(query, params)
        rows = cursor.fetchall()

        if not rows:
            ctk.CTkLabel(
                self.tabela_consultas,
                text="Nenhuma consulta encontrada.",
                font=(self._tm.font, 13),
                text_color=self._tm.c("GRAY"),
            ).pack(pady=20)
            return

        for idx, (cid, pac, fisio, data, hora, status) in enumerate(rows):
            bg = self._tm.c("WHITE") if idx % 2 == 0 else self._tm.c("GRAY_BG")
            row = ctk.CTkFrame(self.tabela_consultas, fg_color=bg, corner_radius=4)
            row.pack(fill="x", padx=4, pady=2)

            ctk.CTkLabel(row, text=pac,    width=200, anchor="w",
                         font=(self._tm.font, 12), text_color=self._tm.c("BLACK")).pack(side="left", padx=6)
            ctk.CTkLabel(row, text=fisio,  width=180, anchor="w",
                         font=(self._tm.font, 12), text_color=self._tm.c("BLACK")).pack(side="left")
            ctk.CTkLabel(row, text=data,   width=100, anchor="w",
                         font=(self._tm.font, 12), text_color=self._tm.c("GRAY_DARK")).pack(side="left")
            ctk.CTkLabel(row, text=hora,   width=70,  anchor="w",
                         font=(self._tm.font, 12), text_color=self._tm.c("GRAY_DARK")).pack(side="left")

            sbg, stc = _STATUS_COLORS.get(status, ("#E5E7EB", "#374151"))
            ctk.CTkLabel(row, text=status, width=110,
                         corner_radius=12, fg_color=sbg, text_color=stc,
                         font=(self._tm.font, 11, "bold")).pack(side="left", padx=4)

            # Ações
            acao_frame = ctk.CTkFrame(row, fg_color="transparent")
            acao_frame.pack(side="right", padx=6)

            ctk.CTkButton(
                acao_frame, text="✔", width=32, height=28,
                fg_color=self._tm.c("SUCCESS_BG"),
                hover_color="#bbf7d0",
                text_color=self._tm.c("SUCCESS"),
                font=(self._tm.font, 13, "bold"),
                command=lambda i=cid: self._mudar_status(i, "Confirmada"),
            ).pack(side="left", padx=2)

            ctk.CTkButton(
                acao_frame, text="✘", width=32, height=28,
                fg_color=self._tm.c("RED_LIGHT"),
                hover_color="#fecaca",
                text_color=self._tm.c("RED"),
                font=(self._tm.font, 13, "bold"),
                command=lambda i=cid: self._mudar_status(i, "Cancelada"),
            ).pack(side="left", padx=2)

            ctk.CTkButton(
                acao_frame, text="🗑", width=32, height=28,
                fg_color=self._tm.c("GRAY_LIGHT"),
                hover_color=self._tm.c("GRAY"),
                text_color=self._tm.c("GRAY_DARK"),
                font=(self._tm.font, 13),
                command=lambda i=cid, n=pac: self._excluir(i, n),
            ).pack(side="left", padx=2)

    # ── ações ─────────────────────────────────────────────────────────────────

    def agendar(self):
        pac_str  = self.cb_paciente.get().strip()
        fis_str  = self.cb_fisio.get().strip()
        data     = self.ent_data.get().strip()
        hora     = self.ent_hora.get().strip()
        convenio = self.cb_convenio.get()
        plano    = self.ent_plano.get().strip()
        obs      = self.ent_obs.get().strip()

        erros = []
        if not pac_str or "—" not in pac_str:
            erros.append("• Selecione um paciente.")
        if not fis_str or "—" not in fis_str:
            erros.append("• Selecione um fisioterapeuta.")
        if not data:
            erros.append("• Informe a data da consulta.")
        if not hora:
            erros.append("• Informe o horário.")
        elif not re.match(r"^\d{2}:\d{2}$", hora):
            erros.append("• Horário inválido. Use o formato HH:MM.")

        if erros:
            messagebox.showerror("Campos inválidos", "\n".join(erros))
            return

        try:
            pac_id = int(pac_str.split("—")[0].strip())
            fis_id = int(fis_str.split("—")[0].strip())
        except (ValueError, IndexError):
            messagebox.showerror("Erro", "Seleção inválida de paciente ou fisioterapeuta.")
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cur  = conn.cursor()
            cur.execute("""
                INSERT INTO consultas
                (id_paciente, id_fisioterapeuta, data_consulta, horario,
                 convenio, plano_saude, status, observacao)
                VALUES (?,?,?,?,?,?,'Pendente',?)
            """, (pac_id, fis_id, data, hora, convenio, plano, obs))
            conn.commit()
            self._render_tabela(cur)
            conn.close()
            messagebox.showinfo("Sucesso", "Consulta agendada com sucesso!")
            self._limpar_form()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _mudar_status(self, consulta_id: int, novo_status: str):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur  = conn.cursor()
            cur.execute("UPDATE consultas SET status = ? WHERE id = ?",
                        (novo_status, consulta_id))
            conn.commit()
            self._render_tabela(cur)
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _excluir(self, consulta_id: int, nome_pac: str):
        if not messagebox.askyesno(
            "Confirmar exclusão",
            f"Excluir consulta de '{nome_pac}'?\nEssa ação não pode ser desfeita."
        ):
            return
        try:
            conn = sqlite3.connect(DB_PATH)
            cur  = conn.cursor()
            cur.execute("DELETE FROM consultas WHERE id = ?", (consulta_id,))
            conn.commit()
            self._render_tabela(cur)
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _limpar_form(self):
        self.ent_data.delete(0, "end")
        self.ent_hora.delete(0, "end")
        self.ent_plano.delete(0, "end")
        self.ent_obs.delete(0, "end")
        self.cb_paciente.set("")
        self.cb_fisio.set("")

    # ── calendário ────────────────────────────────────────────────────────────

    def pop_calendario(self, entry):
        self._calendar_target = entry
        self.pop = ctk.CTkToplevel(self)
        self.pop.geometry("380x280")
        self.pop.grab_set()
        self.cal = Calendar(self.pop, date_pattern="dd/mm/yyyy")
        self.cal.pack()
        ctk.CTkButton(self.pop, text="Confirmar", command=self._get_data).pack(pady=4)

    def _get_data(self):
        self._calendar_target.delete(0, "end")
        self._calendar_target.insert("end", self.cal.get_date())
        self.pop.destroy()