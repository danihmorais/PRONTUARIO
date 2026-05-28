import { useState, useEffect } from "react";
import { dbQuery, dbExecute } from "../db";

interface Consulta {
  id: number;
  paciente_nome: string;
  fisio_nome: string;
  data_consulta: string;
  horario: string;
  status: string;
  observacao: string;
  id_paciente: number;
  id_fisioterapeuta: number;
}

interface ItemSeletor {
  id: number;
  nome: string;
}

const inputStyle: React.CSSProperties = { padding: "0.6rem 0.75rem" };
const labelStyle: React.CSSProperties = { fontSize: "13px", fontWeight: 600, color: "var(--text-muted)", marginBottom: "0.3rem", display: "block" };

export default function Consultas() {
  const [consultas, setConsultas] = useState<Consulta[]>([]);
  const [pacientes, setPacientes] = useState<ItemSeletor[]>([]);
  const [fisios, setFisios] = useState<ItemSeletor[]>([]);
  const [filtroStatus, setFiltroStatus] = useState("Todos");
  const [editando, setEditando] = useState<Consulta | null>(null);

  const [idPaciente, setIdPaciente] = useState("");
  const [idFisio, setIdFisio] = useState("");
  const [dataConsulta, setDataConsulta] = useState("");
  const [horario, setHorario] = useState("");
  const [status, setStatus] = useState("Pendente");
  const [observacao, setObservacao] = useState("");
  const [salvando, setSalvando] = useState(false);

  const carregar = async () => {
    try {
      const [resC, resP, resF] = await Promise.all([
        dbQuery<Consulta>(`
          SELECT c.id, p.nome as paciente_nome, f.nome as fisio_nome,
                 c.data_consulta, c.horario, c.status, c.observacao,
                 c.id_paciente, c.id_fisioterapeuta
          FROM consultas c
          LEFT JOIN pacientes p ON c.id_paciente = p.id
          LEFT JOIN fisioterapeutas f ON c.id_fisioterapeuta = f.id
          ORDER BY c.data_consulta DESC, c.horario DESC
        `),
        dbQuery<ItemSeletor>("SELECT id, nome FROM pacientes ORDER BY nome"),
        dbQuery<ItemSeletor>("SELECT id, nome FROM fisioterapeutas ORDER BY nome"),
      ]);
      setConsultas(resC);
      setPacientes(resP);
      setFisios(resF);
    } catch (e) { console.error(e); }
  };

  useEffect(() => { carregar(); }, []);

  const limparForm = () => {
    setIdPaciente(""); setIdFisio(""); setDataConsulta(""); setHorario("");
    setStatus("Pendente"); setObservacao(""); setEditando(null);
  };

  const preencherEdicao = (c: Consulta) => {
    setEditando(c);
    setIdPaciente(String(c.id_paciente)); setIdFisio(String(c.id_fisioterapeuta));
    setDataConsulta(c.data_consulta); setHorario(c.horario);
    setStatus(c.status); setObservacao(c.observacao ?? "");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const salvar = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!idPaciente || !idFisio) { alert("Selecione paciente e fisioterapeuta."); return; }
    setSalvando(true);
    try {
      if (editando) {
        await dbExecute(
          "UPDATE consultas SET id_paciente=?, id_fisioterapeuta=?, data_consulta=?, horario=?, status=?, observacao=? WHERE id=?",
          [idPaciente, idFisio, dataConsulta, horario, status, observacao, String(editando.id)]
        );
      } else {
        await dbExecute(
          "INSERT INTO consultas (id_paciente, id_fisioterapeuta, data_consulta, horario, status, observacao) VALUES (?,?,?,?,?,?)",
          [idPaciente, idFisio, dataConsulta, horario, status, observacao]
        );
      }
      limparForm();
      await carregar();
    } catch (e) { alert("Erro ao salvar: " + e); }
    finally { setSalvando(false); }
  };

  const deletar = async (id: number) => {
    if (!confirm("Excluir esta consulta?")) return;
    try { await dbExecute("DELETE FROM consultas WHERE id = ?", [String(id)]); carregar(); }
    catch (e) { alert("Erro ao excluir: " + e); }
  };

  const statusBadge = (s: string) => {
    const cls = s === "Pendente" ? "badge-pendente" : s === "Concluída" ? "badge-concluida" : "badge-cancelada";
    return <span className={`badge ${cls}`}>{s}</span>;
  };

  const filtradas = filtroStatus === "Todos" ? consultas : consultas.filter(c => c.status === filtroStatus);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1.5rem" }}>
      <div style={{ background: "var(--bg-panel)", borderRadius: "12px", padding: "1.5rem", border: "1px solid var(--border)", boxShadow: "var(--shadow-sm)" }}>
        <h3 style={{ margin: "0 0 1.25rem", fontSize: "14px", fontWeight: 700, color: "var(--text-main)" }}>
          {editando ? "Editar Consulta" : "Agendar Consulta"}
        </h3>
        <form onSubmit={salvar} style={{ display: "flex", flexWrap: "wrap", gap: "1rem" }}>
          <div style={{ flex: "1 1 200px" }}>
            <label style={labelStyle}>Paciente *</label>
            <select value={idPaciente} onChange={e => setIdPaciente(e.target.value)} required style={inputStyle}>
              <option value="">Selecione...</option>
              {pacientes.map(p => <option key={p.id} value={p.id}>{p.nome}</option>)}
            </select>
          </div>
          <div style={{ flex: "1 1 200px" }}>
            <label style={labelStyle}>Fisioterapeuta *</label>
            <select value={idFisio} onChange={e => setIdFisio(e.target.value)} required style={inputStyle}>
              <option value="">Selecione...</option>
              {fisios.map(f => <option key={f.id} value={f.id}>{f.nome}</option>)}
            </select>
          </div>
          <div style={{ flex: "1 1 150px" }}>
            <label style={labelStyle}>Data *</label>
            <input type="date" value={dataConsulta} onChange={e => setDataConsulta(e.target.value)} required style={inputStyle} />
          </div>
          <div style={{ flex: "1 1 120px" }}>
            <label style={labelStyle}>Horário *</label>
            <input type="time" value={horario} onChange={e => setHorario(e.target.value)} required style={inputStyle} />
          </div>
          <div style={{ flex: "1 1 150px" }}>
            <label style={labelStyle}>Status</label>
            <select value={status} onChange={e => setStatus(e.target.value)} style={inputStyle}>
              <option value="Pendente">Pendente</option>
              <option value="Concluída">Concluída</option>
              <option value="Cancelada">Cancelada</option>
            </select>
          </div>
          <div style={{ flex: "1 1 100%" }}>
            <label style={labelStyle}>Observação</label>
            <input value={observacao} onChange={e => setObservacao(e.target.value)} placeholder="Observações sobre a consulta..." style={inputStyle} />
          </div>
          <div style={{ flex: "0 0 100%", display: "flex", gap: "0.75rem" }}>
            <button type="submit" disabled={salvando} style={{ padding: "0.6rem 1.5rem", background: "var(--btn-success)", color: "white", border: "none", fontSize: "14px" }}>
              {salvando ? "Salvando..." : editando ? "Salvar Alterações" : "Agendar"}
            </button>
            {editando && (
              <button type="button" onClick={limparForm} style={{ padding: "0.6rem 1.25rem", background: "transparent", color: "var(--text-muted)", border: "1px solid var(--border)", fontSize: "14px" }}>Cancelar</button>
            )}
          </div>
        </form>
      </div>

      <div style={{ background: "var(--bg-panel)", borderRadius: "12px", border: "1px solid var(--border)", boxShadow: "var(--shadow-sm)", overflow: "hidden" }}>
        <div style={{ padding: "1rem 1.5rem", borderBottom: "1px solid var(--border)", display: "flex", alignItems: "center", gap: "0.5rem", flexWrap: "wrap" }}>
          {["Todos", "Pendente", "Concluída", "Cancelada"].map(s => (
            <button
              key={s}
              onClick={() => setFiltroStatus(s)}
              style={{
                padding: "0.35rem 1rem",
                border: "1px solid var(--border)",
                background: filtroStatus === s ? "var(--btn-primary)" : "transparent",
                color: filtroStatus === s ? "white" : "var(--text-muted)",
                borderRadius: "999px",
                fontSize: "12px",
                fontWeight: 600,
              }}
            >{s}</button>
          ))}
          <span style={{ fontSize: "13px", color: "var(--text-muted)", marginLeft: "auto" }}>{filtradas.length} consultas</span>
        </div>
        <div style={{ overflowX: "auto" }}>
          <table>
            <thead>
              <tr style={{ background: "var(--bg-subtle)" }}>
                {["ID", "Paciente", "Fisioterapeuta", "Data / Hora", "Status", "Observação", "Ações"].map(h => (
                  <th key={h} style={{ padding: "0.75rem 1rem", textAlign: "left", whiteSpace: "nowrap" }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filtradas.map((c) => (
                <tr key={c.id} style={{ borderTop: "1px solid var(--border)" }}>
                  <td style={{ padding: "0.75rem 1rem", color: "var(--text-muted)", fontSize: "13px", fontFamily: "'DM Mono', monospace" }}>{c.id}</td>
                  <td style={{ padding: "0.75rem 1rem", fontWeight: 500, color: "var(--text-main)", fontSize: "14px" }}>{c.paciente_nome}</td>
                  <td style={{ padding: "0.75rem 1rem", color: "var(--text-muted)", fontSize: "13px" }}>{c.fisio_nome}</td>
                  <td style={{ padding: "0.75rem 1rem", color: "var(--text-muted)", fontSize: "13px", fontFamily: "'DM Mono', monospace", whiteSpace: "nowrap" }}>{c.data_consulta} {c.horario}</td>
                  <td style={{ padding: "0.75rem 1rem" }}>{statusBadge(c.status)}</td>
                  <td style={{ padding: "0.75rem 1rem", color: "var(--text-muted)", fontSize: "13px", maxWidth: "200px", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{c.observacao || "—"}</td>
                  <td style={{ padding: "0.75rem 1rem" }}>
                    <div style={{ display: "flex", gap: "0.5rem" }}>
                      <button onClick={() => preencherEdicao(c)} style={{ background: "rgba(37,99,235,0.1)", color: "var(--btn-primary)", border: "none", padding: "0.3rem 0.75rem", fontSize: "12px", fontWeight: 600 }}>Editar</button>
                      <button onClick={() => deletar(c.id)} style={{ background: "rgba(220,38,38,0.1)", color: "var(--btn-danger)", border: "none", padding: "0.3rem 0.75rem", fontSize: "12px", fontWeight: 600 }}>Excluir</button>
                    </div>
                  </td>
                </tr>
              ))}
              {filtradas.length === 0 && (
                <tr><td colSpan={7} style={{ padding: "2rem", textAlign: "center", color: "var(--text-muted)", fontSize: "14px" }}>
                  Nenhuma consulta encontrada.
                </td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}