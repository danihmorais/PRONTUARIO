import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from tkcalendar import Calendar
from theme_manager import ThemeManager
from config import DB_PATH


class AppointmentWindow(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self._tm = ThemeManager.get()
        self._calendar_target = None

        # 👇 tema reativo
        self._tm.subscribe(self._apply_theme)

        self._build_ui()
        self.carregar_dados()

    # =========================
    # UI
    # =========================
    def _build_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))

        self.title = ctk.CTkLabel(
            header,
            text="Agendamento de Consultas",
            font=(self._tm.font, 24, "bold"),
            text_color=self._tm.c("BLACK"),
        )
        self.title.pack(anchor="w")

        self.subtitle = ctk.CTkLabel(
            header,
            text="Agende e gerencie as sessões de fisioterapia",
            font=(self._tm.font, 13),
            text_color=self._tm.c("GRAY"),
        )
        self.subtitle.pack(anchor="w", pady=(4, 0))

        self.container = ctk.CTkScrollableFrame(
            self,
            fg_color=self._tm.c("WHITE"),
            corner_radius=10,
            border_color=self._tm.c("GRAY_LIGHT"),
            border_width=1,
        )
        self.container.pack(fill="both", expand=True)

        # ================= FORM =================
        form_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        form_frame.pack(fill="x", padx=20, pady=20)

        form_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.cb_paciente = self._combo(form_frame, "Paciente *", 0, 0, [], 2)
        self.cb_fisio = self._combo(form_frame, "Fisioterapeuta *", 0, 2, [], 2)

        self.ent_data = self._field(form_frame, "Data da Consulta *", 1, 0, calendar=True)
        self.ent_hora = self._field(form_frame, "Horário *", 1, 1)
        self.cb_convenio = self._combo(
            form_frame, "Convênio", 1, 2,
            ["Particular", "Plano de Saúde", "SUS"], 1
        )
        self.ent_plano = self._field(form_frame, "Nome do Plano", 1, 3)

        self.ent_obs = ctk.CTkEntry(
            form_frame,
            placeholder_text="Observações adicionais",
            height=36,
        )
        self.ent_obs.grid(row=5, column=0, columnspan=4, sticky="ew", padx=10, pady=(15, 0))

        # ================= BOTÕES =================
        btn_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(
            btn_frame,
            text="Agendar Consulta",
            height=40,
            command=self.agendar,
        ).pack(side="right")

        ctk.CTkButton(
            btn_frame,
            text="Atualizar Listas",
            height=40,
            command=self.carregar_dados,
        ).pack(side="right", padx=10)

        # ================= LISTA =================
        list_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        list_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            list_frame,
            text="Consultas Agendadas",
            font=(self._tm.font, 16, "bold"),
            text_color=self._tm.c("BLACK"),
        ).pack(anchor="w", pady=(0, 10))

        self.tabela_consultas = ctk.CTkScrollableFrame(
            list_frame,
            fg_color=self._tm.c("GRAY_BG"),
            corner_radius=8,
        )
        self.tabela_consultas.pack(fill="both", expand=True)

    # =========================
    # COMPONENTES
    # =========================
    def _field(self, parent, label, row, col, colspan=1, calendar=False):
        ctk.CTkLabel(
            parent,
            text=label,
            font=(self._tm.font, 12, "bold"),
            text_color=self._tm.c("GRAY_DARK"),
        ).grid(row=row * 2, column=col, sticky="w", padx=10)

        entry = ctk.CTkEntry(parent, height=36)
        entry.grid(
            row=row * 2 + 1,
            column=col,
            columnspan=colspan,
            sticky="ew",
            padx=10,
            pady=(0, 15),
        )

        if calendar:
            btn = ctk.CTkButton(
                parent,
                text="📅",
                width=36,
                height=36,
                command=lambda: self.pop_calendario(entry),
            )
            btn.grid(row=row * 2 + 1, column=col + colspan - 1, sticky="e", padx=10)

        return entry

    def _combo(self, parent, label, row, col, values, colspan=1):
        ctk.CTkLabel(
            parent,
            text=label,
            font=(self._tm.font, 12, "bold"),
            text_color=self._tm.c("GRAY_DARK"),
        ).grid(row=row * 2, column=col, sticky="w", padx=10)

        combo = ctk.CTkComboBox(
            parent,
            values=values,
            fg_color=self._tm.c("GRAY_BG"),
            border_color=self._tm.c("GRAY_LIGHT"),
            dropdown_fg_color=self._tm.c("WHITE"),
            dropdown_text_color=self._tm.c("BLACK"),
            button_color=self._tm.c("BLUE"),
            button_hover_color=self._tm.c("DARK_BLUE"),
        )

        combo.grid(
            row=row * 2 + 1,
            column=col,
            columnspan=colspan,
            sticky="ew",
            padx=10,
            pady=(0, 15),
        )

        combo.set("")  # <- ESSENCIAL

        return combo

    # =========================
    # TEMA REATIVO
    # =========================
    def _apply_theme(self, colors):
        self.configure(fg_color="transparent")

        self.container.configure(
            fg_color=colors["WHITE"],
            border_color=colors["GRAY_LIGHT"],
        )

        self.tabela_consultas.configure(
            fg_color=colors["GRAY_BG"]
        )

        for cb in [self.cb_paciente, self.cb_fisio, self.cb_convenio]:
            cb.configure(
                fg_color=colors["GRAY_BG"],
                text_color=colors["BLACK"],
                border_color=colors["GRAY_LIGHT"],
                dropdown_fg_color=colors["WHITE"],
                dropdown_text_color=colors["BLACK"],
                button_color=colors["BLUE"],
                button_hover_color=colors["DARK_BLUE"],
            )

        for ent in [self.ent_data, self.ent_hora, self.ent_plano, self.ent_obs]:
            ent.configure(
                fg_color=colors["GRAY_BG"],
                text_color=colors["BLACK"],
                border_color=colors["GRAY_LIGHT"],
            )

    # =========================
    # DADOS
    # =========================
    def carregar_dados(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT id, nome, cpf FROM pacientes ORDER BY nome")
            self.pacientes_list = cursor.fetchall()
            self.cb_paciente.configure(
                values=[f"{p[0]} - {p[1]}" for p in self.pacientes_list]
            )

            cursor.execute("SELECT id, nome, crefito FROM fisioterapeutas ORDER BY nome")
            self.fisios_list = cursor.fetchall()
            self.cb_fisio.configure(
                values=[f"{f[0]} - {f[1]}" for f in self.fisios_list]
            )

            self.atualizar_tabela(cursor)
            conn.close()

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # =========================
    # TABELA
    # =========================
    def atualizar_tabela(self, cursor):
        for w in self.tabela_consultas.winfo_children():
            w.destroy()

        cursor.execute("""
            SELECT c.id, p.nome, f.nome, c.data_consulta, c.horario, c.status
            FROM consultas c
            JOIN pacientes p ON c.id_paciente = p.id
            JOIN fisioterapeutas f ON c.id_fisioterapeuta = f.id
            ORDER BY c.data_consulta DESC, c.horario DESC
        """)

        for c in cursor.fetchall():
            row = ctk.CTkFrame(self.tabela_consultas, fg_color="transparent")
            row.pack(fill="x", padx=6, pady=2)

            ctk.CTkLabel(row, text=c[1], width=200).grid(row=0, column=0)
            ctk.CTkLabel(row, text=c[2], width=200).grid(row=0, column=1)
            ctk.CTkLabel(row, text=c[3], width=120).grid(row=0, column=2)
            ctk.CTkLabel(row, text=c[4], width=80).grid(row=0, column=3)
            ctk.CTkLabel(row, text=c[5], width=100).grid(row=0, column=4)

    # =========================
    # AÇÕES
    # =========================
    def agendar(self):
        try:
            pac = int(self.cb_paciente.get().split(" - ")[0])
            fis = int(self.cb_fisio.get().split(" - ")[0])

            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO consultas
                (id_paciente, id_fisioterapeuta, data_consulta, horario, status)
                VALUES (?, ?, ?, ?, 'Pendente')
            """, (
                pac,
                fis,
                self.ent_data.get(),
                self.ent_hora.get(),
            ))

            conn.commit()
            conn.close()

            self.carregar_dados()

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # =========================
    # CALENDÁRIO
    # =========================
    def pop_calendario(self, entry):
        self._calendar_target = entry

        self.pop = ctk.CTkToplevel(self)
        self.pop.geometry("380x280")
        self.pop.grab_set()

        self.cal = Calendar(self.pop, date_pattern="dd/mm/yyyy")
        self.cal.pack()

        ctk.CTkButton(
            self.pop,
            text="Confirmar",
            command=self.get_data,
        ).pack()

    def get_data(self):
        self._calendar_target.delete(0, "end")
        self._calendar_target.insert("end", self.cal.get_date())
        self.pop.destroy()