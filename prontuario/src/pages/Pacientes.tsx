import { useState, useEffect } from "react";
import { dbQuery, dbExecute } from "../db";

interface Paciente {
  id: number;
  nome: string;
  cpf: string;
  celular: string;
}

export default function Pacientes() {
  const [pacientes, setPacientes] = useState<Paciente[]>([]);
  const [nome, setNome] = useState("");
  const [cpf, setCpf] = useState("");
  const [celular, setCelular] = useState("");

  const carregarPacientes = async () => {
    try {
      const res = await dbQuery<Paciente>("SELECT id, nome, cpf, celular FROM pacientes ORDER BY id DESC");
      setPacientes(res);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    carregarPacientes();
  }, []);

  const salvarPaciente = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await dbExecute(
        "INSERT INTO pacientes (nome, cpf, celular) VALUES (?, ?, ?)",
        [nome, cpf, celular]
      );
      setNome("");
      setCpf("");
      setCelular("");
      carregarPacientes();
    } catch (e) {
      alert("Erro ao salvar: " + e);
    }
  };

  const deletarPaciente = async (id: number) => {
    if (!confirm("Tem certeza que deseja excluir?")) return;
    try {
      await dbExecute("DELETE FROM pacientes WHERE id = ?", [id.toString()]);
      carregarPacientes();
    } catch (e) {
      alert("Erro ao deletar: " + e);
    }
  };

  return (
    <div>
      <form onSubmit={salvarPaciente} style={{ display: "flex", gap: "1rem", marginBottom: "2rem", background: "#fff", padding: "1.5rem", borderRadius: "8px", boxShadow: "0 1px 3px rgba(0,0,0,0.1)" }}>
        <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: "0.5rem" }}>
          <label>Nome</label>
          <input value={nome} onChange={(e) => setNome(e.target.value)} required style={{ padding: "0.5rem" }} />
        </div>
        <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: "0.5rem" }}>
          <label>CPF</label>
          <input value={cpf} onChange={(e) => setCpf(e.target.value)} required style={{ padding: "0.5rem" }} />
        </div>
        <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: "0.5rem" }}>
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
            <th style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>CPF</th>
            <th style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>Celular</th>
            <th style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb", width: "100px" }}>Ações</th>
          </tr>
        </thead>
        <tbody>
          {pacientes.map((p) => (
            <tr key={p.id}>
              <td style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>{p.id}</td>
              <td style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>{p.nome}</td>
              <td style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>{p.cpf}</td>
              <td style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>{p.celular}</td>
              <td style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>
                <button onClick={() => deletarPaciente(p.id)} style={{ background: "#ef4444", color: "white", border: "none", padding: "0.4rem 0.8rem", borderRadius: "4px", cursor: "pointer" }}>
                  Excluir
                </button>
              </td>
            </tr>
          ))}
          {pacientes.length === 0 && (
            <tr>
              <td colSpan={5} style={{ padding: "1rem", textAlign: "center" }}>Nenhum paciente cadastrado.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}