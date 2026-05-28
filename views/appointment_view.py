import re
import sqlite3
import customtkinter as ctk
from tkinter import messagebox

from theme_manager import ThemeManager
from config import DB_PATH
from views.components.calendar import CalendarPopup
from views.components.appointments import Appointments

_STATUS_THEME_MAP = {
    "Confirmada": ("SUCCESS_BG", "SUCCESS"),
    "Pendente": ("WARN_BG", "WARN"),
    "Cancelada": ("RED_LIGHT", "RED"),
    "Realizada": ("PURPLE_BG", "PURPLE"),
}

class AppointmentView(ctk.CTkFrame):

    def __init__(self, parent, controller=None):
        super().__init__(parent, fg_color="transparent")

        self.controller = controller
        self._tm = ThemeManager.get()

        self._selected_consulta_id = None
        self._themed_widgets = []

        self._tm.subscribe(self._apply_theme)

        self.calendar_popup = CalendarPopup(self, self._tm)

        self._build_ui()
        self.carregar_dados()

    def _tw(self, widget, **color_keys):
        self._themed_widgets.append({
            "widget": widget,
            "keys": color_keys
        })

    def _apply_theme(self, colors):
        alive = []

        for entry in self._themed_widgets:
            widget = entry["widget"]
            keys = entry["keys"]

            try:
                if widget.winfo_exists():
                    widget.configure(**{
                        param: colors[color_key]
                        for param, color_key in keys.items()
                    })

                    alive.append(entry)

            except Exception:
                pass

        self._themed_widgets = alive

    def _build_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))

        self.title_lbl = ctk.CTkLabel(
            header,
            text="Agendamento de Consultas",
            font=(self._tm.font, 24, "bold"),
            text_color=self._tm.c("BLACK"),
        )
        self.title_lbl.pack(anchor="w")
        self._tw(self.title_lbl, text_color="BLACK")

        self.subtitle_lbl = ctk.CTkLabel(
            header,
            text="Agende e gerencie as sessões de fisioterapia",
            font=(self._tm.font, 13),
            text_color=self._tm.c("GRAY"),
        )
        self.subtitle_lbl.pack(anchor="w", pady=(4, 0))
        self._tw(self.subtitle_lbl, text_color="GRAY")

        self.container = ctk.CTkScrollableFrame(
            self,
            fg_color=self._tm.c("WHITE"),
            corner_radius=10,
            border_color=self._tm.c("GRAY_LIGHT"),
            border_width=1,
        )
        self.container.pack(fill="both", expand=True)
        self.container._scrollbar.grid_configure(padx=(0, 6))
        self._tw(
            self.container,
            fg_color="WHITE",
            border_color="GRAY_LIGHT"
        )

        self._build_form()
        self._build_lista()

    def _lbl(self, parent, text, row, col):
        lbl = ctk.CTkLabel(
            parent,
            text=text,
            font=(self._tm.font, 12, "bold"),
            text_color=self._tm.c("GRAY_DARK"),
        )

        lbl.grid(
            row=row,
            column=col,
            sticky="w",
        )

        self._tw(lbl, text_color="GRAY_DARK")

    def _entry(self, parent, **kwargs):
        ent = ctk.CTkEntry(
            parent,
            height=36,
            fg_color=self._tm.c("WHITE"),
            border_color=self._tm.c("GRAY_LIGHT"),
            text_color=self._tm.c("BLACK"),
            placeholder_text_color=self._tm.c("GRAY"),
            **kwargs
        )

        self._tw(
            ent,
            fg_color="WHITE",
            border_color="GRAY_LIGHT",
            text_color="BLACK",
            placeholder_text_color="GRAY"
        )

        return ent

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

        cb.grid(
            row=row,
            column=col,
            columnspan=colspan,
            sticky="ew",
            pady=(0, 12)
        )

        self._tw(
            cb,
            fg_color="GRAY_BG",
            border_color="GRAY_LIGHT",
            dropdown_fg_color="WHITE",
            dropdown_text_color="BLACK",
            button_color="BLUE",
            button_hover_color="DARK_BLUE",
            text_color="BLACK",
        )

        if values:
            cb.set(values[0])
        else:
            cb.set("")

        return cb

    def _build_form(self):
        form = ctk.CTkFrame(self.container, fg_color="transparent")
        form.pack(fill="x", padx=10, pady=20)

        form.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self._lbl(form, "Paciente *", 0, 0)
        self.cb_paciente = self._combo_raw(form, 1, 0, 2)

        self._lbl(form, "Fisioterapeuta *", 0, 2)
        self.cb_fisio = self._combo_raw(form, 1, 2, 2)

        self._lbl(form, "Data *", 2, 0)

        self.ent_data = self._entry(form)
        self.ent_data.grid(
            row=3,
            column=0,
            sticky="ew",
            pady=(0, 12)
        )

        btn_calendar = ctk.CTkButton(
            form,
            text="📅",
            width=36,
            height=36,
            fg_color=self._tm.c("BLUE"),
            hover_color=self._tm.c("DARK_BLUE"),
            text_color=self._tm.c("TOPBAR_TEXT"),
            command=lambda: self.calendar_popup.open(self.ent_data)
        )

        btn_calendar.grid(
            row=3,
            column=0,
            sticky="e",
            padx=0,
            pady=(0, 12)
        )

        self._tw(
            btn_calendar,
            fg_color="BLUE",
            hover_color="DARK_BLUE",
            text_color="TOPBAR_TEXT"
        )

        self._lbl(form, "Horário * (HH:MM)", 2, 1)

        self.ent_hora = self._entry(
            form,
            placeholder_text="08:00"
        )

        self.ent_hora.grid(
            row=3,
            column=1,
            sticky="ew",
            padx=10,
            pady=(0, 12)
        )

        self._lbl(form, "Convênio", 2, 2)

        self.cb_convenio = self._combo_raw(
            form,
            3,
            2,
            1,
            values=[
                "Particular",
                "Plano de Saúde",
                "SUS"
            ]
        )

        self._lbl(form, "Nome do Plano", 2, 3)

        self.ent_plano = self._entry(form)

        self.ent_plano.grid(
            row=3,
            column=3,
            sticky="ew",
            pady=(0, 12)
        )

        self._lbl(form, "Observações", 4, 0)

        self.ent_obs = self._entry(
            form,
            placeholder_text="Observações adicionais"
        )

        self.ent_obs.grid(
            row=5,
            column=0,
            columnspan=4,
            sticky="ew",
            pady=(0, 12)
        )

        btn_frame = ctk.CTkFrame(
            self.container,
            fg_color="transparent"
        )

        btn_frame.pack(
            fill="x",
            pady=(0, 10)
        )

        btn_agendar = ctk.CTkButton(
            btn_frame,
            text="✅  Agendar Consulta",
            height=40,
            fg_color=self._tm.c("BLUE"),
            hover_color=self._tm.c("DARK_BLUE"),
            text_color=self._tm.c("TOPBAR_TEXT"),
            font=(self._tm.font, 13, "bold"),
            command=self.agendar,
        )

        btn_agendar.pack(side="right", padx=10)

        self._tw(
            btn_agendar,
            fg_color="BLUE",
            hover_color="DARK_BLUE",
            text_color="TOPBAR_TEXT"
        )

        btn_refresh = ctk.CTkButton(
            btn_frame,
            text="🔄  Atualizar",
            height=40,
            fg_color=self._tm.c("BLUE_XL"),
            hover_color=self._tm.c("GRAY_LIGHT"),
            text_color=self._tm.c("BLUE"),
            font=(self._tm.font, 13, "bold"),
            command=self.carregar_dados,
        )

        btn_refresh.pack(side="right", padx=10)

        self._tw(
            btn_refresh,
            fg_color="BLUE_XL",
            hover_color="GRAY_LIGHT",
            text_color="BLUE"
        )

    def _build_lista(self):
        lf = ctk.CTkFrame(
            self.container,
            fg_color="transparent"
        )

        lf.pack(
            fill="x",
            padx=10,
            pady=(10, 0)
        )

        lbl_title = ctk.CTkLabel(
            lf,
            text="Consultas Agendadas",
            font=(self._tm.font, 16, "bold"),
            text_color=self._tm.c("BLACK"), 
        )

        lbl_title.pack(side="left")

        self._tw(lbl_title, text_color="BLACK")

        right_box = ctk.CTkFrame(lf, fg_color="transparent")
        right_box.pack(side="right", padx=(0, 5))
        lbl_filter = ctk.CTkLabel(
            right_box,
            text="Filtrar:",
            text_color=self._tm.c("GRAY"),
            font=(self._tm.font, 12)
        )
        right_box.pack(side="right", padx=(0, 0))

        self.cb_filtro = ctk.CTkComboBox(
            right_box,
            values=[
                "Todas",
                "Pendente",
                "Confirmada",
                "Cancelada",
                "Realizada"
            ],
            width=160,
            height=32,
            fg_color=self._tm.c("GRAY_BG"),
            border_color=self._tm.c("GRAY_LIGHT"),
            dropdown_fg_color=self._tm.c("WHITE"),
            dropdown_text_color=self._tm.c("BLACK"),
            button_color=self._tm.c("BLUE"),
            button_hover_color=self._tm.c("DARK_BLUE"),
            text_color=self._tm.c("BLACK"),
            command=lambda _: self.carregar_dados()
        )

        self.cb_filtro.set("Todas")
        self.cb_filtro.pack(side="left", padx = (0, 0))

        self._tw(lbl_filter, text_color="GRAY")

        self.appointments = Appointments(
            self.container,
            self._tm,
            data=[],
            on_confirm=self._mudar_status_confirmar,
            on_cancel=self._mudar_status_cancelar,
            on_delete=self._excluir
        )

        self.appointments.pack(fill="x", padx=10, pady=(10, 10))

    def carregar_dados(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()

            # pacientes
            cur.execute("SELECT id, nome FROM pacientes ORDER BY nome")
            self.pacientes_list = cur.fetchall()

            self.cb_paciente.configure(
                values=[f"{p[0]} — {p[1]}" for p in self.pacientes_list]
            )

            # fisioterapeutas
            cur.execute("SELECT id, nome FROM fisioterapeutas ORDER BY nome")
            self.fisios_list = cur.fetchall()

            self.cb_fisio.configure(
                values=[f"{f[0]} — {f[1]}" for f in self.fisios_list]
            )

            # CONSULTAS (FALTAVA ISSO)
            cur.execute("""
                SELECT c.id, p.nome, f.nome,
                    c.data_consulta, c.horario, c.status
                FROM consultas c
                JOIN pacientes p ON c.id_paciente = p.id
                JOIN fisioterapeutas f ON c.id_fisioterapeuta = f.id
                ORDER BY c.data_consulta DESC, c.horario DESC
            """)

            rows = cur.fetchall()
            self.appointments.update_data(rows)

            conn.close()

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def agendar(self):
        pac_str = self.cb_paciente.get().strip()
        fis_str = self.cb_fisio.get().strip()
        data = self.ent_data.get().strip()
        hora = self.ent_hora.get().strip()
        convenio = self.cb_convenio.get()
        plano = self.ent_plano.get().strip()
        obs = self.ent_obs.get().strip()

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
            messagebox.showerror(
                "Campos inválidos",
                "\n".join(erros)
            )

            return

        try:
            pac_id = int(
                pac_str.split("—")[0].strip()
            )

            fis_id = int(
                fis_str.split("—")[0].strip()
            )

        except (ValueError, IndexError):
            messagebox.showerror(
                "Erro",
                "Seleção inválida de paciente ou fisioterapeuta."
            )

            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO consultas
                (
                    id_paciente,
                    id_fisioterapeuta,
                    data_consulta,
                    horario,
                    convenio,
                    plano_saude,
                    status,
                    observacao
                )
                VALUES
                (
                    ?, ?, ?, ?, ?, ?, 'Pendente', ?
                )
            """, (
                pac_id,
                fis_id,
                data,
                hora,
                convenio,
                plano,
                obs
            ))

            conn.commit()

            self.carregar_dados()

            conn.close()

            messagebox.showinfo(
                "Sucesso",
                "Consulta agendada com sucesso!"
            )

            self._limpar_form()

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _mudar_status(self, consulta_id, novo_status):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()

            cur.execute(
                "UPDATE consultas SET status = ? WHERE id = ?",
                (novo_status, consulta_id)
            )

            conn.commit()

            self.carregar_dados()

            conn.close()

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _excluir(self, consulta_id, nome_pac):
        if not messagebox.askyesno(
            "Confirmar exclusão",
            f"Excluir consulta de '{nome_pac}'?\nEssa ação não pode ser desfeita."
        ):
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()

            cur.execute(
                "DELETE FROM consultas WHERE id = ?",
                (consulta_id,)
            )

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
    
    def _mudar_status_confirmar(self, cid):
        self._mudar_status(cid, "Confirmada")

    def _mudar_status_cancelar(self, cid):
        self._mudar_status(cid, "Cancelada")