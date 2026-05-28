import { useState, useEffect } from "react";
import { dbQuery, dbExecute } from "../db";

interface Funcionario {
  id: number;
  nome: string;
  cargo: string;
  cpf: string;
  celular: string;
}

export default function Funcionarios() {
  const [funcionarios, setFuncionarios] = useState<Funcionario[]>([]);
  const [nome, setNome] = useState("");
  const [cargo, setCargo] = useState("");
  const [cpf, setCpf] = useState("");
  const [celular, setCelular] = useState("");

  const carregarFuncionarios = async () => {
    try {
      const res = await dbQuery<Funcionario>("SELECT id, nome, cargo, cpf, celular FROM funcionarios ORDER BY id DESC");
      setFuncionarios(res);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    carregarFuncionarios();
  }, []);

  const salvarFuncionario = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await dbExecute(
        "INSERT INTO funcionarios (nome, cargo, cpf, celular) VALUES (?, ?, ?, ?)",
        [nome, cargo, cpf, celular]
      );
      setNome("");
      setCargo("");
      setCpf("");
      setCelular("");
      carregarFuncionarios();
    } catch (e) {
      alert("Erro ao salvar: " + e);
    }
  };

  const deletarFuncionario = async (id: number) => {
    if (!confirm("Tem certeza que deseja excluir?")) return;
    try {
      await dbExecute("DELETE FROM funcionarios WHERE id = ?", [id.toString()]);
      carregarFuncionarios();
    } catch (e) {
      alert("Erro ao deletar: " + e);
    }
  };

  return (
    <div>
      <form onSubmit={salvarFuncionario} style={{ display: "flex", flexWrap: "wrap", gap: "1rem", marginBottom: "2rem", background: "#fff", padding: "1.5rem", borderRadius: "8px", boxShadow: "0 1px 3px rgba(0,0,0,0.1)" }}>
        <div style={{ flex: "1 1 200px", display: "flex", flexDirection: "column", gap: "0.5rem" }}>
          <label>Nome</label>
          <input value={nome} onChange={(e) => setNome(e.target.value)} required style={{ padding: "0.5rem" }} />
        </div>
        <div style={{ flex: "1 1 150px", display: "flex", flexDirection: "column", gap: "0.5rem" }}>
          <label>Cargo</label>
          <input value={cargo} onChange={(e) => setCargo(e.target.value)} required style={{ padding: "0.5rem" }} />
        </div>
        <div style={{ flex: "1 1 150px", display: "flex", flexDirection: "column", gap: "0.5rem" }}>
          <label>CPF</label>
          <input value={cpf} onChange={(e) => setCpf(e.target.value)} required style={{ padding: "0.5rem" }} />
        </div>
        <div style={{ flex: "1 1 150px", display: "flex", flexDirection: "column", gap: "0.5rem" }}>
          <label>Celular</label>
          <input value={celular} onChange={(e) => setCelular(e.target.value)} style={{ padding: "0.5rem" }} />
        </div>
        <div style={{ display: "flex", alignItems: "flex-end" }}>
          <button type="submit" style={{ padding: "0.6rem 1.2rem", background: "#10b981", color: "white", border: "none", borderRadius: "4px", cursor: "pointer", height: "38px" }}>
            Adicionar
          </button>
        </div>
      </form>

      <table style={{ width: "100%", borderCollapse: "collapse", background: "#fff", boxShadow: "0 1px 3px rgba(0,0,0,0.1)" }}>
        <thead>
          <tr style={{ background: "#f3f4f6", textAlign: "left" }}>
            <th style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>ID</th>
            <th style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>Nome</th>
            <th style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>Cargo</th>
            <th style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>CPF</th>
            <th style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>Celular</th>
            <th style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb", width: "100px" }}>Ações</th>
          </tr>
        </thead>
        <tbody>
          {funcionarios.map((f) => (
            <tr key={f.id}>
              <td style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>{f.id}</td>
              <td style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>{f.nome}</td>
              <td style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>{f.cargo}</td>
              <td style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>{f.cpf}</td>
              <td style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>{f.celular}</td>
              <td style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>
                <button onClick={() => deletarFuncionario(f.id)} style={{ background: "#ef4444", color: "white", border: "none", padding: "0.4rem 0.8rem", borderRadius: "4px", cursor: "pointer" }}>
                  Excluir
                </button>
              </td>
            </tr>
          ))}
          {funcionarios.length === 0 && (
            <tr>
              <td colSpan={6} style={{ padding: "1rem", textAlign: "center" }}>Nenhum funcionário cadastrado.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}