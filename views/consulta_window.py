from customtkinter import *
from PIL import Image

class ConsultaWindows(CTkToplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.dark_blue = "#0057A7"
        self.blue = "#0076E3"
        self.blue_light_1 = "#A5D4FF"
        self.blue_light_2 = "#DAEDFF"
        self.blue_light_3 = "#EEF7FF"
        self.white = "#FFFFFF"
        self.gray = "#BCBCBC"
        self.gray_light = "#F0F0F0"
        self.gray_light2 = '#F5F6FA'
        self.gray_dark = "#545454"
        self.black = "#000000"
        self.red = "#F2497C"
        self.red_light = "#FFE8F1"

        self.title("Consultas")
        self.configure(fg_color=self.gray_light2)
        self.geometry("1550x674+170+130")
        self.resizable(False, False)

        self.fr_topbar = CTkFrame(self, width=1550, height=53, fg_color=self.blue, corner_radius=0)
        self.fr_topbar.place(x=0, y=0)
        self.img_bg_topbar = CTkImage(Image.open('assets/bg_topbar.png'), size=(691, 52))
        self.lb_bg_topbar = CTkLabel(self.fr_topbar, image=self.img_bg_topbar, text='', fg_color=self.blue).place(x=858, y=0)

        self.icon_user = CTkImage(Image.open('assets/icons/user.png'), size=(32, 32))
        self.lb_icon_user = CTkLabel(self.fr_topbar, image=self.icon_user, text='', fg_color=self.blue).place(x=24, y=10)
        self.lb_nome_usuario = CTkLabel(self.fr_topbar, text='Bruno Álex', text_color=self.white, font=('Segoe UI', 12, 'bold'), height=12).place(x=64, y=10)
        self.lb_nivel_acesso = CTkLabel(self.fr_topbar, text='Admin', text_color=self.white, font=('Segoe UI', 12, 'normal'), height=12).place(x=64, y=28)

        self.tbv_consulta = CTkTabview(self, width=1502, height=580, fg_color=self.white, bg_color=self.gray_light2, border_color=self.gray, border_width=1.5, corner_radius=8, text_color=self.white, segmented_button_fg_color=self.gray, segmented_button_selected_color=self.blue, segmented_button_selected_hover_color=self.dark_blue, segmented_button_unselected_color=self.gray_dark, anchor=W)
        self.tbv_consulta.place(x=24, y=66)
        self.tab_agendar_consulta = self.tbv_consulta.add('Agendar Consulta')
        self.tab_buscar_consulta = self.tbv_consulta.add('Buscar Consulta')

        self.agendar_consulta()

    def agendar_consulta(self):
        self.fr_dados_agendamento = CTkFrame(self.tab_agendar_consulta, width=1458, height=418, fg_color=self.blue_light_3, border_color=self.blue_light_1, border_width=1, corner_radius=6)
        self.fr_dados_agendamento.place(x=14, y=10)

        self.lb_campos_dados_paciente = CTkLabel(self.fr_dados_agendamento, text='DADOS DO PACIENTE', text_color=self.black, font=('Segoe UI', 14, 'bold')).place(x=16, y=18)
        self.bt_buscar_paciente = CTkButton(self.fr_dados_agendamento, width=131, height=32, text='Buscar paciente', compound='left', fg_color=self.blue, bg_color=self.blue_light_3, hover_color=self.dark_blue, corner_radius=6).place(x=16, y=72)
        self.lb_nome_paciente_agendamento = CTkLabel(self.fr_dados_agendamento, text='Nome completo', text_color=self.black, font=('Segoe UI', 12, 'normal')).place(x=163, y=46)
        self.ent_nome_paciente_agendamento = CTkEntry(self.fr_dados_agendamento, width=342, height=32, fg_color=self.white, bg_color=self.blue_light_2, corner_radius=6, border_color=self.black, border_width=1, text_color=self.black, font=('Segoe UI', 14, 'normal'))
        self.ent_nome_paciente_agendamento.place(x=163, y=72)
        self.lb_nascimento_paciente_agendamento = CTkLabel(self.fr_dados_agendamento, text='Data de nascimento', text_color=self.black, font=('Segoe UI', 12, 'normal')).place(x=521, y=46)
        self.ent_nascimento_paciente_agendamento = CTkEntry(self.fr_dados_agendamento, width=150, height=32, fg_color=self.white, bg_color=self.blue_light_2, corner_radius=6, border_color=self.black, border_width=1, text_color=self.black, font=('Segoe UI', 14, 'normal'), placeholder_text='dd/mm/aaaa')
        self.ent_nascimento_paciente_agendamento.place(x=521, y=72)
        self.icon_bt_calendario_nascimento = CTkImage(Image.open('assets/icons/calendar-search.png'), size=(20, 20))
        self.bt_calendario_nascimento_agendamento = CTkButton(self.fr_dados_agendamento, width=32, height=32, text='', image=self.icon_bt_calendario_nascimento, compound='left', fg_color=self.blue_light_1, bg_color=self.blue_light_3, hover_color=self.blue_light_2, corner_radius=6).place(x=678, y=72)
        self.lb_cpf_paciente_agendamento = CTkLabel(self.fr_dados_agendamento, text='CPF', text_color=self.black, font=('Segoe UI', 12, 'normal')).place(x=730, y=46)
        self.ent_cpf_paciente_agendamento = CTkEntry(self.fr_dados_agendamento, width=178, height=32, fg_color=self.white, bg_color=self.blue_light_2, corner_radius=6, border_color=self.black, border_width=1, text_color=self.black, font=('Segoe UI', 14, 'normal'))
        self.ent_cpf_paciente_agendamento.place(x=730, y=72)
        self.lb_sexo_paciente_agendamento = CTkLabel(self.fr_dados_agendamento, text='Sexo', text_color=self.black, font=('Segoe UI', 12, 'normal')).place(x=924, y=46)
        self.cb_sexo_paciente_agendamento = CTkComboBox(self.fr_dados_agendamento, width=176, height=32, fg_color=self.white, bg_color=self.blue_light_2, corner_radius=6, border_color=self.black, border_width=1, button_color=self.blue, button_hover_color=self.dark_blue, dropdown_fg_color=self.white, dropdown_hover_color=self.blue_light_2, dropdown_text_color=self.black, dropdown_font=('Segoe UI', 14, 'normal'), text_color=self.black, font=('Segoe UI', 14, 'normal'), values=(['Masculino', 'Feminino', 'Não-binário', 'Agênero', 'Gênero fluido', 'Não declarado']))
        self.cb_sexo_paciente_agendamento.place(x=924, y=72)
        self.lb_email_paciente_agendamento = CTkLabel(self.fr_dados_agendamento, text='E-Mail', text_color=self.black, font=('Segoe UI', 12, 'normal')).place(x=1116, y=46)
        self.ent_email_paciente_agendamento = CTkEntry(self.fr_dados_agendamento, width=324, height=32, fg_color=self.white, bg_color=self.blue_light_2, corner_radius=6, border_color=self.black, border_width=1, text_color=self.black, font=('Segoe UI', 14, 'normal'))
        self.ent_email_paciente_agendamento.place(x=1116, y=72)
        self.lb_celular_paciente_agendamento = CTkLabel(self.fr_dados_agendamento, text='Celular/Telefone', text_color=self.black, font=('Segoe UI', 12, 'normal')).place(x=16, y=108)
        self.cb_celular_paciente_agendamento = CTkComboBox(self.fr_dados_agendamento, width=228, height=32, fg_color=self.white, bg_color=self.blue_light_2, corner_radius=6, border_color=self.black, border_width=1, button_color=self.blue, button_hover_color=self.dark_blue, dropdown_fg_color=self.white, dropdown_hover_color=self.blue_light_2, dropdown_text_color=self.black, dropdown_font=('Segoe UI', 14, 'normal'), text_color=self.black, font=('Segoe UI', 14, 'normal'), values=(['Celular', 'Celular/WhatsApp', 'Telefone']))
        self.cb_celular_paciente_agendamento.place(x=16, y=134)
        self.lb_celular_paciente_agendamento = CTkLabel(self.fr_dados_agendamento, text='Tipo de contato', text_color=self.black, font=('Segoe UI', 12, 'normal')).place(x=262, y=108)
        self.cb_celular_paciente_agendamento = CTkComboBox(self.fr_dados_agendamento, width=228, height=32, fg_color=self.white, bg_color=self.blue_light_2, corner_radius=6, border_color=self.black, border_width=1, button_color=self.blue, button_hover_color=self.dark_blue, dropdown_fg_color=self.white, dropdown_hover_color=self.blue_light_2, dropdown_text_color=self.black, dropdown_font=('Segoe UI', 14, 'normal'), text_color=self.black, font=('Segoe UI', 14, 'normal'), values=(['Pessoal', 'Residencial', 'Comercial']))
        self.cb_celular_paciente_agendamento.place(x=262, y=134)
        self.lb_celular_paciente_agendamento = CTkLabel(self.fr_dados_agendamento, text='Número', text_color=self.black, font=('Segoe UI', 12, 'normal')).place(x=508, y=108)
        self.ent_celular_paciente_agendamento = CTkEntry(self.fr_dados_agendamento, width=200, height=32, fg_color=self.white, bg_color=self.blue_light_2, corner_radius=6, border_color=self.black, border_width=1, text_color=self.black, font=('Segoe UI', 14, 'normal'), placeholder_text='Ex. 7190000-0000')
        self.ent_celular_paciente_agendamento.place(x=508, y=134)
        self.lb_obsevacao_celular_paciente_agendamento = CTkLabel(self.fr_dados_agendamento, text='Observação', text_color=self.black, font=('Segoe UI', 12, 'normal')).place(x=725, y=108)
        self.ent_obsevacao_celular_paciente_agendamento = CTkEntry(self.fr_dados_agendamento, width=716, height=32, fg_color=self.white, bg_color=self.blue_light_2, corner_radius=6, border_color=self.black, border_width=1, text_color=self.black, font=('Segoe UI', 14, 'normal'))
        self.ent_obsevacao_celular_paciente_agendamento.place(x=725, y=134)

        self.lb_campos_dados_medico = CTkLabel(self.fr_dados_agendamento, text='DADOS DO MÉDICO', text_color=self.black, font=('Segoe UI', 14, 'bold')).place(x=16, y=190)
        self.bt_buscar_medico = CTkButton(self.fr_dados_agendamento, width=131, height=32, text='Buscar médico', compound='left', fg_color=self.blue, bg_color=self.blue_light_3, hover_color=self.dark_blue, corner_radius=6).place(x=16, y=244)
        self.lb_nome_medico_agendamento = CTkLabel(self.fr_dados_agendamento, text='Nome do médico', text_color=self.black, font=('Segoe UI', 12, 'normal')).place(x=164, y=218)
        self.ent_nome_medico_agendamento = CTkEntry(self.fr_dados_agendamento, width=434, height=32, fg_color=self.white, bg_color=self.blue_light_2, corner_radius=6, border_color=self.black, border_width=1, text_color=self.black, font=('Segoe UI', 14, 'normal'))
        self.ent_nome_medico_agendamento.place(x=164, y=244)
        self.lb_especialidade1_medico_agendamento = CTkLabel(self.fr_dados_agendamento, text='Especialidade 1', text_color=self.black, font=('Segoe UI', 12, 'normal')).place(x=618, y=218)
        self.ent_especialidade1_medico_agendamento = CTkEntry(self.fr_dados_agendamento, width=272, height=32, fg_color=self.white, bg_color=self.blue_light_2, corner_radius=6, border_color=self.black, border_width=1, text_color=self.black, font=('Segoe UI', 14, 'normal'))
        self.ent_especialidade1_medico_agendamento.place(x=618, y=244)
        self.lb_especialidade2_medico_agendamento = CTkLabel(self.fr_dados_agendamento, text='Especialidade 2', text_color=self.black, font=('Segoe UI', 12, 'normal')).place(x=908, y=218)
        self.ent_especialidade2_medico_agendamento = CTkEntry(self.fr_dados_agendamento, width=272, height=32, fg_color=self.white, bg_color=self.blue_light_2, corner_radius=6, border_color=self.black, border_width=1, text_color=self.black, font=('Segoe UI', 14, 'normal'))
        self.ent_especialidade2_medico_agendamento.place(x=908, y=244)
        self.lb_crm_medico_agendamento = CTkLabel(self.fr_dados_agendamento, text='CRM/CFM', text_color=self.black, font=('Segoe UI', 12, 'normal')).place(x=1198, y=218)
        self.ent_crm_medico_agendamento = CTkEntry(self.fr_dados_agendamento, width=242, height=32, fg_color=self.white, bg_color=self.blue_light_2, corner_radius=6, border_color=self.black, border_width=1, text_color=self.black, font=('Segoe UI', 14, 'normal'))
        self.ent_crm_medico_agendamento.place(x=1198, y=244)

        self.lb_campos_dados_consulta = CTkLabel(self.fr_dados_agendamento, text='DADOS DA CONSULTA', text_color=self.black, font=('Segoe UI', 14, 'bold')).place(x=16, y=300)
        self.lb_convenio_agendamento = CTkLabel(self.fr_dados_agendamento, text='Convênio médico', text_color=self.black, font=('Segoe UI', 12, 'normal')).place(x=16, y=328)
        self.cb_convenio_agendamento = CTkComboBox(self.fr_dados_agendamento, width=150, height=32, fg_color=self.white, bg_color=self.blue_light_2, corner_radius=6, border_color=self.black, border_width=1, button_color=self.blue, button_hover_color=self.dark_blue, dropdown_fg_color=self.white, dropdown_hover_color=self.blue_light_2, dropdown_text_color=self.black, dropdown_font=('Segoe UI', 14, 'normal'), text_color=self.black, font=('Segoe UI', 14, 'normal'), values=(['Sim', 'Não']))
        self.cb_convenio_agendamento.place(x=16, y=354)
        self.lb_plano_saude_agendamento = CTkLabel(self.fr_dados_agendamento, text='Convênio médico', text_color=self.black, font=('Segoe UI', 12, 'normal')).place(x=184, y=328)
        self.cb_plano_saude_agendamento = CTkComboBox(self.fr_dados_agendamento, width=350, height=32, fg_color=self.white, bg_color=self.blue_light_2, corner_radius=6, border_color=self.black, border_width=1, button_color=self.blue, button_hover_color=self.dark_blue, dropdown_fg_color=self.white, dropdown_hover_color=self.blue_light_2, dropdown_text_color=self.black, dropdown_font=('Segoe UI', 14, 'normal'), text_color=self.black, font=('Segoe UI', 14, 'normal'), values=(["Amil", "Bradesco Saúde", "SulAmérica Saúde", "Unimed", "Golden Cross", "Hapvida", "NotreDame Intermédica", "Porto Seguro Saúde", "São Francisco Saúde", "Medial Saúde", 'SUS']))
        self.cb_plano_saude_agendamento.place(x=184, y=354)
        self.lb_data_consulta_agendamento = CTkLabel(self.fr_dados_agendamento, text='Data da consulta', text_color=self.black, font=('Segoe UI', 12, 'normal')).place(x=554, y=328)
        self.ent_data_consulta_agendamento = CTkEntry(self.fr_dados_agendamento, width=170, height=32, fg_color=self.white, bg_color=self.blue_light_2, corner_radius=6, border_color=self.black, border_width=1, text_color=self.black, font=('Segoe UI', 14, 'normal'), placeholder_text='dd/mm/aaaa')
        self.ent_data_consulta_agendamento.place(x=554, y=354)
        self.icon_bt_calendario_nascimento = CTkImage(Image.open('assets/icons/calendar-search.png'), size=(20, 20))
        self.bt_calendario_data_agendamento = CTkButton(self.fr_dados_agendamento, width=32, height=32, text='', image=self.icon_bt_calendario_nascimento, compound='left', fg_color=self.blue_light_1, bg_color=self.blue_light_3, hover_color=self.blue_light_2, corner_radius=6).place(x=732, y=354)
        self.lb_observacao_convenio_agendamento = CTkLabel(self.fr_dados_agendamento, text='Horário da consulta', text_color=self.black, font=('Segoe UI', 12, 'normal')).place(x=788, y=328)
        self.ent_hora_consulta_agendamento = CTkEntry(self.fr_dados_agendamento, width=170, height=32, fg_color=self.white, bg_color=self.blue_light_2, corner_radius=6, border_color=self.black, border_width=1, text_color=self.black, font=('Segoe UI', 14, 'normal'), placeholder_text='EX. 09:30')
        self.ent_hora_consulta_agendamento.place(x=788, y=354)
        self.lb_observacao_convenio_agendamento = CTkLabel(self.fr_dados_agendamento, text='Observação', text_color=self.black, font=('Segoe UI', 12, 'normal')).place(x=978, y=328)
        self.ent_observacao_convenio_agendamento = CTkEntry(self.fr_dados_agendamento, width=462, height=32, fg_color=self.white, bg_color=self.blue_light_2, corner_radius=6, border_color=self.black, border_width=1, text_color=self.black, font=('Segoe UI', 14, 'normal'))
        self.ent_observacao_convenio_agendamento.place(x=978, y=354)
        
        self.bt_cancelar_cadastro_paciente = CTkButton(self.tbv_consulta, width=148, height=40, text='Cancelar', text_color=self.blue, font=('Segoe UI', 12, 'bold'), fg_color=self.white, hover_color=self.blue_light_2, border_color=self.blue, border_width=1.5, corner_radius=8, command=self.fechar_consulta)
        self.bt_cancelar_cadastro_paciente.place(x=38, y=510)
        self.bt_limpar_cadastro_paciente = CTkButton(self.tbv_consulta, width=148, height=40, text='Limpar', text_color=self.blue, font=('Segoe UI', 12, 'bold'), fg_color=self.blue_light_1, hover_color=self.blue_light_2, corner_radius=8)
        self.bt_limpar_cadastro_paciente.place(x=1144, y=510)
        self.bt_salvar_cadastro_paciente = CTkButton(self.tbv_consulta, width=148, height=40, text='Agendar', text_color=self.white, font=('Segoe UI', 12, 'bold'), fg_color=self.blue, hover_color=self.dark_blue, corner_radius=8)
        self.bt_salvar_cadastro_paciente.place(x=1312, y=510)
        
    def fechar_consulta(self):
        self.destroy()