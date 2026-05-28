#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use rusqlite::{Connection, Result, types::ValueRef};
use sha2::{Digest, Sha256};
use std::env;
use std::fs;
use std::path::PathBuf;
use std::sync::Mutex;
use std::process::Command;
use tauri::{State, Manager, AppHandle};
use serde_json::{Map, Value};

struct AppState {
    db: Mutex<Connection>,
}

fn obter_caminho_db(app_handle: &AppHandle) -> PathBuf {
    let mut caminho = app_handle.path_resolver().app_data_dir().expect("Falha ao obter diretorio de dados do app");
    
    if !caminho.exists() {
        fs::create_dir_all(&caminho).unwrap();
    }
    
    caminho.push("prontuario.db");
    caminho
}

fn inicializar_banco(conn: &Connection) -> Result<()> {
    conn.execute_batch(
        "
        PRAGMA foreign_keys = ON;
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            nivel TEXT NOT NULL DEFAULT 'operador'
        );
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL,
            rg TEXT,
            celular TEXT,
            telefone TEXT,
            email TEXT,
            data_nascimento TEXT,
            sexo TEXT,
            estado_civil TEXT,
            profissao TEXT,
            convenio TEXT,
            numero_convenio TEXT,
            cep TEXT,
            endereco TEXT,
            numero TEXT,
            bairro TEXT,
            cidade TEXT,
            estado TEXT,
            observacoes TEXT
        );
        CREATE TABLE IF NOT EXISTS fisioterapeutas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            crefito TEXT NOT NULL,
            especialidade TEXT,
            cpf TEXT NOT NULL,
            email TEXT,
            celular TEXT
        );
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
        );
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
        );
        CREATE TABLE IF NOT EXISTS prontuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_paciente INTEGER REFERENCES pacientes(id),
            data_registro TEXT,
            queixa TEXT,
            exame TEXT,
            diagnostico TEXT,
            prescricao TEXT
        );
        ",
    )?;

    let mut stmt = conn.prepare("SELECT COUNT(*) FROM usuarios WHERE usuario = 'admin'")?;
    let count: i64 = stmt.query_row([], |row| row.get(0))?;

    if count == 0 {
        let mut hasher = Sha256::new();
        hasher.update(b"admin");
        let senha_hash = format!("{:x}", hasher.finalize());
        conn.execute(
            "INSERT INTO usuarios (usuario, senha, nivel) VALUES (?1, ?2, ?3)",
            (&"admin", &senha_hash, &"admin"),
        )?;
    }

    Ok(())
}

#[tauri::command]
fn login(usuario: String, senha: String, state: State<AppState>) -> Result<String, String> {
    let conn = state.db.lock().unwrap();
    let mut hasher = Sha256::new();
    hasher.update(senha.as_bytes());
    let senha_hash = format!("{:x}", hasher.finalize());

    let mut stmt = conn
        .prepare("SELECT nivel FROM usuarios WHERE usuario = ?1 AND senha = ?2")
        .map_err(|e| e.to_string())?;

    let resultado: rusqlite::Result<String> = stmt.query_row([&usuario, &senha_hash], |row| row.get(0));

    match resultado {
        Ok(nivel) => Ok(nivel),
        Err(rusqlite::Error::QueryReturnedNoRows) => Err("Usuário ou senha inválidos.".to_string()),
        Err(e) => Err(e.to_string()),
    }
}

#[tauri::command]
fn db_execute(sql: String, params: Vec<String>, state: State<AppState>) -> Result<usize, String> {
    let conn = state.db.lock().unwrap();
    let params_ref: Vec<&dyn rusqlite::ToSql> = params.iter().map(|s| s as &dyn rusqlite::ToSql).collect();
    conn.execute(&sql, params_ref.as_slice()).map_err(|e| e.to_string())
}

#[tauri::command]
fn db_query(sql: String, params: Vec<String>, state: State<AppState>) -> Result<Vec<Value>, String> {
    let conn = state.db.lock().unwrap();
    let params_ref: Vec<&dyn rusqlite::ToSql> = params.iter().map(|s| s as &dyn rusqlite::ToSql).collect();
    let mut stmt = conn.prepare(&sql).map_err(|e| e.to_string())?;

    let column_names: Vec<String> = stmt.column_names().into_iter().map(|c| c.to_string()).collect();

    let rows = stmt.query_map(params_ref.as_slice(), |row| {
        let mut map = Map::new();
        for (i, name) in column_names.iter().enumerate() {
            let val = match row.get_ref(i).unwrap() {
                ValueRef::Null => Value::Null,
                ValueRef::Integer(i) => Value::Number(i.into()),
                ValueRef::Real(f) => Value::Number(serde_json::Number::from_f64(f).unwrap()),
                ValueRef::Text(t) => Value::String(String::from_utf8_lossy(t).to_string()),
                ValueRef::Blob(_) => Value::Null,
            };
            map.insert(name.clone(), val);
        }
        Ok(Value::Object(map))
    }).map_err(|e| e.to_string())?;

    let mut result = Vec::new();
    for row in rows {
        result.push(row.map_err(|e| e.to_string())?);
    }
    Ok(result)
}

#[tauri::command]
fn alterar_senha(usuario: String, senha_atual: String, nova_senha: String, state: State<AppState>) -> Result<(), String> {
    let conn = state.db.lock().unwrap();
    let mut hasher = Sha256::new();
    hasher.update(senha_atual.as_bytes());
    let hash_atual = format!("{:x}", hasher.finalize());

    let count: i64 = conn
        .query_row("SELECT COUNT(*) FROM usuarios WHERE usuario = ?1 AND senha = ?2", [&usuario, &hash_atual], |row| row.get(0))
        .map_err(|e| e.to_string())?;

    if count == 0 {
        return Err("Senha atual incorreta.".to_string());
    }

    let mut hasher2 = Sha256::new();
    hasher2.update(nova_senha.as_bytes());
    let novo_hash = format!("{:x}", hasher2.finalize());

    conn.execute("UPDATE usuarios SET senha = ?1 WHERE usuario = ?2", [&novo_hash, &usuario])
        .map_err(|e| e.to_string())?;

    Ok(())
}

#[tauri::command]
fn aplicar_atualizacao(url: String) -> Result<(), String> {
    let temp_dir = env::temp_dir();
    let new_exe_path = temp_dir.join("Prontuario_new.tmp");

    let mut response = reqwest::blocking::get(&url).map_err(|e| e.to_string())?;
    let mut file = fs::File::create(&new_exe_path).map_err(|e| e.to_string())?;
    response.copy_to(&mut file).map_err(|e| e.to_string())?;

    let current_exe = env::current_exe().map_err(|e| e.to_string())?;
    let old_exe = current_exe.with_extension("old");

    if old_exe.exists() {
        let _ = fs::remove_file(&old_exe);
    }

    fs::rename(&current_exe, &old_exe).map_err(|e| e.to_string())?;
    fs::rename(&new_exe_path, &current_exe).map_err(|e| e.to_string())?;

    Command::new(&current_exe).spawn().map_err(|e| e.to_string())?;
    std::process::exit(0);
}

fn main() {
    tauri::Builder::default()
        .setup(|app| {
            let handle = app.handle();
            let caminho_db = obter_caminho_db(&handle);
            let conn = Connection::open(caminho_db).unwrap();
            
            inicializar_banco(&conn).unwrap();
            
            app.manage(AppState {
                db: Mutex::new(conn),
            });

            if let Ok(mut caminho_exe) = env::current_exe() {
                caminho_exe.set_extension("old");
                if caminho_exe.exists() {
                    let _ = fs::remove_file(caminho_exe);
                }
            }

            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            login,
            db_execute,
            db_query,
            alterar_senha,
            aplicar_atualizacao
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}