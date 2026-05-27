import sys
import customtkinter as ctk
from theme_manager import ThemeManager

class MockController:
    def __init__(self):
        self.app = None

    def open_form(self, *args):
        pass

    def open_appointment(self, *args):
        pass

    def open_search_pacient(self, *args):
        pass

    def open_search_doctor(self, *args):
        pass

    def realizar_logout(self, *args):
        pass

    def open_main(self, *args):
        pass

class DevRunner(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Dev Runner - Prontuário")
        self.geometry("450x480")
        
        self._tm = ThemeManager.get()
        self.configure(fg_color=self._tm.c("GRAY_BG"))
        
        lbl = ctk.CTkLabel(
            self, 
            text="Selecione a tela para testar:", 
            font=(self._tm.font, 18, "bold"),
            text_color=self._tm.c("BLACK")
        )
        lbl.pack(pady=30)
        
        views = [
            ("Main Window (Dashboard)", self.run_main),
            ("Form Window (Cadastros)", self.run_form),
            ("Appointment Window (Consultas)", self.run_appointment),
            ("Search Doctor View", self.run_search_doctor),
            ("Search Pacient View", self.run_search_pacient)
        ]
        
        for text, cmd in views:
            btn = ctk.CTkButton(
                self, 
                text=text, 
                command=cmd, 
                width=280, 
                height=45,
                fg_color=self._tm.c("BLUE"),
                hover_color=self._tm.c("DARK_BLUE"),
                text_color=self._tm.c("TOPBAR_TEXT"),
                font=(self._tm.font, 14, "bold"),
                corner_radius=8
            )
            btn.pack(pady=10)

    def launch_view(self, view_class, needs_controller=True):
        self.destroy()
        root = ctk.CTk()
        root.title(f"Dev Test - {view_class.__name__}")
        root.geometry("1280x720")
        root.configure(fg_color=self._tm.c("GRAY_BG"))
        
        controller = MockController()
        controller.app = root
        
        if needs_controller:
            view = view_class(root, controller)
        else:
            view = view_class(root)
            
        view.pack(fill="both", expand=True, padx=24, pady=24)
        root.mainloop()

    def run_main(self):
        self.destroy()
        from views.main_window import MainWindow
        controller = MockController()
        app = MainWindow(controller)
        app.mainloop()

    def run_form(self):
        from views.form_view import FormWindow
        self.launch_view(FormWindow)

    def run_appointment(self):
        from views.appointment_view import AppointmentWindow
        self.launch_view(AppointmentWindow)

    def run_team_view(self):
        from views.team_view import TeamView
        self.launch_view(TeamView, needs_controller=False)

    def run_pacient_view(self):
        from views.pacient_view import PacientView
        self.launch_view(PacientView, needs_controller=False)

if __name__ == "__main__":
    ctk.set_default_color_theme("blue")
    app = DevRunner()
    app.mainloop()