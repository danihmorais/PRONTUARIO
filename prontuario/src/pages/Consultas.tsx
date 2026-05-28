import { useState, useEffect } from "react";
import { dbQuery, dbExecute } from "../db";

interface Consulta {
  id: number;
  paciente_nome: string;
  fisio_nome: string;
  data_consulta: string;
  horario: string;
  status: string;
}

interface ItemSeletor {
  id: number;
  nome: string;
}

export default function Consultas() {
  const [consultas, setConsultas] = useState<Consulta[]>([]);
  const [pacientes, setPacientes] = useState<ItemSeletor[]>([]);
  const [fisios, setFisios] = useState<ItemSeletor[]>([]);
  
  const [idPaciente, setIdPaciente] = useState("");
  const [idFisio, setIdFisio] = useState("");
  const [dataConsulta, setDataConsulta] = useState("");
  const [horario, setHorario] = useState("");
  const [status, setStatus] = useState("Pendente");
  const [observacao, setObservacao] = useState("");

  const carregarDados = async () => {
    try {
      const resConsultas = await dbQuery<Consulta>(`
        SELECT c.id, p.nome as paciente_nome, f.nome as fisio_nome, c.data_consulta, c.horario, c.status 
        FROM consultas c 
        LEFT JOIN pacientes p ON c.id_paciente = p.id 
        LEFT JOIN fisioterapeutas f ON c.id_fisioterapeuta = f.id 
        ORDER BY c.id DESC
      `);
      setConsultas(resConsultas);

      const resPacientes = await dbQuery<ItemSeletor>("SELECT id, nome FROM pacientes ORDER BY nome");
      setPacientes(resPacientes);

      const resFisios = await dbQuery<ItemSeletor>("SELECT id, nome FROM fisioterapeutas ORDER BY nome");
      setFisios(resFisios);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    carregarDados();
  }, []);

  const salvarConsulta = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!idPaciente || !idFisio) {
      alert("Selecione o paciente e o fisioterapeuta.");
      return;
    }
    try {
      await dbExecute(
        "INSERT INTO consultas (id_paciente, id_fisioterapeuta, data_consulta, horario, status, observacao) VALUES (?, ?, ?, ?, ?, ?)",
        [idPaciente, idFisio, dataConsulta, horario, status, observacao]
      );
      setIdPaciente("");
      setIdFisio("");
      setDataConsulta("");
      setHorario("");
      setStatus("Pendente");
      setObservacao("");
      carregarDados();
    } catch (e) {
      alert("Erro ao salvar: " + e);
    }
  };

  const deletarConsulta = async (id: number) => {
    if (!confirm("Tem certeza que deseja excluir?")) return;
    try {
      await dbExecute("DELETE FROM consultas WHERE id = ?", [id.toString()]);
      carregarDados();
    } catch (e) {
      alert("Erro ao deletar: " + e);
    }
  };

  return (
    <div>
      <form onSubmit={salvarConsulta} style={{ display: "flex", flexWrap: "wrap", gap: "1rem", marginBottom: "2rem", background: "#fff", padding: "1.5rem", borderRadius: "8px", boxShadow: "0 1px 3px rgba(0,0,0,0.1)" }}>
        <div style={{ flex: "1 1 200px", display: "flex", flexDirection: "column", gap: "0.5rem" }}>
          <label>Paciente</label>
          <select value={idPaciente} onChange={(e) => setIdPaciente(e.target.value)} required style={{ padding: "0.5rem" }}>
            <option value="">Selecione...</option>
            {pacientes.map((p) => (<option key={p.id} value={p.id}>{p.nome}</option>))}
          </select>
        </div>
        <div style={{ flex: "1 1 200px", display: "flex", flexDirection: "column", gap: "0.5rem" }}>
          <label>Fisioterapeuta</label>
          <select value={idFisio} onChange={(e) => setIdFisio(e.target.value)} required style={{ padding: "0.5rem" }}>
            <option value="">Selecione...</option>
            {fisios.map((f) => (<option key={f.id} value={f.id}>{f.nome}</option>))}
          </select>
        </div>
        <div style={{ flex: "1 1 150px", display: "flex", flexDirection: "column", gap: "0.5rem" }}>
          <label>Data</label>
          <input type="date" value={dataConsulta} onChange={(e) => setDataConsulta(e.target.value)} required style={{ padding: "0.5rem" }} />
        </div>
        <div style={{ flex: "1 1 100px", display: "flex", flexDirection: "column", gap: "0.5rem" }}>
          <label>Horário</label>
          <input type="time" value={horario} onChange={(e) => setHorario(e.target.value)} required style={{ padding: "0.5rem" }} />
        </div>
        <div style={{ flex: "1 1 150px", display: "flex", flexDirection: "column", gap: "0.5rem" }}>
          <label>Status</label>
          <select value={status} onChange={(e) => setStatus(e.target.value)} style={{ padding: "0.5rem" }}>
            <option value="Pendente">Pendente</option>
            <option value="Concluída">Concluída</option>
            <option value="Cancelada">Cancelada</option>
          </select>
        </div>
        <div style={{ flex: "1 1 100%", display: "flex", flexDirection: "column", gap: "0.5rem" }}>
          <label>Observação</label>
          <input value={observacao} onChange={(e) => setObservacao(e.target.value)} style={{ padding: "0.5rem" }} />
        </div>
        <div style={{ display: "flex", alignItems: "flex-end", width: "100%" }}>
          <button type="submit" style={{ padding: "0.6rem 1.2rem", background: "#10b981", color: "white", border: "none", borderRadius: "4px", cursor: "pointer" }}>
            Agendar Consulta
          </button>
        </div>
      </form>

      <table style={{ width: "100%", borderCollapse: "collapse", background: "#fff", boxShadow: "0 1px 3px rgba(0,0,0,0.1)" }}>
        <thead>
          <tr style={{ background: "#f3f4f6", textAlign: "left" }}>
            <th style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>ID</th>
            <th style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>Paciente</th>
            <th style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>Fisioterapeuta</th>
            <th style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>Data/Hora</th>
            <th style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>Status</th>
            <th style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb", width: "100px" }}>Ações</th>
          </tr>
        </thead>
        <tbody>
          {consultas.map((c) => (
            <tr key={c.id}>
              <td style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>{c.id}</td>
              <td style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>{c.paciente_nome}</td>
              <td style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>{c.fisio_nome}</td>
              <td style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>{c.data_consulta} {c.horario}</td>
              <td style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>{c.status}</td>
              <td style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb" }}>
                <button onClick={() => deletarConsulta(c.id)} style={{ background: "#ef4444", color: "white", border: "none", padding: "0.4rem 0.8rem", borderRadius: "4px", cursor: "pointer" }}>
                  Excluir
                </button>
              </td>
            </tr>
          ))}
          {consultas.length === 0 && (
            <tr>
              <td colSpan={6} style={{ padding: "1rem", textAlign: "center" }}>Nenhuma consulta agendada.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}