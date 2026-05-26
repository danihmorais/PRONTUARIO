import re
import sqlite3
import customtkinter as ctk
from tkinter import messagebox
from theme_manager import ThemeManager
from config import DB_PATH


def _only_digits(s):
    return re.sub(r"\D", "", str(s))


class SearchDoctorView(ctk.CTkFrame):

    # colunas por tipo
    _COLS_FISIO = {
        "headers": ["ID", "Nome",             "CREFITO", "Especialidade", "Celular"],
        "widths":  [40,   220,                 110,       160,             120],
        "keys":    ["id", "nome",              "crefito", "especialidade", "celular"],
    }
    _COLS_FUNC = {
        "headers": ["ID", "Nome",  "Cargo",  "CPF",     "Celular"],
        "widths":  [40,   220,     160,      130,       120],
        "keys":    ["id", "nome",  "cargo",  "cpf",     "celular"],
    }

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self._tm = ThemeManager.get()
        self._rows = []
        self._row_frames = []
        self._selected_row = None
        self._tm.subscribe(self._on_theme_change)
        self._build_ui()
        self.buscar()

    # ── layout ────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # cabeçalho
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            header, text="Equipe Clínica e Funcionários",
            font=(self._tm.font, 24, "bold"),
            text_color=self._tm.c("BLACK"),
        ).pack(anchor="w")

        ctk.CTkLabel(
            header, text="Consulte, edite e remova fisioterapeutas e funcionários",
            font=(self._tm.font, 13),
            text_color=self._tm.c("GRAY"),
        ).pack(anchor="w", pady=(4, 0))

        # barra de busca
        search_fr = ctk.CTkFrame(
            self,
            fg_color=self._tm.c("WHITE"),
            corner_radius=10,
            border_color=self._tm.c("GRAY_LIGHT"),
            border_width=1,
        )
        search_fr.pack(fill="x", pady=(0, 16))

        self.ent_busca = ctk.CTkEntry(
            search_fr,
            placeholder_text="Buscar por nome ou CPF...",
            fg_color=self._tm.c("GRAY_BG"),
            border_color=self._tm.c("GRAY_LIGHT"),
            text_color=self._tm.c("BLACK"),
            width=300, height=36,
        )
        self.ent_busca.pack(side="left", padx=16, pady=14)
        self.ent_busca.bind("<Return>", lambda _: self.buscar())
        self.ent_busca.bind("<KeyRelease>", lambda _: self.buscar())

        self.cb_tipo = ctk.CTkComboBox(
            search_fr,
            values=["Fisioterapeutas", "Funcionários"],
            fg_color=self._tm.c("GRAY_BG"),
            border_color=self._tm.c("GRAY_LIGHT"),
            text_color=self._tm.c("BLACK"),
            button_color=self._tm.c("BLUE"),
            height=36, width=160,
            command=lambda _: self.buscar(),
        )
        self.cb_tipo.pack(side="left", padx=8)

        ctk.CTkButton(
            search_fr, text="🔍  Buscar",
            height=36, width=110,
            fg_color=self._tm.c("BLUE"),
            hover_color=self._tm.c("DARK_BLUE"),
            text_color=self._tm.c("TOPBAR_TEXT"),
            font=(self._tm.font, 13, "bold"),
            command=self.buscar,
        ).pack(side="left", padx=8)

        self.lbl_count = ctk.CTkLabel(
            search_fr, text="",
            font=(self._tm.font, 12),
            text_color=self._tm.c("GRAY"),
        )
        self.lbl_count.pack(side="right", padx=16)

        # container tabela
        self._table_outer = ctk.CTkFrame(
            self,
            fg_color=self._tm.c("WHITE"),
            corner_radius=10,
            border_color=self._tm.c("GRAY_LIGHT"),
            border_width=1,
        )
        self._table_outer.pack(fill="both", expand=True)
        self._table_outer.grid_rowconfigure(1, weight=1)
        self._table_outer.grid_columnconfigure(0, weight=1)

        # header row (será recriado em cada busca)
        self._hdr_frame = ctk.CTkFrame(
            self._table_outer,
            fg_color=self._tm.c("BLUE_XL"),
            corner_radius=0, height=38,
        )
        self._hdr_frame.grid(row=0, column=0, sticky="ew")

        self._scroll = ctk.CTkScrollableFrame(
            self._table_outer,
            fg_color=self._tm.c("WHITE"),
            corner_radius=0,
        )
        self._scroll.grid(row=1, column=0, sticky="nsew")

        # rodapé com botões de ação
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.pack(fill="x", pady=(12, 0))

        self.lbl_sel = ctk.CTkLabel(
            footer, text="",
            font=(self._tm.font, 12),
            text_color=self._tm.c("GRAY"),
        )
        self.lbl_sel.pack(side="left")

        ctk.CTkButton(
            footer, text="🗑  Excluir",
            height=38, width=130,
            fg_color=self._tm.c("RED_LIGHT"),
            hover_color="#fecaca",
            text_color=self._tm.c("RED"),
            font=(self._tm.font, 13, "bold"),
            command=self._excluir,
        ).pack(side="right")

        ctk.CTkButton(
            footer, text="✏  Editar",
            height=38, width=130,
            fg_color=self._tm.c("BLUE"),
            hover_color=self._tm.c("DARK_BLUE"),
            text_color=self._tm.c("TOPBAR_TEXT"),
            font=(self._tm.font, 13, "bold"),
            command=self._editar,
        ).pack(side="right", padx=10)

    # ── busca e renderização ──────────────────────────────────────────────────

    def buscar(self):
        termo = f"%{self.ent_busca.get().strip()}%"
        tipo  = self.cb_tipo.get()

        try:
            conn = sqlite3.connect(DB_PATH)
            cur  = conn.cursor()
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
        # limpa
        for fr in self._row_frames:
            fr.destroy()
        self._row_frames.clear()
        self._selected_row = None
        self.lbl_sel.configure(text="")

        # decide schema de colunas
        schema = self._COLS_FISIO if tipo == "Fisioterapeutas" else self._COLS_FUNC

        # reconstrói cabeçalho
        for w in self._hdr_frame.winfo_children():
            w.destroy()
        x = 8
        for hdr, w in zip(schema["headers"], schema["widths"]):
            ctk.CTkLabel(
                self._hdr_frame, text=hdr,
                font=(self._tm.font, 12, "bold"),
                text_color=self._tm.c("DARK_BLUE"),
                width=w, anchor="w",
            ).place(x=x, y=9)
            x += w

        total = len(self._rows)
        self.lbl_count.configure(
            text=f"{total} registro{'s' if total != 1 else ''} encontrado{'s' if total != 1 else ''}"
        )

        if not self._rows:
            ctk.CTkLabel(
                self._scroll, text="Nenhum resultado encontrado.",
                font=(self._tm.font, 13),
                text_color=self._tm.c("GRAY"),
            ).pack(pady=20)
            return

        for idx, row in enumerate(self._rows):
            bg = self._tm.c("WHITE") if idx % 2 == 0 else self._tm.c("BLUE_XL")
            fr = ctk.CTkFrame(
                self._scroll, fg_color=bg,
                corner_radius=0, height=38, cursor="hand2",
            )
            fr.pack(fill="x")
            fr.pack_propagate(False)
            fr._data  = row
            fr._dtype = tipo
            fr._bg    = bg

            x = 8
            for val, w in zip(row, schema["widths"]):
                lbl = ctk.CTkLabel(
                    fr, text=str(val) if val else "—",
                    font=(self._tm.font, 13),
                    text_color=self._tm.c("BLACK"),
                    width=w, anchor="w",
                )
                lbl.place(x=x, y=9)
                lbl.bind("<Button-1>", lambda _e, f=fr: self._select(f))
                x += w

            fr.bind("<Button-1>", lambda _e, f=fr: self._select(f))
            self._row_frames.append(fr)

    def _select(self, frame):
        # deseleciona anterior
        if self._selected_row and self._selected_row.winfo_exists():
            self._selected_row.configure(fg_color=self._selected_row._bg)
            for child in self._selected_row.winfo_children():
                try:
                    child.configure(fg_color=self._selected_row._bg,
                                    text_color=self._tm.c("BLACK"))
                except Exception:
                    pass

        self._selected_row = frame
        frame.configure(fg_color=self._tm.c("BLUE"))
        for child in frame.winfo_children():
            try:
                child.configure(fg_color=self._tm.c("BLUE"),
                                text_color=self._tm.c("TOPBAR_TEXT"))
            except Exception:
                pass

        nome = frame._data[1]
        self.lbl_sel.configure(
            text=f"Selecionado: {nome}",
            text_color=self._tm.c("BLUE"),
        )

    # ── editar ────────────────────────────────────────────────────────────────

    def _editar(self):
        if not self._selected_row:
            messagebox.showwarning("Atenção", "Selecione um registro para editar.")
            return
        data  = self._selected_row._data
        dtype = self._selected_row._dtype
        EditDialog(self, data, dtype, self.buscar)

    # ── excluir ───────────────────────────────────────────────────────────────

    def _excluir(self):
        if not self._selected_row:
            messagebox.showwarning("Atenção", "Selecione um registro para excluir.")
            return

        data  = self._selected_row._data
        dtype = self._selected_row._dtype
        nome  = data[1]
        tabela = "fisioterapeutas" if dtype == "Fisioterapeutas" else "funcionarios"

        if not messagebox.askyesno(
            "Confirmar exclusão",
            f"Excluir '{nome}'?\nEssa ação não pode ser desfeita."
        ):
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cur  = conn.cursor()
            cur.execute(f"DELETE FROM {tabela} WHERE id = ?", (data[0],))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", f"'{nome}' excluído com sucesso.")
            self._selected_row = None
            self.lbl_sel.configure(text="")
            self.buscar()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # ── tema ──────────────────────────────────────────────────────────────────

    def _on_theme_change(self, colors):
        try:
            self._table_outer.configure(fg_color=colors["WHITE"],
                                        border_color=colors["GRAY_LIGHT"])
            self._hdr_frame.configure(fg_color=colors["BLUE_XL"])
            self._scroll.configure(fg_color=colors["WHITE"])
        except Exception:
            pass

    def destroy(self):
        try:
            self._tm.unsubscribe(self._on_theme_change)
        except Exception:
            pass
        super().destroy()


# ─── diálogo de edição ────────────────────────────────────────────────────────

class EditDialog(ctk.CTkToplevel):
    def __init__(self, parent, data, dtype, on_save):
        super().__init__(parent)
        self._tm  = ThemeManager.get()
        self._data  = data
        self._dtype = dtype
        self._on_save = on_save
        self._id = data[0]

        self.title("Editar Registro")
        self.geometry("540x360")
        self.resizable(False, False)
        self.configure(fg_color=self._tm.c("WHITE"))
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

        form = ctk.CTkFrame(self, fg_color="transparent")
        form.pack(fill="x", padx=24)
        form.grid_columnconfigure((0, 1), weight=1)

        self._entries = {}

        if self._dtype == "Fisioterapeutas":
            fields = [
                ("nome",          "Nome completo",  0, 0),
                ("crefito",       "CREFITO",        0, 1),
                ("especialidade", "Especialidade",  1, 0),
                ("celular",       "Celular",        1, 1),
                ("email",         "E-mail",         2, 0),
            ]
            db_values = self._fetch("fisioterapeutas",
                ["nome","crefito","especialidade","celular","email"])
        else:
            fields = [
                ("nome",    "Nome completo", 0, 0),
                ("cargo",   "Cargo",         0, 1),
                ("celular", "Celular",       1, 0),
                ("email",   "E-mail",        1, 1),
            ]
            db_values = self._fetch("funcionarios",
                ["nome","cargo","celular","email"])

        for key, lbl, row, col in fields:
            ctk.CTkLabel(
                form, text=lbl,
                font=(self._tm.font, 12, "bold"),
                text_color=self._tm.c("GRAY_DARK"),
            ).grid(row=row*2, column=col, sticky="w", padx=8)

            ent = ctk.CTkEntry(
                form, height=34,
                fg_color=self._tm.c("GRAY_BG"),
                border_color=self._tm.c("GRAY_LIGHT"),
                text_color=self._tm.c("BLACK"),
            )
            ent.grid(row=row*2+1, column=col, sticky="ew", padx=8, pady=(0, 10))
            val = db_values.get(key, "")
            if val:
                ent.insert(0, str(val))
            self._entries[key] = ent

        # botões
        btn_fr = ctk.CTkFrame(self, fg_color="transparent")
        btn_fr.pack(fill="x", padx=24, pady=16)

        ctk.CTkButton(
            btn_fr, text="💾  Salvar",
            height=40,
            fg_color=self._tm.c("BLUE"),
            hover_color=self._tm.c("DARK_BLUE"),
            text_color=self._tm.c("TOPBAR_TEXT"),
            font=(self._tm.font, 13, "bold"),
            command=self._salvar,
        ).pack(side="right")

        ctk.CTkButton(
            btn_fr, text="Cancelar",
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
            cur  = conn.cursor()
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
        vals = {k: v.get().strip() for k, v in self._entries.items()}

        if not vals.get("nome"):
            messagebox.showerror("Erro", "Nome é obrigatório.", parent=self)
            return

        tabela = "fisioterapeutas" if self._dtype == "Fisioterapeutas" else "funcionarios"
        sets   = ", ".join(f"{k} = ?" for k in vals)
        params = list(vals.values()) + [self._id]

        try:
            conn = sqlite3.connect(DB_PATH)
            cur  = conn.cursor()
            cur.execute(f"UPDATE {tabela} SET {sets} WHERE id = ?", params)
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Registro atualizado com sucesso!", parent=self)
            self._on_save()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Erro", str(e), parent=self)