import re
import sqlite3
import customtkinter as ctk
from tkinter import messagebox
from config import DB_PATH
from theme_manager import ThemeManager


def _only_digits(s):
    return re.sub(r"\D", "", str(s))


class SearchPacientView(ctk.CTkFrame):
    COLUMNS   = ("ID", "Nome", "CPF", "Nascimento", "Sexo", "Cidade")
    COL_WIDTHS = (40,   230,    130,   110,           110,    150)

    def __init__(self, parent, on_select=None):
        super().__init__(parent, fg_color="transparent")
        self._tm        = ThemeManager.get()
        self._on_select = on_select
        self._rows      = []
        self._row_frames = []
        self._selected_row = None
        self._tm.subscribe(self._on_theme_change)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self._build_ui()
        self._load_all()

    # ── layout ────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # cabeçalho
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 20))

        ctk.CTkLabel(
            header, text="Buscar Pacientes",
            text_color=self._tm.c("BLACK"),
            font=(self._tm.font, 24, "bold"),
        ).pack(anchor="w")

        ctk.CTkLabel(
            header, text="Consulte, edite e remova pacientes cadastrados",
            text_color=self._tm.c("GRAY"),
            font=(self._tm.font, 13),
        ).pack(anchor="w", pady=(4, 0))

        # barra de busca
        fr_search = ctk.CTkFrame(
            self,
            fg_color=self._tm.c("WHITE"),
            corner_radius=10,
            border_width=1,
            border_color=self._tm.c("GRAY_LIGHT"),
        )
        fr_search.grid(row=1, column=0, sticky="ew", pady=(0, 16))
        fr_search.grid_columnconfigure(1, weight=1)
        self._fr_search = fr_search

        ctk.CTkLabel(
            fr_search, text="Buscar:",
            text_color=self._tm.c("BLACK"),
            font=(self._tm.font, 13),
        ).grid(row=0, column=0, padx=(16, 10), pady=14)

        self.ent_search = ctk.CTkEntry(
            fr_search, height=36,
            fg_color=self._tm.c("WHITE"),
            border_color=self._tm.c("GRAY_DARK"),
            border_width=1, corner_radius=8,
            text_color=self._tm.c("BLACK"),
            font=(self._tm.font, 14),
            placeholder_text="Nome, CPF ou cidade...",
            placeholder_text_color=self._tm.c("GRAY"),
        )
        self.ent_search.grid(row=0, column=1, sticky="ew", pady=14)
        self.ent_search.bind("<Return>",     lambda _: self._search())
        self.ent_search.bind("<KeyRelease>", lambda _: self._search())

        self.bt_search = ctk.CTkButton(
            fr_search, width=120, height=36,
            text="Pesquisar",
            fg_color=self._tm.c("BLUE"),
            hover_color=self._tm.c("DARK_BLUE"),
            text_color=self._tm.c("TOPBAR_TEXT"),
            font=(self._tm.font, 13, "bold"),
            corner_radius=8,
            command=self._search,
        )
        self.bt_search.grid(row=0, column=2, padx=12, pady=14)

        # tabela
        table_cont = ctk.CTkFrame(
            self,
            fg_color=self._tm.c("WHITE"),
            corner_radius=10, border_width=1,
            border_color=self._tm.c("GRAY_LIGHT"),
        )
        table_cont.grid(row=2, column=0, sticky="nsew")
        table_cont.grid_rowconfigure(1, weight=1)
        table_cont.grid_columnconfigure(0, weight=1)
        self._table_cont = table_cont

        self._fr_header = ctk.CTkFrame(
            table_cont, fg_color=self._tm.c("BLUE_XL"),
            corner_radius=0, height=40,
        )
        self._fr_header.grid(row=0, column=0, sticky="ew")
        self._build_header()

        self._scroll = ctk.CTkScrollableFrame(
            table_cont, fg_color=self._tm.c("WHITE"),
            corner_radius=0,
            scrollbar_button_color=self._tm.c("GRAY_LIGHT"),
            scrollbar_button_hover_color=self._tm.c("GRAY"),
        )
        self._scroll.grid(row=1, column=0, sticky="nsew")

        # rodapé
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=3, column=0, sticky="ew", pady=(14, 0))
        footer.grid_columnconfigure(0, weight=1)

        self.lbl_status = ctk.CTkLabel(
            footer, text="",
            text_color=self._tm.c("GRAY"),
            font=(self._tm.font, 12),
        )
        self.lbl_status.grid(row=0, column=0, sticky="w")

        btn_frame = ctk.CTkFrame(footer, fg_color="transparent")
        btn_frame.grid(row=0, column=1, sticky="e")

        ctk.CTkButton(
            btn_frame, width=130, height=40,
            text="🗑  Excluir",
            fg_color=self._tm.c("RED_LIGHT"),
            hover_color="#fecaca",
            text_color=self._tm.c("RED"),
            font=(self._tm.font, 13, "bold"),
            corner_radius=8,
            command=self._excluir,
        ).pack(side="right")

        ctk.CTkButton(
            btn_frame, width=130, height=40,
            text="✏  Editar",
            fg_color=self._tm.c("BLUE"),
            hover_color=self._tm.c("DARK_BLUE"),
            text_color=self._tm.c("TOPBAR_TEXT"),
            font=(self._tm.font, 13, "bold"),
            corner_radius=8,
            command=self._editar,
        ).pack(side="right", padx=10)

        if self._on_select:
            ctk.CTkButton(
                btn_frame, width=140, height=40,
                text="✔  Selecionar",
                fg_color=self._tm.c("SUCCESS"),
                hover_color="#15803d",
                text_color="white",
                font=(self._tm.font, 13, "bold"),
                corner_radius=8,
                command=self._confirmar,
            ).pack(side="right", padx=10)

    def _build_header(self):
        for w in self._fr_header.winfo_children():
            w.destroy()
        x = 8
        for col, w in zip(self.COLUMNS, self.COL_WIDTHS):
            ctk.CTkLabel(
                self._fr_header, text=col,
                text_color=self._tm.c("DARK_BLUE"),
                font=(self._tm.font, 12, "bold"),
                width=w, anchor="w",
            ).place(x=x, y=10)
            x += w

    # ── dados ─────────────────────────────────────────────────────────────────

    def _load_all(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur  = conn.cursor()
            cur.execute(
                "SELECT id, nome, cpf, data_nascimento, sexo, cidade "
                "FROM pacientes ORDER BY nome"
            )
            self._rows = cur.fetchall()
            conn.close()
        except Exception:
            self._rows = []
        self._render_rows(self._rows)

    def _search(self):
        termo = self.ent_search.get().strip().lower()
        if not termo:
            self._render_rows(self._rows)
            return
        filtrado = [
            r for r in self._rows
            if any(termo in str(v).lower() for v in r)
        ]
        self._render_rows(filtrado)

    def _render_rows(self, rows):
        for fr in self._row_frames:
            fr.destroy()
        self._row_frames.clear()
        self._selected_row = None

        total = len(rows)
        self.lbl_status.configure(
            text=f"{total} paciente{'s' if total != 1 else ''} "
                 f"encontrado{'s' if total != 1 else ''}"
        )

        for idx, row in enumerate(rows):
            bg = self._tm.c("WHITE") if idx % 2 == 0 else self._tm.c("BLUE_XL")
            fr = ctk.CTkFrame(
                self._scroll, fg_color=bg,
                corner_radius=0, height=38, cursor="hand2",
            )
            fr.pack(fill="x")
            fr.pack_propagate(False)
            fr._data   = row
            fr._def_bg = bg

            x = 8
            for val, w in zip(row, self.COL_WIDTHS):
                lbl = ctk.CTkLabel(
                    fr, text=str(val) if val else "—",
                    text_color=self._tm.c("BLACK"),
                    font=(self._tm.font, 13),
                    width=w, anchor="w",
                )
                lbl.place(x=x, y=9)
                lbl.bind("<Button-1>", lambda _e, f=fr: self._select_row(f))
                x += w

            fr.bind("<Button-1>", lambda _e, f=fr: self._select_row(f))
            self._row_frames.append(fr)

    def _select_row(self, frame):
        if self._selected_row and self._selected_row.winfo_exists():
            self._selected_row.configure(fg_color=self._selected_row._def_bg)
            for child in self._selected_row.winfo_children():
                try:
                    child.configure(
                        fg_color=self._selected_row._def_bg,
                        text_color=self._tm.c("BLACK"),
                    )
                except Exception:
                    pass

        self._selected_row = frame
        frame.configure(fg_color=self._tm.c("BLUE"))
        for child in frame.winfo_children():
            try:
                child.configure(
                    fg_color=self._tm.c("BLUE"),
                    text_color=self._tm.c("TOPBAR_TEXT"),
                )
            except Exception:
                pass

    # ── ações ─────────────────────────────────────────────────────────────────

    def _editar(self):
        if not self._selected_row:
            messagebox.showwarning("Atenção", "Selecione um paciente para editar.")
            return
        EditPacientDialog(self, self._selected_row._data[0], self._load_all)

    def _excluir(self):
        if not self._selected_row:
            messagebox.showwarning("Atenção", "Selecione um paciente para excluir.")
            return
        nome = self._selected_row._data[1]
        pid  = self._selected_row._data[0]
        if not messagebox.askyesno(
            "Confirmar exclusão",
            f"Excluir o paciente '{nome}'?\n"
            "Todos os prontuários e consultas vinculados também serão excluídos.\n"
            "Essa ação não pode ser desfeita."
        ):
            return
        try:
            conn = sqlite3.connect(DB_PATH)
            cur  = conn.cursor()
            cur.execute("DELETE FROM prontuarios WHERE id_paciente = ?", (pid,))
            cur.execute("DELETE FROM consultas   WHERE id_paciente = ?", (pid,))
            cur.execute("DELETE FROM pacientes   WHERE id = ?",          (pid,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", f"Paciente '{nome}' excluído.")
            self._selected_row = None
            self._load_all()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _confirmar(self):
        if not self._selected_row:
            return
        if self._on_select:
            self._on_select(self._selected_row._data)

    # ── tema ──────────────────────────────────────────────────────────────────

    def _on_theme_change(self, colors):
        try:
            self._fr_search.configure(fg_color=colors["WHITE"],
                                       border_color=colors["GRAY_LIGHT"])
            self.ent_search.configure(fg_color=colors["WHITE"],
                                       border_color=colors["GRAY_DARK"],
                                       text_color=colors["BLACK"])
            self.bt_search.configure(fg_color=colors["BLUE"],
                                      hover_color=colors["DARK_BLUE"])
            self._table_cont.configure(fg_color=colors["WHITE"],
                                        border_color=colors["GRAY_LIGHT"])
            self._fr_header.configure(fg_color=colors["BLUE_XL"])
            self._scroll.configure(fg_color=colors["WHITE"])
            self.lbl_status.configure(text_color=colors["GRAY"])
        except Exception:
            pass

    def destroy(self):
        try:
            self._tm.unsubscribe(self._on_theme_change)
        except Exception:
            pass
        super().destroy()


# ─── diálogo de edição de paciente ───────────────────────────────────────────

class EditPacientDialog(ctk.CTkToplevel):
    _UFS = ["AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS",
            "MG","PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC",
            "SP","SE","TO"]

    def __init__(self, parent, paciente_id, on_save):
        super().__init__(parent)
        self._tm         = ThemeManager.get()
        self._id         = paciente_id
        self._on_save    = on_save
        self._entries    = {}

        self.title("Editar Paciente")
        self.geometry("640x540")
        self.resizable(False, False)
        self.configure(fg_color=self._tm.c("WHITE"))
        self.grab_set()
        self.transient(parent)

        self._load_data()
        self._build()

    def _load_data(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur  = conn.cursor()
            cur.execute("""
                SELECT nome, cpf, data_nascimento, sexo, email, celular,
                       cep, endereco, bairro, cidade, estado
                FROM pacientes WHERE id = ?
            """, (self._id,))
            row = cur.fetchone()
            conn.close()
            keys = ["nome","cpf","data_nascimento","sexo","email","celular",
                    "cep","endereco","bairro","cidade","estado"]
            self._db = dict(zip(keys, row)) if row else {}
        except Exception:
            self._db = {}

    def _build(self):
        ctk.CTkLabel(
            self, text="Editar Dados do Paciente",
            font=(self._tm.font, 18, "bold"),
            text_color=self._tm.c("BLACK"),
        ).pack(anchor="w", padx=24, pady=(18, 12))

        cont = ctk.CTkScrollableFrame(self, fg_color="transparent")
        cont.pack(fill="both", expand=True, padx=24)
        cont.grid_columnconfigure((0, 1), weight=1)

        def field(label, key, row, col, colspan=1, combo_vals=None):
            ctk.CTkLabel(
                cont, text=label,
                font=(self._tm.font, 12, "bold"),
                text_color=self._tm.c("GRAY_DARK"),
            ).grid(row=row*2, column=col, sticky="w", padx=6)

            if combo_vals:
                w = ctk.CTkComboBox(
                    cont, values=combo_vals,
                    fg_color=self._tm.c("GRAY_BG"),
                    border_color=self._tm.c("GRAY_LIGHT"),
                    text_color=self._tm.c("BLACK"),
                    height=34,
                )
                w.grid(row=row*2+1, column=col, columnspan=colspan,
                       sticky="ew", padx=6, pady=(0, 8))
                val = self._db.get(key, "")
                if val in combo_vals:
                    w.set(val)
                elif combo_vals:
                    w.set(combo_vals[0])
            else:
                w = ctk.CTkEntry(
                    cont, height=34,
                    fg_color=self._tm.c("GRAY_BG"),
                    border_color=self._tm.c("GRAY_LIGHT"),
                    text_color=self._tm.c("BLACK"),
                )
                w.grid(row=row*2+1, column=col, columnspan=colspan,
                       sticky="ew", padx=6, pady=(0, 8))
                val = self._db.get(key, "")
                if val:
                    w.insert(0, str(val))

            self._entries[key] = w

        field("Nome completo",    "nome",             0, 0, 2)
        field("CPF",              "cpf",              1, 0)
        field("Data nascimento",  "data_nascimento",  1, 1)
        field("Sexo", "sexo", 2, 0,
              combo_vals=["Masculino","Feminino","Não-binário","Gênero fluido","Não declarado"])
        field("E-mail",           "email",            2, 1)
        field("Celular",          "celular",          3, 0)
        field("CEP",              "cep",              3, 1)
        field("Endereço",         "endereco",         4, 0, 2)
        field("Bairro",           "bairro",           5, 0)
        field("Cidade",           "cidade",           5, 1)
        field("Estado",           "estado",           6, 0, combo_vals=self._UFS)

        # botões
        btn_fr = ctk.CTkFrame(self, fg_color="transparent")
        btn_fr.pack(fill="x", padx=24, pady=14)

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

    def _salvar(self):
        vals = {}
        for k, w in self._entries.items():
            if isinstance(w, ctk.CTkComboBox):
                vals[k] = w.get()
            else:
                vals[k] = w.get().strip()

        if not vals.get("nome"):
            messagebox.showerror("Erro", "Nome é obrigatório.", parent=self)
            return

        sets   = ", ".join(f"{k} = ?" for k in vals)
        params = list(vals.values()) + [self._id]

        try:
            conn = sqlite3.connect(DB_PATH)
            cur  = conn.cursor()
            cur.execute(f"UPDATE pacientes SET {sets} WHERE id = ?", params)
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Paciente atualizado com sucesso!", parent=self)
            self._on_save()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Erro", str(e), parent=self)