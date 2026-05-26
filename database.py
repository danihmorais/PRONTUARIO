import sqlite3
import hashlib
from config import DB_PATH

def inicializar_banco():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        nivel TEXT NOT NULL DEFAULT 'operador'
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pacientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT NOT NULL,
        data_nascimento TEXT,
        sexo TEXT,
        email TEXT,
        celular TEXT,
        cep TEXT,
        endereco TEXT,
        bairro TEXT,
        cidade TEXT,
        estado TEXT
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fisioterapeutas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        crefito TEXT NOT NULL,
        especialidade TEXT,
        cpf TEXT NOT NULL,
        email TEXT,
        celular TEXT
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS funcionarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cargo TEXT NOT NULL,
        cpf TEXT NOT NULL,
        data_nascimento TEXT,
        email TEXT,
        celular TEXT,
        cep TEXT,
        endereco TEXT,
        bairro TEXT,
        cidade TEXT,
        estado TEXT
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS consultas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_paciente INTEGER REFERENCES pacientes(id),
        id_fisioterapeuta INTEGER REFERENCES fisioterapeutas(id),
        data_consulta TEXT,
        horario TEXT,
        convenio TEXT,
        plano_saude TEXT,
        status TEXT DEFAULT 'Pendente',
        observacao TEXT
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS prontuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_paciente INTEGER REFERENCES pacientes(id),
        data_registro TEXT,
        queixa TEXT,
        exame TEXT,
        diagnostico TEXT,
        prescricao TEXT
    )
    ''')
    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE usuario = 'admin'")
    if cursor.fetchone()[0] == 0:
        senha_hash = hashlib.sha256("admin".encode()).hexdigest()
        cursor.execute(
            "INSERT INTO usuarios (usuario, senha, nivel) VALUES (?, ?, ?)",
            ("admin", senha_hash, "admin")
        )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    inicializar_banco()