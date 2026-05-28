import { useState, useEffect } from "react";
import { dbQuery, dbExecute } from "../db";

interface Prontuario {
  id: number;
  paciente_nome: string;
  data_registro: string;
  queixa: string;
  exame: string;
  diagnostico: string;
  prescricao: string;
  id_paciente: number;
}

interface ItemSeletor {
  id: number;
  nome: string;
}

const inputStyle: React.CSSProperties = { padding: "0.6rem 0.75rem" };
const labelStyle: React.CSSProperties = { fontSize: "13px", fontWeight: 600, color: "var(--text-muted)", marginBottom: "0.3rem", display: "block" };
const textareaStyle: React.CSSProperties = { padding: "0.6rem 0.75rem", minHeight: "70px", resize: "vertical" };

export default function Prontuarios() {
  const [prontuarios, setProntuarios] = useState<Prontuario[]>([]);
  const [pacientes, setPacientes] = useState<ItemSeletor[]>([]);
  const [busca, setBusca] = useState("");
  const [expandido, setExpandido] = useState<number | null>(null);
  const [editando, setEditando] = useState<Prontuario | null>(null);

  const [idPaciente, setIdPaciente] = useState("");
  const [dataRegistro, setDataRegistro] = useState(new Date().toISOString().split("T")[0]);
  const [queixa, setQueixa] = useState("");
  const [exame, setExame] = useState("");
  const [diagnostico, setDiagnostico] = useState("");
  const [prescricao, setPrescricao] = useState("");
  const [salvando, setSalvando] = useState(false);

  const carregar = async () => {
    try {
      const [resPron, resPac] = await Promise.all([
        dbQuery<Prontuario>(`
          SELECT pr.id, p.nome as paciente_nome, pr.data_registro,
                 pr.queixa, pr.exame, pr.diagnostico, pr.prescricao, pr.id_paciente
          FROM prontuarios pr
          LEFT JOIN pacientes p ON pr.id_paciente = p.id
          ORDER BY pr.id DESC
        `),
        dbQuery<ItemSeletor>("SELECT id, nome FROM pacientes ORDER BY nome"),
      ]);
      setProntuarios(resPron);
      setPacientes(resPac);
    } catch (e) { console.error(e); }
  };

  useEffect(() => { carregar(); }, []);

  const limparForm = () => {
    setIdPaciente(""); setDataRegistro(new Date().toISOString().split("T")[0]);
    setQueixa(""); setExame(""); setDiagnostico(""); setPrescricao(""); setEditando(null);
  };

  const preencherEdicao = (pr: Prontuario) => {
    setEditando(pr);
    setIdPaciente(String(pr.id_paciente));
    setDataRegistro(pr.data_registro);
    setQueixa(pr.queixa ?? "");
    setExame(pr.exame ?? "");
    setDiagnostico(pr.diagnostico ?? "");
    setPrescricao(pr.prescricao ?? "");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const salvar = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!idPaciente) { alert("Selecione o paciente."); return; }
    setSalvando(true);
    try {
      if (editando) {
        await dbExecute(
          "UPDATE prontuarios SET id_paciente=?, data_registro=?, queixa=?, exame=?, diagnostico=?, prescricao=? WHERE id=?",
          [idPaciente, dataRegistro, queixa, exame, diagnostico, prescricao, String(editando.id)]
        );
      } else {
        await dbExecute(
          "INSERT INTO prontuarios (id_paciente, data_registro, queixa, exame, diagnostico, prescricao) VALUES (?,?,?,?,?,?)",
          [idPaciente, dataRegistro, queixa, exame, diagnostico, prescricao]
        );
      }
      limparForm();
      await carregar();
    } catch (e) { alert("Erro ao salvar: " + e); }
    finally { setSalvando(false); }
  };

  const deletar = async (id: number, nome: string) => {
    if (!confirm(`Excluir prontuário de "${nome}"?`)) return;
    try { await dbExecute("DELETE FROM prontuarios WHERE id = ?", [String(id)]); carregar(); }
    catch (e) { alert("Erro ao excluir: " + e); }
  };

  const truncar = (texto: string | null | undefined, len = 50) => {
    if (!texto) return "—";
    return texto.length > len ? texto.substring(0, len) + "..." : texto;
  };

  const filtrados = prontuarios.filter(pr =>
    pr.paciente_nome?.toLowerCase().includes(busca.toLowerCase()) ||
    pr.queixa?.toLowerCase().includes(busca.toLowerCase()) ||
    pr.diagnostico?.toLowerCase().includes(busca.toLowerCase())
  );

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1.5rem" }}>
      <div style={{ background: "var(--bg-panel)", borderRadius: "12px", padding: "1.5rem", border: "1px solid var(--border)", boxShadow: "var(--shadow-sm)" }}>
        <h3 style={{ margin: "0 0 1.25rem", fontSize: "14px", fontWeight: 700, color: "var(--text-main)" }}>
          {editando ? `Editando Prontuário — ${editando.paciente_nome}` : "Novo Prontuário"}
        </h3>
        <form onSubmit={salvar} style={{ display: "flex", flexWrap: "wrap", gap: "1rem" }}>
          <div style={{ flex: "1 1 280px" }}>
            <label style={labelStyle}>Paciente *</label>
            <select value={idPaciente} onChange={e => setIdPaciente(e.target.value)} required style={inputStyle}>
              <option value="">Selecione...</option>
              {pacientes.map(p => <option key={p.id} value={p.id}>{p.nome}</option>)}
            </select>
          </div>
          <div style={{ flex: "1 1 160px" }}>
            <label style={labelStyle}>Data do Registro *</label>
            <input type="date" value={dataRegistro} onChange={e => setDataRegistro(e.target.value)} required style={inputStyle} />
          </div>
          <div style={{ flex: "1 1 100%" }}>
            <label style={labelStyle}>Queixa Principal *</label>
            <textarea value={queixa} onChange={e => setQueixa(e.target.value)} required placeholder="Descreva a queixa principal do paciente..." style={textareaStyle} />
          </div>
          <div style={{ flex: "1 1 100%" }}>
            <label style={labelStyle}>Exame Físico</label>
            <textarea value={exame} onChange={e => setExame(e.target.value)} placeholder="Resultados do exame físico..." style={textareaStyle} />
          </div>
          <div style={{ flex: "1 1 100%" }}>
            <label style={labelStyle}>Diagnóstico Cinesiológico Funcional</label>
            <textarea value={diagnostico} onChange={e => setDiagnostico(e.target.value)} placeholder="Diagnóstico..." style={textareaStyle} />
          </div>
          <div style={{ flex: "1 1 100%" }}>
            <label style={labelStyle}>Plano de Tratamento / Prescrição</label>
            <textarea value={prescricao} onChange={e => setPrescricao(e.target.value)} placeholder="Plano de tratamento e prescrições..." style={textareaStyle} />
          </div>
          <div style={{ flex: "0 0 100%", display: "flex", gap: "0.75rem" }}>
            <button type="submit" disabled={salvando} style={{ padding: "0.6rem 1.5rem", background: "var(--btn-success)", color: "white", border: "none", fontSize: "14px" }}>
              {salvando ? "Salvando..." : editando ? "Salvar Alterações" : "Salvar Prontuário"}
            </button>
            {editando && (
              <button type="button" onClick={limparForm} style={{ padding: "0.6rem 1.25rem", background: "transparent", color: "var(--text-muted)", border: "1px solid var(--border)", fontSize: "14px" }}>Cancelar</button>
            )}
          </div>
        </form>
      </div>

      <div style={{ background: "var(--bg-panel)", borderRadius: "12px", border: "1px solid var(--border)", boxShadow: "var(--shadow-sm)", overflow: "hidden" }}>
        <div style={{ padding: "1rem 1.5rem", borderBottom: "1px solid var(--border)", display: "flex", alignItems: "center", gap: "1rem" }}>
          <input value={busca} onChange={e => setBusca(e.target.value)} placeholder="Buscar por paciente, queixa ou diagnóstico..." style={{ maxWidth: "360px", padding: "0.5rem 0.75rem", fontSize: "13px" }} />
          <span style={{ fontSize: "13px", color: "var(--text-muted)", marginLeft: "auto" }}>{filtrados.length} registros</span>
        </div>
        <div style={{ overflowX: "auto" }}>
          <table>
            <thead>
              <tr style={{ background: "var(--bg-subtle)" }}>
                {["ID", "Paciente", "Data", "Queixa", "Diagnóstico", "Ações"].map(h => (
                  <th key={h} style={{ padding: "0.75rem 1rem", textAlign: "left", whiteSpace: "nowrap" }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filtrados.map((pr) => (
                <>
                  <tr key={pr.id} style={{ borderTop: "1px solid var(--border)" }}>
                    <td style={{ padding: "0.75rem 1rem", color: "var(--text-muted)", fontSize: "13px", fontFamily: "'DM Mono', monospace" }}>{pr.id}</td>
                    <td style={{ padding: "0.75rem 1rem", fontWeight: 500, color: "var(--text-main)", fontSize: "14px" }}>{pr.paciente_nome}</td>
                    <td style={{ padding: "0.75rem 1rem", color: "var(--text-muted)", fontSize: "13px", whiteSpace: "nowrap" }}>{pr.data_registro}</td>
                    <td style={{ padding: "0.75rem 1rem", color: "var(--text-muted)", fontSize: "13px", maxWidth: "220px" }}>{truncar(pr.queixa, 55)}</td>
                    <td style={{ padding: "0.75rem 1rem", color: "var(--text-muted)", fontSize: "13px", maxWidth: "200px" }}>{truncar(pr.diagnostico, 55)}</td>
                    <td style={{ padding: "0.75rem 1rem" }}>
                      <div style={{ display: "flex", gap: "0.5rem" }}>
                        <button onClick={() => setExpandido(expandido === pr.id ? null : pr.id)} style={{ background: "rgba(124,58,237,0.1)", color: "#7c3aed", border: "none", padding: "0.3rem 0.75rem", fontSize: "12px", fontWeight: 600 }}>
                          {expandido === pr.id ? "Fechar" : "Ver"}
                        </button>
                        <button onClick={() => preencherEdicao(pr)} style={{ background: "rgba(37,99,235,0.1)", color: "var(--btn-primary)", border: "none", padding: "0.3rem 0.75rem", fontSize: "12px", fontWeight: 600 }}>Editar</button>
                        <button onClick={() => deletar(pr.id, pr.paciente_nome)} style={{ background: "rgba(220,38,38,0.1)", color: "var(--btn-danger)", border: "none", padding: "0.3rem 0.75rem", fontSize: "12px", fontWeight: 600 }}>Excluir</button>
                      </div>
                    </td>
                  </tr>
                  {expandido === pr.id && (
                    <tr key={`exp-${pr.id}`} style={{ background: "var(--bg-subtle)" }}>
                      <td colSpan={6} style={{ padding: "1rem 1.5rem" }}>
                        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem" }}>
                          {[
                            { label: "Queixa Principal", valor: pr.queixa },
                            { label: "Exame Físico", valor: pr.exame },
                            { label: "Diagnóstico", valor: pr.diagnostico },
                            { label: "Plano de Tratamento", valor: pr.prescricao },
                          ].map(({ label, valor }) => (
                            <div key={label}>
                              <div style={{ fontSize: "11px", fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.05em", color: "var(--text-muted)", marginBottom: "0.3rem" }}>{label}</div>
                              <div style={{ fontSize: "13px", color: "var(--text-main)", lineHeight: 1.6, whiteSpace: "pre-wrap" }}>{valor || "—"}</div>
                            </div>
                          ))}
                        </div>
                      </td>
                    </tr>
                  )}
                </>
              ))}
              {filtrados.length === 0 && (
                <tr><td colSpan={6} style={{ padding: "2rem", textAlign: "center", color: "var(--text-muted)", fontSize: "14px" }}>
                  {busca ? "Nenhum resultado encontrado." : "Nenhum prontuário registrado."}
                </td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}