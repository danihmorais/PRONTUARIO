@echo off
echo Iniciando compilacao do Gerador de Artefatos...
pyinstaller --noconfirm Prontuario.spec
echo Compilacao finalizada!
pause