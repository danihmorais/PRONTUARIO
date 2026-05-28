import sqlite3
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from theme_manager import ThemeManager
from config import DB_PATH

class RecordView(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, fg_color="transparent")

        self.controller = controller
        self._tm = ThemeManager.get()
        self._paciente_id = None
        self._paciente_nome = None
        self._registros = []
        self._themed_widgets = []

        self._tm.subscribe(self._apply_theme)

        self._build_ui()

    def _tw(self, widget, **color_keys):
        self._themed_widgets.append({"widget": widget, "keys": color_keys})

    def _update_tw(self, widget, **new_keys):
        for entry in self._themed_widgets:
            if entry["widget"] == widget:
                entry["keys"].update(new_keys)
                break

    def _apply_theme(self, colors):
        if not self.winfo_exists():
            return

        alive = []

        for entry in self._themed_widgets:
            widget = entry["widget"]
            keys = entry["keys"]

            try:
                if widget.winfo_exists():
                    alive.append(entry)

                    cfg = {}
                    for param, color_key in keys.items():
                        if color_key in colors:
                            cfg[param] = colors[color_key]

                    if cfg:
                        widget.configure(**cfg)

                    widget.update_idletasks()

            except Exception:
                pass

        self._themed_widgets = alive

        try:
            self.tbv._segmented_button.configure(
                fg_color=colors["GRAY_BG"],
                selected_color=colors["BLUE"],
                selected_hover_color=colors["DARK_BLUE"],
                unselected_color=colors["GRAY_BG"],
                unselected_hover_color=colors["GRAY_LIGHT"],
                text_color=colors["BLACK"],
            )
        except Exception:
            pass

        try:
            self._tab_novo.configure(fg_color=colors["WHITE"])
            self._tab_hist.configure(fg_color=colors["WHITE"])
        except Exception:
            pass

    def _build_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 16))

        title = ctk.CTkLabel(
            header,
            text="Prontuário Fisioterapêutico",
            font=(self._tm.font, 24, "bold"),
            text_color=self._tm.c("BLACK"),
        )
        title.pack(anchor="w")
        self._tw(title, text_color="BLACK")

        subtitle = ctk.CTkLabel(
            header,
            text="Evolução clínica, avaliações e prescrições",
            font=(self._tm.font, 13),
            text_color=self._tm.c("GRAY"),
        )
        subtitle.pack(anchor="w", pady=(4, 0))
        self._tw(subtitle, text_color="GRAY")

        self._build_busca()

        self.tbv = ctk.CTkTabview(
            self,
            fg_color=self._tm.c("WHITE"),
            bg_color="transparent",
            border_color=self._tm.c("GRAY_LIGHT"),
            border_width=1,
            corner_radius=10,
            text_color=self._tm.c("BLACK"),
            segmented_button_selected_color=self._tm.c("BLUE"),
            segmented_button_selected_hover_color=self._tm.c("DARK_BLUE"),
            segmented_button_unselected_color=self._tm.c("GRAY_BG"),
            segmented_button_unselected_hover_color=self._tm.c("GRAY_LIGHT"),
        )
        self.tbv.pack(fill="both", expand=True)

        self._tw(
            self.tbv,
            fg_color="WHITE",
            border_color="GRAY_LIGHT",
            text_color="BLACK",
            segmented_button_selected_color="BLUE",
            segmented_button_selected_hover_color="DARK_BLUE",
            segmented_button_unselected_color="GRAY_BG",
            segmented_button_unselected_hover_color="GRAY_LIGHT",
        )

        self._tab_novo = self.tbv.add("Novo Registro")
        self._tab_hist = self.tbv.add("Histórico do Paciente")

        self._tw(self._tab_novo, fg_color="WHITE")
        self._tw(self._tab_hist, fg_color="WHITE")

        self._build_novo_registro()
        self._build_historico()

    def _build_busca(self):
        fr = ctk.CTkFrame(
            self,
            fg_color=self._tm.c("WHITE"),
            corner_radius=10,
            border_color=self._tm.c("GRAY_LIGHT"),
            border_width=1,
        )
        fr.pack(fill="x", pady=(0, 6))

        self._tw(fr, fg_color="WHITE", border_color="GRAY_LIGHT")

        lbl = ctk.CTkLabel(
            fr,
            text="Buscar Paciente:",
            font=(self._tm.font, 13, "bold"),
            text_color=self._tm.c("BLACK"),
        )
        lbl.pack(side="left", padx=(20, 8), pady=12)
        self._tw(lbl, text_color="BLACK")

        self.ent_busca = ctk.CTkEntry(
            fr,
            width=260,
            height=36,
            placeholder_text="Nome ou CPF...",
            fg_color=self._tm.c("GRAY_BG"),
            text_color=self._tm.c("BLACK"),
            border_color=self._tm.c("GRAY_LIGHT"),
            font=(self._tm.font, 13),
        )
        self.ent_busca.pack(side="left", padx=8, pady=12)
        self.ent_busca.bind("<Return>", lambda _: self._buscar())

        self._tw(self.ent_busca, fg_color="GRAY_BG", text_color="BLACK", border_color="GRAY_LIGHT")

        btn = ctk.CTkButton(
            fr,
            text="🔍  Buscar",
            height=36,
            width=120,
            fg_color=self._tm.c("BLUE"),
            hover_color=self._tm.c("DARK_BLUE"),
            text_color=self._tm.c("TOPBAR_TEXT"),
            font=(self._tm.font, 13, "bold"),
            command=self._buscar,
        )
        btn.pack(side="left", padx=8)
        self._tw(btn, fg_color="BLUE", hover_color="DARK_BLUE", text_color="TOPBAR_TEXT")

        self.lbl_pac_info = ctk.CTkLabel(
            fr,
            text="Nenhum paciente selecionado",
            font=(self._tm.font, 13, "bold"),
            text_color=self._tm.c("GRAY"),
        )
        self.lbl_pac_info.pack(side="right", padx=20)
        self._tw(self.lbl_pac_info, text_color="GRAY")

    def _build_novo_registro(self):
        cont = ctk.CTkScrollableFrame(
            self._tab_novo,
            fg_color=self._tm.c("WHITE"),
            corner_radius=0,
        )
        # CORRIGIDO: usando pack em vez de grid para evitar conflito com pack já usado na tab
        cont.pack(fill="both", expand=True)

        self._tw(cont, fg_color="WHITE")

        self._fields = {}

        specs = [
            ("queixa", "📋  Motivo da Consulta / Queixa Principal"),
            ("exame", "🔍  Avaliação Fisioterapêutica / Exame Físico"),
            ("diagnostico", "📊  Diagnóstico Cinesiológico Funcional / Conduta"),
            ("prescricao", "💊  Prescrição de Exercícios / Orientações"),
        ]

        for key, label in specs:
            self._fields[key] = self._add_textbox(cont, label)

        footer = ctk.CTkFrame(cont, fg_color="transparent")
        footer.pack(fill="x", padx=10, pady=(10, 20))

        btn_salvar = ctk.CTkButton(
            footer,
            text="💾  Salvar Prontuário",
            height=42,
            fg_color=self._tm.c("BLUE"),
            hover_color=self._tm.c("DARK_BLUE"),
            text_color=self._tm.c("TOPBAR_TEXT"),
            font=(self._tm.font, 13, "bold"),
            command=self._salvar,
        )
        btn_salvar.pack(side="right")
        self._tw(btn_salvar, fg_color="BLUE", hover_color="DARK_BLUE", text_color="TOPBAR_TEXT")

        btn_limpar = ctk.CTkButton(
            footer,
            text="Limpar",
            height=42,
            fg_color=self._tm.c("BLUE_XL"),
            hover_color=self._tm.c("GRAY_LIGHT"),
            text_color=self._tm.c("BLUE"),
            font=(self._tm.font, 13, "bold"),
            command=self._limpar,
        )
        btn_limpar.pack(side="right", padx=10)
        self._tw(btn_limpar, fg_color="BLUE_XL", hover_color="GRAY_LIGHT", text_color="BLUE")

    def _build_historico(self):
        barra = ctk.CTkFrame(self._tab_hist, fg_color="transparent")
        barra.pack(fill="x", padx=10, pady=(10, 6))

        self.ent_busca_hist = ctk.CTkEntry(
            barra,
            placeholder_text="Filtrar por text...",
            height=32,
            width=240,
            fg_color=self._tm.c("GRAY_BG"),
            text_color=self._tm.c("BLACK"),
            border_color=self._tm.c("GRAY_LIGHT"),
        )
        self.ent_busca_hist.pack(side="left")
        self._tw(self.ent_busca_hist, fg_color="GRAY_BG", text_color="BLACK", border_color="GRAY_LIGHT")
        self.ent_busca_hist.bind("<KeyRelease>", lambda _: self._filtrar_hist())

        btn_refresh = ctk.CTkButton(
            barra,
            text="🔄",
            width=36,
            height=32,
            fg_color=self._tm.c("BLUE_XL"),
            hover_color=self._tm.c("GRAY_LIGHT"),
            text_color=self._tm.c("BLUE"),
            command=self._recarregar_hist,
        )
        btn_refresh.pack(side="left", padx=8)
        self._tw(btn_refresh, fg_color="BLUE_XL", hover_color="GRAY_LIGHT", text_color="BLUE")

        self.lbl_hist_count = ctk.CTkLabel(
            barra,
            text="",
            font=(self._tm.font, 12),
            text_color=self._tm.c("GRAY"),
        )
        self.lbl_hist_count.pack(side="right")
        self._tw(self.lbl_hist_count, text_color="GRAY")

        self.cont_hist = ctk.CTkScrollableFrame(
            self._tab_hist,
            fg_color=self._tm.c("WHITE"),
            corner_radius=0,
        )
        # CORRIGIDO: usando pack em vez de grid para evitar conflito com pack já usado na tab
        self.cont_hist.pack(fill="both", expand=True)

        self._tw(self.cont_hist, fg_color="WHITE")

        self._mostrar_vazio_hist()

    def _add_textbox(self, parent, label_text):
        fr = ctk.CTkFrame(parent, fg_color="transparent")
        fr.pack(fill="x", padx=10, pady=8)

        lbl = ctk.CTkLabel(
            fr,
            text=label_text,
            font=(self._tm.font, 13, "bold"),
            text_color=self._tm.c("BLACK"),
        )
        lbl.pack(anchor="w", pady=(0, 4))
        self._tw(lbl, text_color="BLACK")

        txt = ctk.CTkTextbox(
            fr,
            height=90,
            fg_color=self._tm.c("GRAY_BG"),
            border_color=self._tm.c("GRAY_LIGHT"),
            border_width=1,
            text_color=self._tm.c("BLACK"),
            font=(self._tm.font, 13),
        )
        txt.pack(fill="x")
        self._tw(txt, fg_color="GRAY_BG", border_color="GRAY_LIGHT", text_color="BLACK")

        return txt

    def _mostrar_vazio_hist(self):
        for w in self.cont_hist.winfo_children():
            w.destroy()

        lbl = ctk.CTkLabel(
            self.cont_hist,
            text="Busque um paciente para ver o histórico de prontuários.",
            font=(self._tm.font, 14),
            text_color=self._tm.c("GRAY"),
        )
        lbl.pack(pady=40)
        self._tw(lbl, text_color="GRAY")

    def _buscar(self):
        termo = self.ent_busca.get().strip()

        if not termo:
            messagebox.showwarning("Atenção", "Digite o nome ou CPF do paciente.")
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()

            digitos = "".join(c for c in termo if c.isdigit())

            if digitos:
                cur.execute("SELECT id, nome, cpf FROM pacientes WHERE cpf = ?", (digitos,))
            else:
                cur.execute("SELECT id, nome, cpf FROM pacientes WHERE nome LIKE ?", (f"%{termo}%",))

            resultados = cur.fetchall()
            conn.close()

        except Exception as e:
            messagebox.showerror("Erro", str(e))
            return

        if not resultados:
            self.lbl_pac_info.configure(text="Paciente não encontrado", text_color=self._tm.c("RED"))
            self._paciente_id = None
            self._mostrar_vazio_hist()
            return

        if len(resultados) == 1:
            self._selecionar_paciente(*resultados[0])
        else:
            self._popup_selecao(resultados)

    def _selecionar_paciente(self, pid, nome, cpf):
        self._paciente_id = pid
        self._paciente_nome = nome

        self.lbl_pac_info.configure(text=f"📋  {nome}  —  CPF: {cpf}", text_color=self._tm.c("BLUE"))
        self._carregar_historico()

    def _carregar_historico(self):
        if not self._paciente_id:
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()

            cur.execute("""
                SELECT id, data_registro, queixa, exame, diagnostico, prescricao
                FROM prontuarios
                WHERE id_paciente = ?
                ORDER BY id DESC
            """, (self._paciente_id,))

            self._registros = cur.fetchall()
            conn.close()

        except Exception as e:
            messagebox.showerror("Erro", str(e))
            return

        self._render_historico(self._registros)

    def _recarregar_hist(self):
        self.ent_busca_hist.delete(0, "end")
        self._carregar_historico()

    def _filtrar_hist(self):
        text = self.ent_busca_hist.get().strip().lower()
        if not text:
            self._render_historico(self._registros)
            return

        filtrados = [r for r in self._registros if any(text in str(v).lower() for v in r)]
        self._render_historico(filtrados)

    def _render_historico(self, registros):
        for w in self.cont_hist.winfo_children():
            w.destroy()

        self.lbl_hist_count.configure(text=f"{len(registros)} registro(s)")

        if not registros:
            lbl = ctk.CTkLabel(
                self.cont_hist,
                text="Nenhum registro encontrado.",
                font=(self._tm.font, 14),
                text_color=self._tm.c("GRAY"),
            )
            lbl.pack(pady=30)
            self._tw(lbl, text_color="GRAY")
            return

        for reg in registros:
            self._render_card(*reg)

    def _render_card(self, rid, data_reg, queixa, exame, diag, presc):
        card = ctk.CTkFrame(
            self.cont_hist,
            fg_color=self._tm.c("WHITE"),
            corner_radius=10,
            border_color=self._tm.c("GRAY_LIGHT"),
            border_width=1,
        )

        card.pack(fill="x", padx=0, pady=8)
        self._tw(card, fg_color="WHITE", border_color="GRAY_LIGHT")

        header = ctk.CTkFrame(card, fg_color=self._tm.c("BLUE_XL"))
        header.pack(fill="x", padx=1, pady=(1, 0))
        self._tw(header, fg_color="BLUE_XL")

        lbl = ctk.CTkLabel(
            header,
            text=f"📅  {data_reg}",
            font=(self._tm.font, 13, "bold"),
            text_color=self._tm.c("DARK_BLUE"),
        )
        lbl.pack(side="left", padx=14, pady=8)

        btn = ctk.CTkButton(
            header,
            text="🗑  Excluir",
            width=90,
            height=28,
            fg_color=self._tm.c("RED_LIGHT"),
            hover_color=self._tm.c("RED_LIGHT"),
            text_color=self._tm.c("RED"),
            command=lambda i=rid: self._excluir_registro(i),
        )
        btn.pack(side="right", padx=10, pady=6)

        body = ctk.CTkFrame(card, fg_color="transparent")
        body.pack(fill="x", padx=10, pady=10)

        campos = [
            ("Queixa", queixa),
            ("Exame", exame),
            ("Diagnóstico", diag),
            ("Prescrição", presc),
        ]

        for titulo, valor in campos:
            if valor and valor.strip():
                ctk.CTkLabel(
                    body,
                    text=titulo,
                    font=(self._tm.font, 12, "bold"),
                    text_color=self._tm.c("BLACK"),
                ).pack(anchor="w")

                ctk.CTkLabel(
                    body,
                    text=valor,
                    font=(self._tm.font, 12),
                    text_color=self._tm.c("GRAY"),
                    justify="left",
                ).pack(anchor="w", pady=(0, 6))

    def _salvar(self):
        if not self._paciente_id:
            messagebox.showwarning("Atenção", "Selecione um paciente.")
            return

        queixa = self._fields["queixa"].get("1.0", "end").strip()
        exame = self._fields["exame"].get("1.0", "end").strip()
        diag = self._fields["diagnostico"].get("1.0", "end").strip()
        presc = self._fields["prescricao"].get("1.0", "end").strip()

        if not any([queixa, exame, diag, presc]):
            messagebox.showwarning("Atenção", "Preencha ao menos um campo.")
            return

        data = datetime.now().strftime("%d/%m/%Y %H:%M")

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO prontuarios
                (id_paciente, data_registro, queixa, exame, diagnostico, prescricao)
                VALUES (?,?,?,?,?,?)
            """, (self._paciente_id, data, queixa, exame, diag, presc))

            conn.commit()
            conn.close()

            self._limpar()
            self._carregar_historico()

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _excluir_registro(self, registro_id):
        if not messagebox.askyesno("Confirmar", "Excluir registro?"):
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("DELETE FROM prontuarios WHERE id = ?", (registro_id,))
            conn.commit()
            conn.close()
            self._carregar_historico()

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _limpar(self):
        for txt in self._fields.values():
            txt.delete("1.0", "end")