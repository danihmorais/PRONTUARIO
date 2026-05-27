import re
import sqlite3
import customtkinter as ctk
from tkinter import messagebox

from theme_manager import ThemeManager
from config import DB_PATH
from views.components.calendar import CalendarPopup

_STATUS_THEME_MAP = {
    "Confirmada": ("SUCCESS_BG", "SUCCESS"),
    "Pendente": ("WARN_BG", "WARN"),
    "Cancelada": ("RED_LIGHT", "RED"),
    "Realizada": ("PURPLE_BG", "PURPLE"),
}


def _get_status_colors(self, status):
    bg_key, text_key = _STATUS_THEME_MAP.get(
        status,
        ("GRAY_LIGHT", "GRAY_DARK")
    )

    return self._tm.c(bg_key), self._tm.c(text_key)


class AppointmentWindow(ctk.CTkFrame):

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
            padx=10
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
            padx=10,
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
        form.pack(fill="x", padx=20, pady=20)

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
            padx=10,
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
            padx=10,
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
            padx=10,
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
            padx=10,
            pady=(0, 12)
        )

        btn_frame = ctk.CTkFrame(
            self.container,
            fg_color="transparent"
        )

        btn_frame.pack(
            fill="x",
            padx=20,
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

        btn_agendar.pack(side="right")

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
            padx=20,
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

        self.cb_filtro = ctk.CTkComboBox(
            lf,
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
        self.cb_filtro.pack(side="right")

        self._tw(
            self.cb_filtro,
            fg_color="GRAY_BG",
            border_color="GRAY_LIGHT",
            dropdown_fg_color="WHITE",
            dropdown_text_color="BLACK",
            button_color="BLUE",
            button_hover_color="DARK_BLUE",
            text_color="BLACK"
        )

        lbl_filter = ctk.CTkLabel(
            lf,
            text="Filtrar:",
            text_color=self._tm.c("GRAY"),
            font=(self._tm.font, 12)
        )

        lbl_filter.pack(side="right", padx=(0, 4))

        self._tw(lbl_filter, text_color="GRAY")

        hdr = ctk.CTkFrame(
            self.container,
            fg_color=self._tm.c("BLUE_XL"),
            corner_radius=6
        )

        hdr.pack(fill="x", padx=20, pady=(8, 2))

        self._tw(hdr, fg_color="BLUE_XL")

        for txt, w in [
            ("Paciente", 200),
            ("Fisioterapeuta", 180),
            ("Data", 100),
            ("Hora", 70),
            ("Status", 110),
            ("Ações", 140)
        ]:
            lbl = ctk.CTkLabel(
                hdr,
                text=txt,
                width=w,
                anchor="w",
                font=(self._tm.font, 12, "bold"),
                text_color=self._tm.c("DARK_BLUE")
            )

            lbl.pack(side="left", padx=6, pady=6)

            self._tw(lbl, text_color="DARK_BLUE")

        self.tabela_consultas = ctk.CTkScrollableFrame(
            self.container,
            fg_color=self._tm.c("GRAY_BG"),
            corner_radius=8,
            height=280,
        )

        self.tabela_consultas.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        self._tw(
            self.tabela_consultas,
            fg_color="GRAY_BG"
        )

    def carregar_dados(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()

            cur.execute(
                "SELECT id, nome FROM pacientes ORDER BY nome"
            )

            self.pacientes_list = cur.fetchall()

            self.cb_paciente.configure(
                values=[
                    f"{p[0]} — {p[1]}"
                    for p in self.pacientes_list
                ]
            )

            cur.execute(
                "SELECT id, nome FROM fisioterapeutas ORDER BY nome"
            )

            self.fisios_list = cur.fetchall()

            self.cb_fisio.configure(
                values=[
                    f"{f[0]} — {f[1]}"
                    for f in self.fisios_list
                ]
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
            SELECT c.id, p.nome, f.nome,
                   c.data_consulta, c.horario, c.status
            FROM consultas c
            JOIN pacientes p
                ON c.id_paciente = p.id
            JOIN fisioterapeutas f
                ON c.id_fisioterapeuta = f.id
        """

        params = ()

        if filtro != "Todas":
            query += " WHERE c.status = ?"
            params = (filtro,)

        query += """
            ORDER BY
                c.data_consulta DESC,
                c.horario DESC
        """

        cursor.execute(query, params)

        rows = cursor.fetchall()

        if not rows:
            lbl_empty = ctk.CTkLabel(
                self.tabela_consultas,
                text="Nenhuma consulta encontrada.",
                font=(self._tm.font, 13),
                text_color=self._tm.c("GRAY"),
            )

            lbl_empty.pack(pady=20)

            self._tw(lbl_empty, text_color="GRAY")

            return

        for idx, (cid, pac, fisio, data, hora, status) in enumerate(rows):
            bg_key = "WHITE" if idx % 2 == 0 else "GRAY_BG"

            row = ctk.CTkFrame(
                self.tabela_consultas,
                fg_color=self._tm.c(bg_key),
                corner_radius=4
            )

            row.pack(fill="x", padx=4, pady=2)

            self._tw(row, fg_color=bg_key)

            lbl_p = ctk.CTkLabel(
                row,
                text=pac,
                width=200,
                anchor="w",
                font=(self._tm.font, 12),
                text_color=self._tm.c("BLACK")
            )

            lbl_p.pack(side="left", padx=6)

            self._tw(lbl_p, text_color="BLACK")

            lbl_f = ctk.CTkLabel(
                row,
                text=fisio,
                width=180,
                anchor="w",
                font=(self._tm.font, 12),
                text_color=self._tm.c("BLACK")
            )

            lbl_f.pack(side="left")

            self._tw(lbl_f, text_color="BLACK")

            lbl_d = ctk.CTkLabel(
                row,
                text=data,
                width=100,
                anchor="w",
                font=(self._tm.font, 12),
                text_color=self._tm.c("GRAY_DARK")
            )

            lbl_d.pack(side="left")

            self._tw(lbl_d, text_color="GRAY_DARK")

            lbl_h = ctk.CTkLabel(
                row,
                text=hora,
                width=70,
                anchor="w",
                font=(self._tm.font, 12),
                text_color=self._tm.c("GRAY_DARK")
            )

            lbl_h.pack(side="left")

            self._tw(lbl_h, text_color="GRAY_DARK")

            sbg_key, stc_key = _STATUS_THEME_MAP.get(
                status,
                ("GRAY_LIGHT", "GRAY_DARK")
            )

            lbl_status = ctk.CTkLabel(
                row,
                text=status,
                width=110,
                corner_radius=12,
                fg_color=self._tm.c(sbg_key),
                text_color=self._tm.c(stc_key),
                font=(self._tm.font, 11, "bold")
            )

            lbl_status.pack(side="left", padx=4)

            self._tw(
                lbl_status,
                fg_color=sbg_key,
                text_color=stc_key
            )

            acao_frame = ctk.CTkFrame(
                row,
                fg_color="transparent"
            )

            acao_frame.pack(side="right", padx=6)

            btn_ok = ctk.CTkButton(
                acao_frame,
                text="✔",
                width=32,
                height=28,
                fg_color=self._tm.c("SUCCESS_BG"),
                hover_color=self._tm.c("SUCCESS_BG"),
                text_color=self._tm.c("SUCCESS"),
                font=(self._tm.font, 13, "bold"),
                command=lambda i=cid: self._mudar_status(i, "Confirmada"),
            )

            btn_ok.pack(side="left", padx=2)

            self._tw(
                btn_ok,
                fg_color="SUCCESS_BG",
                hover_color="SUCCESS_BG",
                text_color="SUCCESS"
            )

            btn_cancel = ctk.CTkButton(
                acao_frame,
                text="✘",
                width=32,
                height=28,
                fg_color=self._tm.c("RED_LIGHT"),
                hover_color=self._tm.c("RED_LIGHT"),
                text_color=self._tm.c("RED"),
                font=(self._tm.font, 13, "bold"),
                command=lambda i=cid: self._mudar_status(i, "Cancelada"),
            )

            btn_cancel.pack(side="left", padx=2)

            self._tw(
                btn_cancel,
                fg_color="RED_LIGHT",
                hover_color="RED_LIGHT",
                text_color="RED"
            )

            btn_delete = ctk.CTkButton(
                acao_frame,
                text="🗑",
                width=32,
                height=28,
                fg_color=self._tm.c("GRAY_LIGHT"),
                hover_color=self._tm.c("GRAY"),
                text_color=self._tm.c("GRAY_DARK"),
                font=(self._tm.font, 13),
                command=lambda i=cid, n=pac: self._excluir(i, n),
            )

            btn_delete.pack(side="left", padx=2)

            self._tw(
                btn_delete,
                fg_color="GRAY_LIGHT",
                hover_color="GRAY",
                text_color="GRAY_DARK"
            )

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

            self._render_tabela(cur)

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

            self._render_tabela(cur)

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