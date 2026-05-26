import sqlite3
import customtkinter as ctk

from config import DB_PATH
from theme_manager import ThemeManager


class SearchPacientView(ctk.CTkFrame):

    COLUMNS = ("ID", "Nome", "CPF", "Nascimento", "Sexo", "Cidade")
    COL_WIDTHS = (50, 260, 130, 110, 110, 160)

    def __init__(self, parent, on_select=None):
        super().__init__(
            parent,
            fg_color="transparent"
        )

        self._tm = ThemeManager.get()

        self._on_select = on_select
        self._rows: list[tuple] = []
        self._selected_row = None
        self._row_frames: list[ctk.CTkFrame] = []

        self._tm.subscribe(self._on_theme_change)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._build_ui()
        self._load_all()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self):

        # =========================
        # HEADER
        # =========================

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 20)
        )

        title = ctk.CTkLabel(
            header,
            text="Buscar pacientes",
            text_color=self._tm.c("BLACK"),
            font=(self._tm.font, 24, "bold")
        )

        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header,
            text="Pesquise pacientes cadastrados no sistema",
            text_color=self._tm.c("GRAY"),
            font=(self._tm.font, 13)
        )

        subtitle.pack(anchor="w", pady=(4, 0))

        # =========================
        # SEARCH BOX
        # =========================

        fr_search = ctk.CTkFrame(
            self,
            fg_color=self._tm.c("WHITE"),
            corner_radius=10,
            border_width=1,
            border_color=self._tm.c("GRAY_LIGHT")
        )

        fr_search.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        fr_search.grid_columnconfigure(1, weight=1)

        self._fr_search = fr_search

        lbl_search = ctk.CTkLabel(
            fr_search,
            text="Buscar:",
            text_color=self._tm.c("BLACK"),
            font=(self._tm.font, 13)
        )

        lbl_search.grid(
            row=0,
            column=0,
            padx=(16, 12),
            pady=16
        )

        self.ent_search = ctk.CTkEntry(
            fr_search,
            height=36,
            fg_color=self._tm.c("WHITE"),
            border_color=self._tm.c("GRAY_DARK"),
            border_width=1,
            corner_radius=8,
            text_color=self._tm.c("BLACK"),
            font=(self._tm.font, 14),
            placeholder_text="Nome, CPF ou cidade...",
            placeholder_text_color=self._tm.c("GRAY")
        )

        self.ent_search.grid(
            row=0,
            column=1,
            sticky="ew",
            pady=16
        )

        self.ent_search.bind("<Return>", lambda e: self._search())
        self.ent_search.bind("<KeyRelease>", lambda e: self._search())

        self.bt_search = ctk.CTkButton(
            fr_search,
            width=140,
            height=36,
            text="Pesquisar",
            fg_color=self._tm.c("BLUE"),
            hover_color=self._tm.c("DARK_BLUE"),
            text_color=self._tm.c("TOPBAR_TEXT"),
            font=(self._tm.font, 13, "bold"),
            corner_radius=8,
            command=self._search
        )

        self.bt_search.grid(
            row=0,
            column=2,
            padx=16,
            pady=16
        )

        # =========================
        # TABLE CONTAINER
        # =========================

        table_container = ctk.CTkFrame(
            self,
            fg_color=self._tm.c("WHITE"),
            corner_radius=10,
            border_width=1,
            border_color=self._tm.c("GRAY_LIGHT")
        )

        table_container.grid(
            row=2,
            column=0,
            sticky="nsew",
            pady=(20, 0)
        )

        table_container.grid_rowconfigure(1, weight=1)
        table_container.grid_columnconfigure(0, weight=1)

        self._table_container = table_container

        # =========================
        # TABLE HEADER
        # =========================

        fr_header = ctk.CTkFrame(
            table_container,
            fg_color=self._tm.c("BLUE_XL"),
            corner_radius=0,
            height=40
        )

        fr_header.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        self._fr_header = fr_header

        x = 8

        for col, w in zip(self.COLUMNS, self.COL_WIDTHS):

            lbl = ctk.CTkLabel(
                fr_header,
                text=col,
                text_color=self._tm.c("DARK_BLUE"),
                font=(self._tm.font, 12, "bold"),
                width=w,
                anchor="w"
            )

            lbl.place(x=x, y=10)

            x += w

        # =========================
        # SCROLLABLE TABLE
        # =========================

        self._scroll = ctk.CTkScrollableFrame(
            table_container,
            fg_color=self._tm.c("WHITE"),
            corner_radius=0,
            scrollbar_button_color=self._tm.c("GRAY_LIGHT"),
            scrollbar_button_hover_color=self._tm.c("GRAY")
        )

        self._scroll.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        # =========================
        # FOOTER
        # =========================

        footer = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        footer.grid(
            row=3,
            column=0,
            sticky="ew",
            pady=(20, 0)
        )

        footer.grid_columnconfigure(0, weight=1)

        self.lbl_status = ctk.CTkLabel(
            footer,
            text="",
            text_color=self._tm.c("GRAY"),
            font=(self._tm.font, 12)
        )

        self.lbl_status.grid(
            row=0,
            column=0,
            sticky="w"
        )

        buttons = ctk.CTkFrame(
            footer,
            fg_color="transparent"
        )

        buttons.grid(
            row=0,
            column=1,
            sticky="e"
        )

        self.bt_select = ctk.CTkButton(
            buttons,
            width=160,
            height=40,
            text="Selecionar",
            fg_color=self._tm.c("BLUE"),
            hover_color=self._tm.c("DARK_BLUE"),
            text_color=self._tm.c("TOPBAR_TEXT"),
            font=(self._tm.font, 12, "bold"),
            corner_radius=8,
            command=self._confirmar
        )

        self.bt_select.pack(side="right")

    # =========================================================
    # DATABASE
    # =========================================================

    def _load_all(self):

        try:

            conn = sqlite3.connect(DB_PATH)

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    id,
                    nome,
                    cpf,
                    data_nascimento,
                    sexo,
                    cidade
                FROM pacientes
                ORDER BY nome
            """)

            self._rows = cursor.fetchall()

            conn.close()

        except Exception as e:
            print(f"Erro ao carregar pacientes: {e}")
            self._rows = []

        self._render_rows(self._rows)

    # =========================================================
    # SEARCH
    # =========================================================

    def _search(self):

        termo = self.ent_search.get().strip().lower()

        if not termo:
            self._render_rows(self._rows)
            return

        filtrado = [
            r for r in self._rows
            if any(
                termo in str(campo).lower()
                for campo in r
            )
        ]

        self._render_rows(filtrado)

    # =========================================================
    # TABLE
    # =========================================================

    def _render_rows(self, rows):

        for fr in self._row_frames:
            fr.destroy()

        self._row_frames.clear()

        self._selected_row = None

        total = len(rows)

        self.lbl_status.configure(
            text=f"{total} paciente{'s' if total != 1 else ''} encontrado{'s' if total != 1 else ''}"
        )

        for idx, row in enumerate(rows):

            bg = (
                self._tm.c("WHITE")
                if idx % 2 == 0
                else self._tm.c("BLUE_XL")
            )

            fr = ctk.CTkFrame(
                self._scroll,
                fg_color=bg,
                corner_radius=0,
                height=38,
                cursor="hand2"
            )

            fr.pack(fill="x")

            fr.pack_propagate(False)

            fr._data = row
            fr._default_bg = bg

            x = 8

            for val, w in zip(row, self.COL_WIDTHS):

                lbl = ctk.CTkLabel(
                    fr,
                    text=str(val) if val else "",
                    text_color=self._tm.c("BLACK"),
                    font=(self._tm.font, 13),
                    width=w,
                    anchor="w"
                )

                lbl.place(x=x, y=9)

                lbl.bind(
                    "<Button-1>",
                    lambda e, f=fr: self._select_row(f)
                )

                x += w

            fr.bind(
                "<Button-1>",
                lambda e, f=fr: self._select_row(f)
            )

            self._row_frames.append(fr)

    def _select_row(self, frame):

        if self._selected_row and self._selected_row.winfo_exists():

            self._selected_row.configure(
                fg_color=self._selected_row._default_bg
            )

            for child in self._selected_row.winfo_children():

                try:
                    child.configure(
                        fg_color=self._selected_row._default_bg,
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

    # =========================================================
    # ACTIONS
    # =========================================================

    def _confirmar(self):

        if not self._selected_row:
            return

        if self._on_select:
            self._on_select(self._selected_row._data)

    # =========================================================
    # THEME
    # =========================================================

    def _on_theme_change(self, colors: dict):

        try:

            self._fr_search.configure(
                fg_color=colors["WHITE"],
                border_color=colors["GRAY_LIGHT"]
            )

            self.ent_search.configure(
                fg_color=colors["WHITE"],
                border_color=colors["GRAY_DARK"],
                text_color=colors["BLACK"]
            )

            self.bt_search.configure(
                fg_color=colors["BLUE"],
                hover_color=colors["DARK_BLUE"]
            )

            self._table_container.configure(
                fg_color=colors["WHITE"],
                border_color=colors["GRAY_LIGHT"]
            )

            self._fr_header.configure(
                fg_color=colors["BLUE_XL"]
            )

            self._scroll.configure(
                fg_color=colors["WHITE"]
            )

            self.bt_select.configure(
                fg_color=colors["BLUE"],
                hover_color=colors["DARK_BLUE"]
            )

            self.lbl_status.configure(
                text_color=colors["GRAY"]
            )

        except Exception as e:
            print(f"Erro ao atualizar tema: {e}")

    # =========================================================
    # DESTROY
    # =========================================================

    def destroy(self):

        try:
            self._tm.unsubscribe(self._on_theme_change)
        except Exception:
            pass

        super().destroy()