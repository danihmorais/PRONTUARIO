import re
import sqlite3
import customtkinter as ctk
from tkinter import messagebox
from theme_manager import ThemeManager
from config import DB_PATH


def _only_digits(s):
    return re.sub(r"\D", "", str(s))


class SearchDoctorView(ctk.CTkFrame):

    _COLS_FISIO = {
        "headers": ["ID", "Nome", "CREFITO", "Especialidade", "Celular"],
        "widths": [40, 220, 110, 160, 120],
    }

    _COLS_FUNC = {
        "headers": ["ID", "Nome", "Cargo", "CPF", "Celular"],
        "widths": [40, 220, 160, 130, 120],
    }

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self._tm = ThemeManager.get()

        self._rows = []
        self._row_frames = []
        self._selected_row = None
        self._themed_widgets = []

        self._tm.subscribe(self._on_theme_change)

        self._build_ui()
        self.buscar()

    def _tw(self, widget, **keys):
        self._themed_widgets.append({
            "widget": widget,
            "keys": keys
        })

    def _apply_theme_widgets(self, colors):
        alive = []

        for item in self._themed_widgets:
            widget = item["widget"]
            keys = item["keys"]

            try:
                if widget.winfo_exists():
                    alive.append(item)

                    cfg = {}

                    for param, color_key in keys.items():
                        if color_key in colors:
                            cfg[param] = colors[color_key]

                    if cfg:
                        widget.configure(**cfg)

            except Exception:
                pass

        self._themed_widgets = alive

    def _build_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))

        title = ctk.CTkLabel(
            header,
            text="Equipe Clínica e Funcionários",
            font=(self._tm.font, 24, "bold"),
            text_color=self._tm.c("BLACK"),
        )

        title.pack(anchor="w")

        self._tw(title, text_color="BLACK")

        subtitle = ctk.CTkLabel(
            header,
            text="Consulte, edite e remova fisioterapeutas e funcionários",
            font=(self._tm.font, 13),
            text_color=self._tm.c("GRAY"),
        )

        subtitle.pack(anchor="w", pady=(4, 0))

        self._tw(subtitle, text_color="GRAY")

        self.search_fr = ctk.CTkFrame(
            self,
            fg_color=self._tm.c("WHITE"),
            corner_radius=10,
            border_color=self._tm.c("GRAY_LIGHT"),
            border_width=1,
        )

        self.search_fr.pack(fill="x", pady=(0, 16))

        self._tw(
            self.search_fr,
            fg_color="WHITE",
            border_color="GRAY_LIGHT"
        )

        self.search_fr.grid_columnconfigure(1, weight=1)

        lbl_busca = ctk.CTkLabel(
            self.search_fr,
            text="Buscar:",
            text_color=self._tm.c("BLACK"),
            font=(self._tm.font, 13),
        )

        lbl_busca.grid(
            row=0,
            column=0,
            padx=(16, 10),
            pady=14
        )

        self._tw(lbl_busca, text_color="BLACK")

        self.ent_busca = ctk.CTkEntry(
            self.search_fr,
            placeholder_text="Nome, CPF, cargo ou especialidade...",
            fg_color=self._tm.c("GRAY_BG"),
            border_color=self._tm.c("GRAY_LIGHT"),
            text_color=self._tm.c("BLACK"),
            placeholder_text_color=self._tm.c("GRAY"),
            height=36,
        )

        self.ent_busca.grid(
            row=0,
            column=1,
            sticky="ew",
            pady=14
        )

        self._tw(
            self.ent_busca,
            fg_color="GRAY_BG",
            border_color="GRAY_LIGHT",
            text_color="BLACK",
            placeholder_text_color="GRAY"
        )

        self.ent_busca.bind("<Return>", lambda _: self.buscar())
        self.ent_busca.bind("<KeyRelease>", lambda _: self.buscar())

        self.cb_tipo = ctk.CTkComboBox(
            self.search_fr,
            values=["Fisioterapeutas", "Funcionários"],
            fg_color=self._tm.c("GRAY_BG"),
            border_color=self._tm.c("GRAY_LIGHT"),
            text_color=self._tm.c("BLACK"),
            button_color=self._tm.c("BLUE"),
            button_hover_color=self._tm.c("DARK_BLUE"),
            dropdown_fg_color=self._tm.c("WHITE"),
            dropdown_text_color=self._tm.c("BLACK"),
            width=180,
            height=36,
            command=lambda _: self.buscar(),
        )

        self.cb_tipo.grid(
            row=0,
            column=2,
            padx=12,
            pady=14
        )

        self.cb_tipo.set("Fisioterapeutas")

        self._tw(
            self.cb_tipo,
            fg_color="GRAY_BG",
            border_color="GRAY_LIGHT",
            text_color="BLACK",
            button_color="BLUE",
            button_hover_color="DARK_BLUE",
            dropdown_fg_color="WHITE",
            dropdown_text_color="BLACK"
        )

        self.bt_busca = ctk.CTkButton(
            self.search_fr,
            text="Pesquisar",
            height=36,
            width=120,
            fg_color=self._tm.c("BLUE"),
            hover_color=self._tm.c("DARK_BLUE"),
            text_color=self._tm.c("TOPBAR_TEXT"),
            font=(self._tm.font, 13, "bold"),
            command=self.buscar,
        )

        self.bt_busca.grid(
            row=0,
            column=3,
            padx=(0, 16),
            pady=14
        )

        self._tw(
            self.bt_busca,
            fg_color="BLUE",
            hover_color="DARK_BLUE",
            text_color="TOPBAR_TEXT"
        )

        self._table_outer = ctk.CTkFrame(
            self,
            fg_color=self._tm.c("WHITE"),
            corner_radius=10,
            border_color=self._tm.c("GRAY_LIGHT"),
            border_width=1,
        )

        self._table_outer.pack(fill="both", expand=True)

        self._tw(
            self._table_outer,
            fg_color="WHITE",
            border_color="GRAY_LIGHT"
        )

        self._table_outer.grid_rowconfigure(1, weight=1)
        self._table_outer.grid_columnconfigure(0, weight=1)

        self._hdr_frame = ctk.CTkFrame(
            self._table_outer,
            fg_color=self._tm.c("BLUE_XL"),
            corner_radius=0,
            height=38,
        )

        self._hdr_frame.grid(row=0, column=0, sticky="ew")

        self._tw(self._hdr_frame, fg_color="BLUE_XL")

        self._scroll = ctk.CTkScrollableFrame(
            self._table_outer,
            fg_color=self._tm.c("WHITE"),
            corner_radius=0,
        )

        self._scroll.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(0, 6)
        )

        try:
            self._scroll._scrollbar.grid_configure(
                padx=(0, 6)
            )
        except Exception:
            pass

        self._tw(
            self._scroll,
            fg_color="WHITE",
        )

        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.pack(fill="x", pady=(12, 0))

        self.lbl_count = ctk.CTkLabel(
            footer,
            text="",
            font=(self._tm.font, 12),
            text_color=self._tm.c("GRAY"),
        )

        self.lbl_count.pack(side="left")

        self._tw(self.lbl_count, text_color="GRAY")

        self.lbl_sel = ctk.CTkLabel(
            footer,
            text="",
            font=(self._tm.font, 12),
            text_color=self._tm.c("BLUE"),
        )

        self.lbl_sel.pack(side="left", padx=(20, 0))

        self._tw(self.lbl_sel, text_color="BLUE")

        btn_excluir = ctk.CTkButton(
            footer,
            text="🗑  Excluir",
            height=38,
            width=130,
            fg_color=self._tm.c("RED_LIGHT"),
            hover_color=self._tm.c("RED"),
            text_color=self._tm.c("RED"),
            font=(self._tm.font, 13, "bold"),
            command=self._excluir,
        )

        btn_excluir.pack(side="right")

        self._tw(
            btn_excluir,
            fg_color="RED_LIGHT",
            hover_color="RED",
            text_color="RED"
        )

        btn_editar = ctk.CTkButton(
            footer,
            text="✏  Editar",
            height=38,
            width=130,
            fg_color=self._tm.c("BLUE"),
            hover_color=self._tm.c("DARK_BLUE"),
            text_color=self._tm.c("TOPBAR_TEXT"),
            font=(self._tm.font, 13, "bold"),
            command=self._editar,
        )

        btn_editar.pack(side="right", padx=10)

        self._tw(
            btn_editar,
            fg_color="BLUE",
            hover_color="DARK_BLUE",
            text_color="TOPBAR_TEXT"
        )

    def buscar(self):
        termo = f"%{self.ent_busca.get().strip()}%"
        tipo = self.cb_tipo.get()

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()

            if tipo == "Fisioterapeutas":
                cur.execute("""
                    SELECT id, nome, crefito, especialidade, celular
                    FROM fisioterapeutas
                    WHERE nome LIKE ? OR cpf LIKE ?
                    ORDER BY nome
                """, (termo, termo))
            else:
                cur.execute("""
                    SELECT id, nome, cargo, cpf, celular
                    FROM funcionarios
                    WHERE nome LIKE ? OR cpf LIKE ?
                    ORDER BY nome
                """, (termo, termo))

            self._rows = cur.fetchall()

            conn.close()

        except Exception as e:
            messagebox.showerror("Erro", str(e))
            return

        self._render(tipo)

    def _render(self, tipo):
        self._selected_row = None

        self.lbl_sel.configure(text="")

        for w in self._scroll.winfo_children():
            w.destroy()

        self._row_frames.clear()

        schema = self._COLS_FISIO if tipo == "Fisioterapeutas" else self._COLS_FUNC

        for w in self._hdr_frame.winfo_children():
            w.destroy()

        x = 8

        for hdr, width in zip(schema["headers"], schema["widths"]):
            lbl = ctk.CTkLabel(
                self._hdr_frame,
                text=hdr,
                font=(self._tm.font, 12, "bold"),
                text_color=self._tm.c("DARK_BLUE"),
                width=width,
                anchor="w",
            )

            lbl.place(x=x, y=9)

            self._tw(lbl, text_color="DARK_BLUE")

            x += width

        total = len(self._rows)

        self.lbl_count.configure(
            text=f"{total} registro{'s' if total != 1 else ''} encontrado{'s' if total != 1 else ''}"
        )

        if not self._rows:
            lbl = ctk.CTkLabel(
                self._scroll,
                text="Nenhum resultado encontrado.",
                font=(self._tm.font, 13),
                text_color=self._tm.c("GRAY"),
            )

            lbl.pack(pady=20)

            self._tw(lbl, text_color="GRAY")

            return

        for idx, row in enumerate(self._rows):
            bg = self._tm.c("WHITE") if idx % 2 == 0 else self._tm.c("BLUE_XL")

            fr = ctk.CTkFrame(
                self._scroll,
                fg_color=bg,
                corner_radius=0,
                height=38,
                cursor="hand2",
            )

            fr.pack(fill="x")
            fr.pack_propagate(False)

            fr._data = row
            fr._dtype = tipo
            fr._bg = bg

            x = 8

            for val, width in zip(row, schema["widths"]):
                lbl = ctk.CTkLabel(
                    fr,
                    text=str(val) if val else "—",
                    font=(self._tm.font, 13),
                    text_color=self._tm.c("BLACK"),
                    width=width,
                    anchor="w",
                )

                lbl.place(x=x, y=9)

                lbl.bind("<Button-1>", lambda _e, f=fr: self._select(f))

                x += width

            fr.bind("<Button-1>", lambda _e, f=fr: self._select(f))

            self._row_frames.append(fr)

    def _select(self, frame):
        if self._selected_row and self._selected_row.winfo_exists():
            self._selected_row.configure(
                fg_color=self._selected_row._bg
            )

            for child in self._selected_row.winfo_children():
                try:
                    child.configure(
                        fg_color=self._selected_row._bg,
                        text_color=self._tm.c("BLACK")
                    )
                except Exception:
                    pass

        self._selected_row = frame

        frame.configure(
            fg_color=self._tm.c("BLUE")
        )

        for child in frame.winfo_children():
            try:
                child.configure(
                    fg_color=self._tm.c("BLUE"),
                    text_color=self._tm.c("TOPBAR_TEXT")
                )
            except Exception:
                pass

        self.lbl_sel.configure(
            text=f"Selecionado: {frame._data[1]}"
        )

    def _editar(self):
        if not self._selected_row:
            messagebox.showwarning(
                "Atenção",
                "Selecione um registro para editar."
            )
            return

        EditDialog(
            self,
            self._selected_row._data,
            self._selected_row._dtype,
            self.buscar
        )

    def _excluir(self):
        if not self._selected_row:
            messagebox.showwarning(
                "Atenção",
                "Selecione um registro para excluir."
            )
            return

        data = self._selected_row._data
        dtype = self._selected_row._dtype

        tabela = (
            "fisioterapeutas"
            if dtype == "Fisioterapeutas"
            else "funcionarios"
        )

        nome = data[1]

        if not messagebox.askyesno(
            "Confirmar exclusão",
            f"Excluir '{nome}'?\nEssa ação não pode ser desfeita."
        ):
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()

            cur.execute(
                f"DELETE FROM {tabela} WHERE id = ?",
                (data[0],)
            )

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Sucesso",
                f"'{nome}' excluído com sucesso."
            )

            self.buscar()

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _on_theme_change(self, colors):
        self._apply_theme_widgets(colors)

        try:
            self.buscar()
        except Exception:
            pass

    def destroy(self):
        try:
            self._tm.unsubscribe(self._on_theme_change)
        except Exception:
            pass

        super().destroy()


class EditDialog(ctk.CTkToplevel):

    def __init__(self, parent, data, dtype, on_save):
        super().__init__(parent)

        self._tm = ThemeManager.get()

        self._data = data
        self._dtype = dtype
        self._on_save = on_save
        self._id = data[0]

        self.title("Editar Registro")
        self.geometry("540x360")
        self.resizable(False, False)

        self.configure(
            fg_color=self._tm.c("WHITE")
        )

        self.grab_set()
        self.transient(parent)

        self._build()

    def _build(self):
        ctk.CTkLabel(
            self,
            text=f"Editar {'Fisioterapeuta' if self._dtype == 'Fisioterapeutas' else 'Funcionário'}",
            font=(self._tm.font, 18, "bold"),
            text_color=self._tm.c("BLACK"),
        ).pack(anchor="w", padx=24, pady=(20, 16))

        form = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        form.pack(fill="x", padx=24)

        form.grid_columnconfigure((0, 1), weight=1)

        self._entries = {}

        if self._dtype == "Fisioterapeutas":
            fields = [
                ("nome", "Nome completo", 0, 0),
                ("crefito", "CREFITO", 0, 1),
                ("especialidade", "Especialidade", 1, 0),
                ("celular", "Celular", 1, 1),
                ("email", "E-mail", 2, 0),
            ]

            db_values = self._fetch(
                "fisioterapeutas",
                ["nome", "crefito", "especialidade", "celular", "email"]
            )

        else:
            fields = [
                ("nome", "Nome completo", 0, 0),
                ("cargo", "Cargo", 0, 1),
                ("celular", "Celular", 1, 0),
                ("email", "E-mail", 1, 1),
            ]

            db_values = self._fetch(
                "funcionarios",
                ["nome", "cargo", "celular", "email"]
            )

        for key, label, row, col in fields:
            ctk.CTkLabel(
                form,
                text=label,
                font=(self._tm.font, 12, "bold"),
                text_color=self._tm.c("GRAY_DARK"),
            ).grid(
                row=row * 2,
                column=col,
                sticky="w",
                padx=8
            )

            ent = ctk.CTkEntry(
                form,
                height=34,
                fg_color=self._tm.c("GRAY_BG"),
                border_color=self._tm.c("GRAY_LIGHT"),
                text_color=self._tm.c("BLACK"),
            )

            ent.grid(
                row=row * 2 + 1,
                column=col,
                sticky="ew",
                padx=8,
                pady=(0, 10)
            )

            val = db_values.get(key, "")

            if val:
                ent.insert(0, str(val))

            self._entries[key] = ent

        btn_fr = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        btn_fr.pack(fill="x", padx=24, pady=16)

        ctk.CTkButton(
            btn_fr,
            text="💾  Salvar",
            height=40,
            fg_color=self._tm.c("BLUE"),
            hover_color=self._tm.c("DARK_BLUE"),
            text_color=self._tm.c("TOPBAR_TEXT"),
            font=(self._tm.font, 13, "bold"),
            command=self._salvar,
        ).pack(side="right")

        ctk.CTkButton(
            btn_fr,
            text="Cancelar",
            height=40,
            fg_color=self._tm.c("BLUE_XL"),
            hover_color=self._tm.c("GRAY_LIGHT"),
            text_color=self._tm.c("BLUE"),
            font=(self._tm.font, 13, "bold"),
            command=self.destroy,
        ).pack(side="right", padx=10)

    def _fetch(self, tabela, cols):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()

            cur.execute(
                f"SELECT {','.join(cols)} FROM {tabela} WHERE id = ?",
                (self._id,)
            )

            row = cur.fetchone()

            conn.close()

            return dict(zip(cols, row)) if row else {}

        except Exception:
            return {}

    def _salvar(self):
        vals = {
            k: v.get().strip()
            for k, v in self._entries.items()
        }

        if not vals.get("nome"):
            messagebox.showerror(
                "Erro",
                "Nome é obrigatório.",
                parent=self
            )
            return

        tabela = (
            "fisioterapeutas"
            if self._dtype == "Fisioterapeutas"
            else "funcionarios"
        )

        sets = ", ".join(f"{k} = ?" for k in vals)

        params = list(vals.values()) + [self._id]

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()

            cur.execute(
                f"UPDATE {tabela} SET {sets} WHERE id = ?",
                params
            )

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Sucesso",
                "Registro atualizado com sucesso!",
                parent=self
            )

            self._on_save()

            self.destroy()

        except Exception as e:
            messagebox.showerror(
                "Erro",
                str(e),
                parent=self
            )