import { useState, useEffect } from "react";
import { dbQuery, dbExecute } from "../db";

interface Prontuario {
  id: number;
  paciente_nome: string;
  data_registro: string;
  queixa: string;
  diagnostico: string;
}

interface ItemSeletor {
  id: number;
  nome: string;
}

export default function Prontuarios() {
  const [prontuarios, setProntuarios] = useState<Prontuario[]>([]);
  const [pacientes, setPacientes] = useState<ItemSeletor[]>([]);
  
  const [idPaciente, setIdPaciente] = useState("");
  const [dataRegistro, setDataRegistro] = useState(new Date().toISOString().split("T")[0]);
  const [queixa, setQueixa] = useState("");
  const [exame, setExame] = useState("");
  const [diagnostico, setDiagnostico] = useState("");
  const [prescricao, setPrescricao] = useState("");

  const carregarDados = async () => {
    try {
      const resProntuarios = await dbQuery<Prontuario>(`
        SELECT pr.id, p.nome as paciente_nome, pr.data_registro, pr.queixa, pr.diagnostico 
        FROM prontuarios pr 
        LEFT JOIN pacientes p ON pr.id_paciente = p.id 
        ORDER BY pr.id DESC
      `);
      setProntuarios(resProntuarios);

      const resPacientes = await dbQuery<ItemSeletor>("SELECT id, nome FROM pacientes ORDER BY nome");
      setPacientes(resPacientes);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    carregarDados();
  }, []);

  const salvarProntuario = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!idPaciente) {
      alert("Selecione o paciente.");
      return;
    }
    try {
      await dbExecute(
        "INSERT INTO prontuarios (id_paciente, data_registro, queixa, exame, diagnostico, prescricao) VALUES (?, ?, ?, ?, ?, ?)",
        [idPaciente, dataRegistro, queixa, exame, diagnostico, prescricao]
      );
      setIdPaciente("");
      setQueixa("");
      setExame("");
      setDiagnostico("");
      setPrescricao("");
      carregarDados();
    } catch (e) {
      alert("Erro ao salvar: " + e);
    }
  };

  const deletarProntuario = async (id: number) => {
    if (!confirm("Tem certeza que deseja excluir?")) return;
    try {
      await dbExecute("DELETE FROM prontuarios WHERE id = ?", [id.toString()]);
      carregarDados();
    } catch (e) {
      alert("Erro ao deletar: " + e);
    }
  };

  return (
    <div>
      <form onSubmit={salvarProntuario} style={{ display: "flex", flexWrap: "wrap", gap: "1rem", marginBottom: "2rem", background: "#fff", padding: "1.5rem", borderRadius: "8px", boxShadow: "0 1px 3px rgba(0,0,0,0.1)" }}>
        <div style={{ flex: "1 1 300px", display: "flex", flexDirection: "column", gap: "0.5rem" }}>
          <label>Paciente</label>
          <select value={idPaciente} onChange={(e) => setIdPaciente(e.target.value)} required style={{ padding: "0.5rem" }}>
            <option value="">Selecione...</option>
            {pacientes.map((p) => (<option key={p.id} value={p.id}>{p.nome}</option>))}
          </select>
        </div>
        <div style={{ flex: "1 1 150px", display: "flex", flexDirection: "column", gap: "0.5rem" }}>
          <label>Data do Registro</label>
          <input type="date" value={dataRegistro} onChange={(e) => setDataRegistro(e.target.value)} required style={{ padding: "0.5rem" }} />
        </div>
        <div style={{ flex: "1 1 100%", display: "flex", flexDirection: "column", gap: "0.5rem" }}>
          <label>Queixa Principal</label>
          <textarea value={queixa} onChange={(e) => setQueixa(e.target.value)} required style={{ padding: "0.5rem", minHeight: "60px" }} />
        </div>
        <div style={{ flex: "1 1 100%", display: "flex", flexDirection: "column", gap: "0.5rem" }}>
          <label>Exame Físico</label>
          <textarea value={exame} onChange={(e) => setExame(e.target.value)} style={{ padding: "0.5rem", minHeight: "60px" }} />
        </div>
        <div style={{ flex: "1 1 100%", display: "flex", flexDirection: "column", gap: "0.5rem" }}>
          <label>Diagnóstico Cinesiológico Funcional</label>
          <textarea value={diagnostico} onChange={(e) => setDiagnostico(e.target.value)} style={{ padding: "0.5rem", minHeight: "60px" }} />
        </div>
        <div style={{ flex: "1 1 100%", display: "flex", flexDirection: "column", gap: "0.5rem" }}>
          <label>Plano de Tratamento / Prescrição</label>
          <textarea value={prescricao} onChange={(e) => setPrescricao(e.target.value)} style={{ padding: "0.5rem", minHeight: "60px" }} />
        </div>
        <div style={{ display: "flex", alignItems: "flex-end", width: "100%", marginTop: "0.5rem" }}>
          <button type="submit" style={{ padding: "0.6rem 1.2rem", background: "#10b981", color: "white", border: "none", borderRadius: "4px", cursor: "pointer" }}>
            Salvar Prontuário
          </button>
        </div>
      </form>

      <table style={{ width: "100%", borderCollapse: "collapse", background: "#fff", boxShadow: "0 1px 3px rgba(0,0,0,0.1)" }}>
        <thead>
          <tr style={{ background: "#f3f4f6", textAlign: "left" }}>
            <th style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>ID</th>
            <th style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>Paciente</th>
            <th style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>Data</th>
            <th style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>Queixa / Diagnóstico Resumido</th>
            <th style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb", width: "100px" }}>Ações</th>
          </tr>
        </thead>
        <tbody>
          {prontuarios.map((pr) => (
            <tr key={pr.id}>
              <td style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>{pr.id}</td>
              <td style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>{pr.paciente_nome}</td>
              <td style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>{pr.data_registro}</td>
              <td style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>{pr.queixa.substring(0, 30)}...</td>
              <td style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>
                <button onClick={() => deletarProntuario(pr.id)} style={{ background: "#ef4444", color: "white", border: "none", padding: "0.4rem 0.8rem", borderRadius: "4px", cursor: "pointer" }}>
                  Excluir
                </button>
              </td>
            </tr>
          ))}
          {prontuarios.length === 0 && (
            <tr>
              <td colSpan={5} style={{ padding: "1rem", textAlign: "center" }}>Nenhum prontuário registrado.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}