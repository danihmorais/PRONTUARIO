import { useState, useEffect } from "react";
import { dbQuery, dbExecute } from "../db";

interface Paciente {
  id: number;
  nome: string;
  cpf: string;
  celular: string;
  email: string;
  data_nascimento: string;
}

const inputStyle: React.CSSProperties = { padding: "0.6rem 0.75rem" };
const labelStyle: React.CSSProperties = { fontSize: "13px", fontWeight: 600, color: "var(--text-muted)", marginBottom: "0.3rem", display: "block" };

export default function Pacientes() {
  const [pacientes, setPacientes] = useState<Paciente[]>([]);
  const [busca, setBusca] = useState("");
  const [editando, setEditando] = useState<Paciente | null>(null);
  const [nome, setNome] = useState("");
  const [cpf, setCpf] = useState("");
  const [celular, setCelular] = useState("");
  const [email, setEmail] = useState("");
  const [dataNasc, setDataNasc] = useState("");
  const [salvando, setSalvando] = useState(false);

  const carregar = async () => {
    try {
      const res = await dbQuery<Paciente>("SELECT id, nome, cpf, celular, email, data_nascimento FROM pacientes ORDER BY nome ASC");
      setPacientes(res);
    } catch (e) { console.error(e); }
  };

  useEffect(() => { carregar(); }, []);

  const limparForm = () => {
    setNome(""); setCpf(""); setCelular(""); setEmail(""); setDataNasc(""); setEditando(null);
  };

  const preencherEdicao = (p: Paciente) => {
    setEditando(p);
    setNome(p.nome); setCpf(p.cpf); setCelular(p.celular ?? ""); setEmail(p.email ?? ""); setDataNasc(p.data_nascimento ?? "");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const salvar = async (e: React.FormEvent) => {
    e.preventDefault();
    setSalvando(true);
    try {
      if (editando) {
        await dbExecute(
          "UPDATE pacientes SET nome=?, cpf=?, celular=?, email=?, data_nascimento=? WHERE id=?",
          [nome, cpf, celular, email, dataNasc, String(editando.id)]
        );
      } else {
        await dbExecute(
          "INSERT INTO pacientes (nome, cpf, celular, email, data_nascimento) VALUES (?,?,?,?,?)",
          [nome, cpf, celular, email, dataNasc]
        );
      }
      limparForm();
      await carregar();
    } catch (e) { alert("Erro ao salvar: " + e); }
    finally { setSalvando(false); }
  };

  const deletar = async (id: number, nome: string) => {
    if (!confirm(`Excluir o paciente "${nome}"? Esta ação não pode ser desfeita.`)) return;
    try {
      await dbExecute("DELETE FROM pacientes WHERE id = ?", [String(id)]);
      carregar();
    } catch (e) { alert("Erro ao excluir: " + e); }
  };

  const filtrados = pacientes.filter(p =>
    p.nome?.toLowerCase().includes(busca.toLowerCase()) ||
    p.cpf?.includes(busca) ||
    p.celular?.includes(busca)
  );

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1.5rem" }}>
      <div style={{ background: "var(--bg-panel)", borderRadius: "12px", padding: "1.5rem", border: "1px solid var(--border)", boxShadow: "var(--shadow-sm)" }}>
        <h3 style={{ margin: "0 0 1.25rem", fontSize: "14px", fontWeight: 700, color: "var(--text-main)" }}>
          {editando ? `Editando: ${editando.nome}` : "Novo Paciente"}
        </h3>
        <form onSubmit={salvar} style={{ display: "flex", flexWrap: "wrap", gap: "1rem" }}>
          <div style={{ flex: "1 1 220px" }}>
            <label style={labelStyle}>Nome completo *</label>
            <input value={nome} onChange={e => setNome(e.target.value)} required placeholder="Nome do paciente" style={inputStyle} />
          </div>
          <div style={{ flex: "1 1 160px" }}>
            <label style={labelStyle}>CPF *</label>
            <input value={cpf} onChange={e => setCpf(e.target.value)} required placeholder="000.000.000-00" style={inputStyle} />
          </div>
          <div style={{ flex: "1 1 150px" }}>
            <label style={labelStyle}>Celular</label>
            <input value={celular} onChange={e => setCelular(e.target.value)} placeholder="(00) 00000-0000" style={inputStyle} />
          </div>
          <div style={{ flex: "1 1 200px" }}>
            <label style={labelStyle}>E-mail</label>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="email@exemplo.com" style={inputStyle} />
          </div>
          <div style={{ flex: "1 1 150px" }}>
            <label style={labelStyle}>Data de Nascimento</label>
            <input type="date" value={dataNasc} onChange={e => setDataNasc(e.target.value)} style={inputStyle} />
          </div>
          <div style={{ flex: "0 0 100%", display: "flex", gap: "0.75rem" }}>
            <button type="submit" disabled={salvando} style={{ padding: "0.6rem 1.5rem", background: "var(--btn-success)", color: "white", border: "none", fontSize: "14px" }}>
              {salvando ? "Salvando..." : editando ? "Salvar Alterações" : "Adicionar Paciente"}
            </button>
            {editando && (
              <button type="button" onClick={limparForm} style={{ padding: "0.6rem 1.25rem", background: "transparent", color: "var(--text-muted)", border: "1px solid var(--border)", fontSize: "14px" }}>
                Cancelar
              </button>
            )}
          </div>
        </form>
      </div>

      <div style={{ background: "var(--bg-panel)", borderRadius: "12px", border: "1px solid var(--border)", boxShadow: "var(--shadow-sm)", overflow: "hidden" }}>
        <div style={{ padding: "1rem 1.5rem", borderBottom: "1px solid var(--border)", display: "flex", alignItems: "center", gap: "1rem" }}>
          <input
            value={busca}
            onChange={e => setBusca(e.target.value)}
            placeholder="Buscar por nome, CPF ou celular..."
            style={{ maxWidth: "320px", padding: "0.5rem 0.75rem", fontSize: "13px" }}
          />
          <span style={{ fontSize: "13px", color: "var(--text-muted)", marginLeft: "auto" }}>
            {filtrados.length} paciente{filtrados.length !== 1 ? "s" : ""}
          </span>
        </div>
        <div style={{ overflowX: "auto" }}>
          <table>
            <thead>
              <tr style={{ background: "var(--bg-subtle)" }}>
                {["ID", "Nome", "CPF", "Celular", "E-mail", "Nascimento", "Ações"].map(h => (
                  <th key={h} style={{ padding: "0.75rem 1rem", textAlign: "left", whiteSpace: "nowrap" }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filtrados.map((p) => (
                <tr key={p.id} style={{ borderTop: "1px solid var(--border)" }}>
                  <td style={{ padding: "0.75rem 1rem", color: "var(--text-muted)", fontSize: "13px", fontFamily: "'DM Mono', monospace" }}>{p.id}</td>
                  <td style={{ padding: "0.75rem 1rem", fontWeight: 500, color: "var(--text-main)", fontSize: "14px" }}>{p.nome}</td>
                  <td style={{ padding: "0.75rem 1rem", color: "var(--text-muted)", fontSize: "13px", fontFamily: "'DM Mono', monospace" }}>{p.cpf}</td>
                  <td style={{ padding: "0.75rem 1rem", color: "var(--text-muted)", fontSize: "13px" }}>{p.celular || "—"}</td>
                  <td style={{ padding: "0.75rem 1rem", color: "var(--text-muted)", fontSize: "13px" }}>{p.email || "—"}</td>
                  <td style={{ padding: "0.75rem 1rem", color: "var(--text-muted)", fontSize: "13px" }}>{p.data_nascimento || "—"}</td>
                  <td style={{ padding: "0.75rem 1rem" }}>
                    <div style={{ display: "flex", gap: "0.5rem" }}>
                      <button onClick={() => preencherEdicao(p)} style={{ background: "rgba(37,99,235,0.1)", color: "var(--btn-primary)", border: "none", padding: "0.3rem 0.75rem", fontSize: "12px", fontWeight: 600 }}>
                        Editar
                      </button>
                      <button onClick={() => deletar(p.id, p.nome)} style={{ background: "rgba(220,38,38,0.1)", color: "var(--btn-danger)", border: "none", padding: "0.3rem 0.75rem", fontSize: "12px", fontWeight: 600 }}>
                        Excluir
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
              {filtrados.length === 0 && (
                <tr>
                  <td colSpan={7} style={{ padding: "2rem", textAlign: "center", color: "var(--text-muted)", fontSize: "14px" }}>
                    {busca ? "Nenhum paciente encontrado para esta busca." : "Nenhum paciente cadastrado."}
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}