import { useState, useEffect } from "react";
import { dbQuery, dbExecute } from "../db";

interface Fisioterapeuta {
  id: number;
  nome: string;
  crefito: string;
  especialidade: string;
  celular: string;
}

export default function Fisioterapeutas() {
  const [fisioterapeutas, setFisioterapeutas] = useState<Fisioterapeuta[]>([]);
  const [nome, setNome] = useState("");
  const [crefito, setCrefito] = useState("");
  const [especialidade, setEspecialidade] = useState("");
  const [celular, setCelular] = useState("");
  const [cpf, setCpf] = useState("");

  const carregarFisioterapeutas = async () => {
    try {
      const res = await dbQuery<Fisioterapeuta>("SELECT id, nome, crefito, especialidade, celular FROM fisioterapeutas ORDER BY id DESC");
      setFisioterapeutas(res);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    carregarFisioterapeutas();
  }, []);

  const salvarFisioterapeuta = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await dbExecute(
        "INSERT INTO fisioterapeutas (nome, crefito, especialidade, cpf, celular) VALUES (?, ?, ?, ?, ?)",
        [nome, crefito, especialidade, cpf, celular]
      );
      setNome("");
      setCrefito("");
      setEspecialidade("");
      setCpf("");
      setCelular("");
      carregarFisioterapeutas();
    } catch (e) {
      alert("Erro ao salvar: " + e);
    }
  };

  const deletarFisioterapeuta = async (id: number) => {
    if (!confirm("Tem certeza que deseja excluir?")) return;
    try {
      await dbExecute("DELETE FROM fisioterapeutas WHERE id = ?", [id.toString()]);
      carregarFisioterapeutas();
    } catch (e) {
      alert("Erro ao deletar: " + e);
    }
  };

  return (
    <div>
      <form onSubmit={salvarFisioterapeuta} style={{ display: "flex", flexWrap: "wrap", gap: "1rem", marginBottom: "2rem", background: "var(--bg-panel)", padding: "1.5rem", borderRadius: "8px", boxShadow: "0 1px 3px rgba(0,0,0,0.1)" }}>
        <div style={{ flex: "1 1 200px", display: "flex", flexDirection: "column", gap: "0.5rem" }}>
          <label>Nome</label>
          <input value={nome} onChange={(e) => setNome(e.target.value)} required style={{ padding: "0.5rem" }} />
        </div>
        <div style={{ flex: "1 1 150px", display: "flex", flexDirection: "column", gap: "0.5rem" }}>
          <label>CREFITO</label>
          <input value={crefito} onChange={(e) => setCrefito(e.target.value)} required style={{ padding: "0.5rem" }} />
        </div>
        <div style={{ flex: "1 1 150px", display: "flex", flexDirection: "column", gap: "0.5rem" }}>
          <label>Especialidade</label>
          <input value={especialidade} onChange={(e) => setEspecialidade(e.target.value)} style={{ padding: "0.5rem" }} />
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
          <button type="submit" style={{ padding: "0.6rem 1.2rem", background: "var(--btn-success)", color: "white", border: "none", borderRadius: "4px", cursor: "pointer", height: "38px" }}>
            Adicionar
          </button>
        </div>
      </form>

      <table style={{ width: "100%", borderCollapse: "collapse", background: "var(--bg-panel)", boxShadow: "0 1px 3px rgba(0,0,0,0.1)" }}>
        <thead>
          <tr style={{ background: "var(--bg-base)", textAlign: "left" }}>
            <th style={{ padding: "1rem", borderBottom: "1px solid var(--border)" }}>ID</th>
            <th style={{ padding: "1rem", borderBottom: "1px solid var(--border)" }}>Nome</th>
            <th style={{ padding: "1rem", borderBottom: "1px solid var(--border)" }}>CREFITO</th>
            <th style={{ padding: "1rem", borderBottom: "1px solid var(--border)" }}>Especialidade</th>
            <th style={{ padding: "1rem", borderBottom: "1px solid var(--border)" }}>Celular</th>
            <th style={{ padding: "1rem", borderBottom: "1px solid var(--border)", width: "100px" }}>Ações</th>
          </tr>
        </thead>
        <tbody>
          {fisioterapeutas.map((f) => (
            <tr key={f.id}>
              <td style={{ padding: "1rem", borderBottom: "1px solid var(--border)" }}>{f.id}</td>
              <td style={{ padding: "1rem", borderBottom: "1px solid var(--border)" }}>{f.nome}</td>
              <td style={{ padding: "1rem", borderBottom: "1px solid var(--border)" }}>{f.crefito}</td>
              <td style={{ padding: "1rem", borderBottom: "1px solid var(--border)" }}>{f.especialidade}</td>
              <td style={{ padding: "1rem", borderBottom: "1px solid var(--border)" }}>{f.celular}</td>
              <td style={{ padding: "1rem", borderBottom: "1px solid var(--border)" }}>
                <button onClick={() => deletarFisioterapeuta(f.id)} style={{ background: "var(--btn-danger)", color: "white", border: "none", padding: "0.4rem 0.8rem", borderRadius: "4px", cursor: "pointer" }}>
                  Excluir
                </button>
              </td>
            </tr>
          ))}
          {fisioterapeutas.length === 0 && (
            <tr>
              <td colSpan={6} style={{ padding: "1rem", textAlign: "center" }}>Nenhum fisioterapeuta cadastrado.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}