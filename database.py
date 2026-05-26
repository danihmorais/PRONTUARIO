import sqlite3
import hashlib

def inicializar_banco():
    conn = sqlite3.connect('prontuario.db')
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
        cpf TEXT,
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
    CREATE TABLE IF NOT EXISTS medicos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        crm TEXT,
        especialidade TEXT,
        cpf TEXT,
        email TEXT,
        celular TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS consultas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_paciente INTEGER REFERENCES pacientes(id),
        id_medico INTEGER REFERENCES medicos(id),
        data_consulta TEXT,
        horario TEXT,
        convenio TEXT,
        plano_saude TEXT,
        observacao TEXT
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