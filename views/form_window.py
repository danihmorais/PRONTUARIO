import re
import sqlite3
import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import Calendar
from theme_manager import ThemeManager
from config import DB_PATH


# ─── helpers ──────────────────────────────────────────────────────────────────

def _only_digits(s: str) -> str:
    return re.sub(r"\D", "", s)

def _fmt_cpf(digits: str) -> str:
    d = digits[:11]
    if len(d) <= 3:   return d
    if len(d) <= 6:   return f"{d[:3]}.{d[3:]}"
    if len(d) <= 9:   return f"{d[:3]}.{d[3:6]}.{d[6:]}"
    return f"{d[:3]}.{d[3:6]}.{d[6:9]}-{d[9:]}"

def _fmt_cel(digits: str) -> str:
    d = digits[:11]
    if len(d) <= 2:   return f"({d}"
    if len(d) <= 7:   return f"({d[:2]}) {d[2:]}"
    return f"({d[:2]}) {d[2:7]}-{d[7:]}"

def _fmt_cep(digits: str) -> str:
    d = digits[:8]
    if len(d) <= 5:   return d
    return f"{d[:5]}-{d[5:]}"

def _validate_cpf(cpf: str) -> bool:
    d = _only_digits(cpf)
    if len(d) != 11 or len(set(d)) == 1:
        return False
    for i in range(2):
        s = sum(int(d[j]) * (10 + i - j) for j in range(9 + i))
        r = (s * 10) % 11
        if r == 10: r = 0
        if r != int(d[9 + i]):
            return False
    return True

def _validate_email(email: str) -> bool:
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))

def _bind_mask(entry: ctk.CTkEntry, fmt_fn):
    """Bind a formatting function to an entry on KeyRelease."""
    def _on_key(_event):
        raw = _only_digits(entry.get())
        formatted = fmt_fn(raw)
        entry.delete(0, "end")
        entry.insert(0, formatted)
    entry.bind("<KeyRelease>", _on_key)


# ─── main window ──────────────────────────────────────────────────────────────

class FormWindow(ctk.CTkFrame):
    def __init__(self, parent, controller=None, usuario=None):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self._tm = ThemeManager.get()
        self._calendar_target = None
        self._build_ui()

    # ── layout ────────────────────────────────────────────────────────────────

    def _build_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            header, text="Cadastros",
            font=(self._tm.font, 24, "bold"),
            text_color=self._tm.c("BLACK")
        ).pack(anchor="w")

        ctk.CTkLabel(
            header, text="Cadastre pacientes, fisioterapeutas e funcionários",
            font=(self._tm.font, 13),
            text_color=self._tm.c("GRAY")
        ).pack(anchor="w", pady=(4, 0))

        self.tbv = ctk.CTkTabview(
            self,
            fg_color=self._tm.c("WHITE"),
            bg_color="transparent",
            border_color=self._tm.c("GRAY_LIGHT"),
            border_width=1,
            corner_radius=10,
            segmented_button_selected_color=self._tm.c("BLUE"),
            segmented_button_selected_hover_color=self._tm.c("DARK_BLUE"),
            segmented_button_unselected_color=self._tm.c("GRAY_BG"),
            segmented_button_unselected_hover_color=self._tm.c("GRAY_LIGHT"),
            text_color=self._tm.c("BLACK"),
        )
        self.tbv.pack(fill="both", expand=True)

        self._tab_pac  = self.tbv.add("Pacientes")
        self._tab_fisio = self.tbv.add("Fisioterapeutas")
        self._tab_func = self.tbv.add("Funcionários")

        self._build_paciente()
        self._build_fisioterapeuta()
        self._build_funcionario()

    # ── section / field helpers ───────────────────────────────────────────────

    def _section(self, parent, title):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="cols")
        ctk.CTkLabel(
            frame, text=title,
            font=(self._tm.font, 13, "bold"),
            text_color=self._tm.c("BLUE")
        ).grid(row=0, column=0, sticky="w", padx=10, pady=(15, 4), columnspan=4)
        ctk.CTkFrame(frame, height=1, fg_color=self._tm.c("GRAY_LIGHT")).grid(
            row=1, column=0, columnspan=4, sticky="ew", padx=10, pady=(0, 12)
        )
        return frame

    def _field(self, parent, label, row, col, colspan=1,
               calendar=False, mask_fn=None, required=False):
        lbl_text = label + (" *" if required else "")
        ctk.CTkLabel(
            parent, text=lbl_text,
            text_color=self._tm.c("GRAY_DARK"),
            font=(self._tm.font, 12, "bold")
        ).grid(row=row * 2 + 2, column=col, sticky="w", padx=10)

        entry = ctk.CTkEntry(
            parent,
            fg_color=self._tm.c("GRAY_BG"),
            border_color=self._tm.c("GRAY_LIGHT"),
            text_color=self._tm.c("BLACK"),
            font=(self._tm.font, 13),
            height=36
        )
        entry.grid(row=row * 2 + 3, column=col, columnspan=colspan,
                   sticky="ew", padx=10, pady=(0, 12))

        if mask_fn:
            _bind_mask(entry, mask_fn)

        if calendar:
            ctk.CTkButton(
                parent, text="📅", width=36, height=36,
                fg_color=self._tm.c("BLUE"),
                hover_color=self._tm.c("DARK_BLUE"),
                command=lambda e=entry: self.pop_calendario(e)
            ).grid(row=row * 2 + 3, column=col + colspan - 1,
                   sticky="e", padx=10, pady=(0, 12))

        return entry

    def _combo(self, parent, label, row, col, values, colspan=1):
        ctk.CTkLabel(
            parent, text=label,
            text_color=self._tm.c("GRAY_DARK"),
            font=(self._tm.font, 12, "bold")
        ).grid(row=row * 2 + 2, column=col, sticky="w", padx=10)

        combo = ctk.CTkComboBox(
            parent, values=values,
            fg_color=self._tm.c("GRAY_BG"),
            border_color=self._tm.c("GRAY_LIGHT"),
            text_color=self._tm.c("BLACK"),
            button_color=self._tm.c("BLUE"),
            button_hover_color=self._tm.c("DARK_BLUE"),
            dropdown_fg_color=self._tm.c("WHITE"),
            dropdown_text_color=self._tm.c("BLACK"),
            font=(self._tm.font, 13),
            height=36
        )
        combo.grid(row=row * 2 + 3, column=col, columnspan=colspan,
                   sticky="ew", padx=10, pady=(0, 12))
        if values:
            combo.set(values[0])
        return combo

    def _actions(self, parent, save_cmd, clear_cmd):
        fr = ctk.CTkFrame(parent, fg_color="transparent")
        fr.pack(fill="x", padx=20, pady=(10, 20))
        ctk.CTkButton(
            fr, text="💾  Salvar Cadastro",
            fg_color=self._tm.c("BLUE"),
            hover_color=self._tm.c("DARK_BLUE"),
            text_color=self._tm.c("TOPBAR_TEXT"),
            font=(self._tm.font, 13, "bold"),
            height=42,
            command=save_cmd
        ).pack(side="right")
        ctk.CTkButton(
            fr, text="Limpar",
            fg_color=self._tm.c("BLUE_XL"),
            hover_color=self._tm.c("GRAY_LIGHT"),
            text_color=self._tm.c("BLUE"),
            font=(self._tm.font, 13, "bold"),
            height=42,
            command=clear_cmd
        ).pack(side="right", padx=10)

    # ── UFs helper ────────────────────────────────────────────────────────────

    @staticmethod
    def _ufs():
        return ["AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS",
                "MG","PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC",
                "SP","SE","TO"]

    # ══════════════════════════════════════════════════════════════════════════
    # PACIENTE
    # ══════════════════════════════════════════════════════════════════════════

    def _build_paciente(self):
        cont = ctk.CTkScrollableFrame(self._tab_pac, fg_color="transparent")
        cont.pack(fill="both", expand=True)

        geral = self._section(cont, "DADOS GERAIS")
        geral.pack(fill="x", padx=10)
        self.p_nome    = self._field(geral, "Nome completo",         0, 0, 2, required=True)
        self.p_nasc    = self._field(geral, "Data de nascimento",    0, 2, calendar=True)
        self.p_cpf     = self._field(geral, "CPF",                   0, 3, required=True, mask_fn=_fmt_cpf)
        self.p_sexo    = self._combo(geral, "Sexo", 1, 0,
            ["Masculino","Feminino","Não-binário","Gênero fluido","Não declarado"])

        end = self._section(cont, "ENDEREÇO")
        end.pack(fill="x", padx=10)
        self.p_cep     = self._field(end, "CEP",       0, 0, mask_fn=_fmt_cep)
        self.p_end     = self._field(end, "Endereço",  0, 1, 3)
        self.p_bairro  = self._field(end, "Bairro",    1, 0, 2)
        self.p_cidade  = self._field(end, "Cidade",    1, 2)
        self.p_estado  = self._combo(end, "Estado",    1, 3, self._ufs())

        contato = self._section(cont, "CONTATOS")
        contato.pack(fill="x", padx=10)
        self.p_email   = self._field(contato, "E-mail",  0, 0, 2)
        self.p_celular = self._field(contato, "Celular", 0, 2, 2, mask_fn=_fmt_cel)

        self._actions(cont, self._salvar_paciente, self._limpar_paciente)

    def _salvar_paciente(self):
        nome   = self.p_nome.get().strip()
        cpf    = self.p_cpf.get().strip()
        nasc   = self.p_nasc.get().strip()
        sexo   = self.p_sexo.get()
        email  = self.p_email.get().strip()
        cel    = self.p_celular.get().strip()
        cep    = self.p_cep.get().strip()
        end    = self.p_end.get().strip()
        bairro = self.p_bairro.get().strip()
        cidade = self.p_cidade.get().strip()
        estado = self.p_estado.get()

        # Validações
        erros = []
        if not nome:
            erros.append("• Nome completo é obrigatório.")
        if not cpf:
            erros.append("• CPF é obrigatório.")
        elif not _validate_cpf(cpf):
            erros.append("• CPF inválido.")
        if email and not _validate_email(email):
            erros.append("• E-mail inválido.")

        if erros:
            messagebox.showerror("Campos inválidos", "\n".join(erros))
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cur  = conn.cursor()

            # Verifica CPF duplicado
            cur.execute("SELECT id FROM pacientes WHERE cpf = ?", (_only_digits(cpf),))
            if cur.fetchone():
                messagebox.showerror("CPF duplicado",
                    "Já existe um paciente cadastrado com este CPF.")
                conn.close()
                return

            cur.execute("""
                INSERT INTO pacientes
                (nome, cpf, data_nascimento, sexo, email, celular,
                 cep, endereco, bairro, cidade, estado)
                VALUES (?,?,?,?,?,?,?,?,?,?,?)
            """, (nome, _only_digits(cpf), nasc, sexo, email, cel,
                  _only_digits(cep), end, bairro, cidade, estado))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", f"Paciente '{nome}' cadastrado com sucesso!")
            self._limpar_paciente()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _limpar_paciente(self):
        for w in [self.p_nome, self.p_nasc, self.p_cpf, self.p_end,
                  self.p_bairro, self.p_cidade, self.p_cep, self.p_email, self.p_celular]:
            w.delete(0, "end")

    # ══════════════════════════════════════════════════════════════════════════
    # FISIOTERAPEUTA
    # ══════════════════════════════════════════════════════════════════════════

    def _build_fisioterapeuta(self):
        cont = ctk.CTkScrollableFrame(self._tab_fisio, fg_color="transparent")
        cont.pack(fill="both", expand=True)

        geral = self._section(cont, "DADOS PROFISSIONAIS")
        geral.pack(fill="x", padx=10)
        self.f_nome     = self._field(geral, "Nome completo",   0, 0, 2, required=True)
        self.f_crefito  = self._field(geral, "CREFITO",         0, 2, required=True)
        self.f_cpf      = self._field(geral, "CPF",             0, 3, required=True, mask_fn=_fmt_cpf)
        self.f_esp      = self._combo(geral, "Especialidade",   1, 0, 2,
            ["Ortopedia","Neurologia","Respiratória","Cardiovascular",
             "Desportiva","Dermato-Funcional","Gerontologia","Pediatria","Outra"])
        self.f_email    = self._field(geral, "E-mail",          1, 2)
        self.f_celular  = self._field(geral, "Celular",         1, 3, mask_fn=_fmt_cel)

        self._actions(cont, self._salvar_fisioterapeuta, self._limpar_fisioterapeuta)

    def _salvar_fisioterapeuta(self):
        nome    = self.f_nome.get().strip()
        crefito = self.f_crefito.get().strip()
        cpf     = self.f_cpf.get().strip()
        esp     = self.f_esp.get()
        email   = self.f_email.get().strip()
        cel     = self.f_celular.get().strip()

        erros = []
        if not nome:
            erros.append("• Nome completo é obrigatório.")
        if not crefito:
            erros.append("• CREFITO é obrigatório.")
        if not cpf:
            erros.append("• CPF é obrigatório.")
        elif not _validate_cpf(cpf):
            erros.append("• CPF inválido.")
        if email and not _validate_email(email):
            erros.append("• E-mail inválido.")

        if erros:
            messagebox.showerror("Campos inválidos", "\n".join(erros))
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cur  = conn.cursor()
            cur.execute("SELECT id FROM fisioterapeutas WHERE cpf = ?", (_only_digits(cpf),))
            if cur.fetchone():
                messagebox.showerror("CPF duplicado",
                    "Já existe um fisioterapeuta cadastrado com este CPF.")
                conn.close()
                return

            cur.execute("""
                INSERT INTO fisioterapeutas (nome, crefito, especialidade, cpf, email, celular)
                VALUES (?,?,?,?,?,?)
            """, (nome, crefito, esp, _only_digits(cpf), email, cel))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", f"Fisioterapeuta '{nome}' cadastrado com sucesso!")
            self._limpar_fisioterapeuta()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _limpar_fisioterapeuta(self):
        for w in [self.f_nome, self.f_crefito, self.f_cpf,
                  self.f_email, self.f_celular]:
            w.delete(0, "end")

    # ══════════════════════════════════════════════════════════════════════════
    # FUNCIONÁRIO
    # ══════════════════════════════════════════════════════════════════════════

    def _build_funcionario(self):
        cont = ctk.CTkScrollableFrame(self._tab_func, fg_color="transparent")
        cont.pack(fill="both", expand=True)

        geral = self._section(cont, "DADOS GERAIS")
        geral.pack(fill="x", padx=10)
        self.func_nome  = self._field(geral, "Nome completo",      0, 0, 2, required=True)
        self.func_cargo = self._combo(geral, "Cargo",              0, 2,
            ["Recepcionista","Administrativo","Auxiliar de Fisioterapia",
             "Faturamento","Limpeza","Segurança","Outro"])
        self.func_cpf   = self._field(geral, "CPF",                0, 3, required=True, mask_fn=_fmt_cpf)
        self.func_nasc  = self._field(geral, "Data de nascimento", 1, 0, calendar=True)
        self.func_email = self._field(geral, "E-mail",             1, 1, 2)
        self.func_cel   = self._field(geral, "Celular",            1, 3, mask_fn=_fmt_cel)

        end = self._section(cont, "ENDEREÇO")
        end.pack(fill="x", padx=10)
        self.func_cep    = self._field(end, "CEP",       0, 0, mask_fn=_fmt_cep)
        self.func_end    = self._field(end, "Endereço",  0, 1, 3)
        self.func_bairro = self._field(end, "Bairro",    1, 0, 2)
        self.func_cidade = self._field(end, "Cidade",    1, 2)
        self.func_estado = self._combo(end, "Estado",    1, 3, self._ufs())

        self._actions(cont, self._salvar_funcionario, self._limpar_funcionario)

    def _salvar_funcionario(self):
        nome   = self.func_nome.get().strip()
        cargo  = self.func_cargo.get()
        cpf    = self.func_cpf.get().strip()
        nasc   = self.func_nasc.get().strip()
        email  = self.func_email.get().strip()
        cel    = self.func_cel.get().strip()
        cep    = self.func_cep.get().strip()
        end    = self.func_end.get().strip()
        bairro = self.func_bairro.get().strip()
        cidade = self.func_cidade.get().strip()
        estado = self.func_estado.get()

        erros = []
        if not nome:
            erros.append("• Nome completo é obrigatório.")
        if not cpf:
            erros.append("• CPF é obrigatório.")
        elif not _validate_cpf(cpf):
            erros.append("• CPF inválido.")
        if email and not _validate_email(email):
            erros.append("• E-mail inválido.")

        if erros:
            messagebox.showerror("Campos inválidos", "\n".join(erros))
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cur  = conn.cursor()
            cur.execute("SELECT id FROM funcionarios WHERE cpf = ?", (_only_digits(cpf),))
            if cur.fetchone():
                messagebox.showerror("CPF duplicado",
                    "Já existe um funcionário cadastrado com este CPF.")
                conn.close()
                return

            cur.execute("""
                INSERT INTO funcionarios
                (nome, cargo, cpf, data_nascimento, email, celular,
                 cep, endereco, bairro, cidade, estado)
                VALUES (?,?,?,?,?,?,?,?,?,?,?)
            """, (nome, cargo, _only_digits(cpf), nasc, email, cel,
                  _only_digits(cep), end, bairro, cidade, estado))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", f"Funcionário '{nome}' cadastrado com sucesso!")
            self._limpar_funcionario()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _limpar_funcionario(self):
        for w in [self.func_nome, self.func_cpf, self.func_nasc,
                  self.func_email, self.func_cel, self.func_cep,
                  self.func_end, self.func_bairro, self.func_cidade]:
            w.delete(0, "end")

    # ── calendário ────────────────────────────────────────────────────────────

    def pop_calendario(self, entry_destino):
        self._calendar_target = entry_destino
        colors = self._tm.colors

        self.pop = ctk.CTkToplevel(self)
        self.pop.configure(fg_color=colors["WHITE"])
        self.pop.geometry("386x287")
        self.pop.title("Calendário")
        self.pop.resizable(False, False)
        self.pop.transient(self.winfo_toplevel())
        self.pop.grab_set()
        self.pop.focus_force()

        self.calendario = Calendar(self.pop, selectmode="day", date_pattern="dd/mm/yyyy")
        self.calendario.place(x=0, y=0, width=386, height=207)

        ctk.CTkButton(
            self.pop, text="Confirmar",
            text_color=colors["TOPBAR_TEXT"],
            font=(self._tm.font, 12, "bold"),
            width=167, height=36,
            fg_color=colors["BLUE"],
            hover_color=colors["DARK_BLUE"],
            command=self._get_data
        ).place(x=18, y=231)

        ctk.CTkButton(
            self.pop, text="Cancelar",
            text_color=colors["BLUE"],
            font=(self._tm.font, 12, "bold"),
            width=167, height=36,
            fg_color=colors["BLUE_XL"],
            hover_color=colors["GRAY_LIGHT"],
            command=self.pop.destroy
        ).place(x=201, y=231)

    def _get_data(self):
        if self._calendar_target is not None:
            self._calendar_target.delete(0, "end")
            self._calendar_target.insert("end", self.calendario.get_date())
        self.pop.destroy()