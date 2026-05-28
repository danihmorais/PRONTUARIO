import { useState, useEffect } from "react";
import { dbQuery, dbExecute } from "../db";

interface Fisioterapeuta {
  id: number;
  nome: string;
  crefito: string;
  especialidade: string;
  cpf: string;
  email: string;
  celular: string;
}

const inputStyle: React.CSSProperties = { padding: "0.6rem 0.75rem" };
const labelStyle: React.CSSProperties = { fontSize: "13px", fontWeight: 600, color: "var(--text-muted)", marginBottom: "0.3rem", display: "block" };

export default function Fisioterapeutas() {
  const [lista, setLista] = useState<Fisioterapeuta[]>([]);
  const [busca, setBusca] = useState("");
  const [editando, setEditando] = useState<Fisioterapeuta | null>(null);
  const [nome, setNome] = useState("");
  const [crefito, setCrefito] = useState("");
  const [especialidade, setEspecialidade] = useState("");
  const [cpf, setCpf] = useState("");
  const [email, setEmail] = useState("");
  const [celular, setCelular] = useState("");
  const [salvando, setSalvando] = useState(false);

  const carregar = async () => {
    try {
      const res = await dbQuery<Fisioterapeuta>("SELECT id, nome, crefito, especialidade, cpf, email, celular FROM fisioterapeutas ORDER BY nome ASC");
      setLista(res);
    } catch (e) { console.error(e); }
  };

  useEffect(() => { carregar(); }, []);

  const limparForm = () => {
    setNome(""); setCrefito(""); setEspecialidade(""); setCpf(""); setEmail(""); setCelular(""); setEditando(null);
  };

  const preencherEdicao = (f: Fisioterapeuta) => {
    setEditando(f);
    setNome(f.nome); setCrefito(f.crefito); setEspecialidade(f.especialidade ?? "");
    setCpf(f.cpf); setEmail(f.email ?? ""); setCelular(f.celular ?? "");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const salvar = async (e: React.FormEvent) => {
    e.preventDefault();
    setSalvando(true);
    try {
      if (editando) {
        await dbExecute(
          "UPDATE fisioterapeutas SET nome=?, crefito=?, especialidade=?, cpf=?, email=?, celular=? WHERE id=?",
          [nome, crefito, especialidade, cpf, email, celular, String(editando.id)]
        );
      } else {
        await dbExecute(
          "INSERT INTO fisioterapeutas (nome, crefito, especialidade, cpf, email, celular) VALUES (?,?,?,?,?,?)",
          [nome, crefito, especialidade, cpf, email, celular]
        );
      }
      limparForm();
      await carregar();
    } catch (e) { alert("Erro ao salvar: " + e); }
    finally { setSalvando(false); }
  };

  const deletar = async (id: number, nome: string) => {
    if (!confirm(`Excluir o fisioterapeuta "${nome}"?`)) return;
    try {
      await dbExecute("DELETE FROM fisioterapeutas WHERE id = ?", [String(id)]);
      carregar();
    } catch (e) { alert("Erro ao excluir: " + e); }
  };

  const filtrados = lista.filter(f =>
    f.nome?.toLowerCase().includes(busca.toLowerCase()) ||
    f.crefito?.includes(busca) ||
    f.especialidade?.toLowerCase().includes(busca.toLowerCase())
  );

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1.5rem" }}>
      <div style={{ background: "var(--bg-panel)", borderRadius: "12px", padding: "1.5rem", border: "1px solid var(--border)", boxShadow: "var(--shadow-sm)" }}>
        <h3 style={{ margin: "0 0 1.25rem", fontSize: "14px", fontWeight: 700, color: "var(--text-main)" }}>
          {editando ? `Editando: ${editando.nome}` : "Novo Fisioterapeuta"}
        </h3>
        <form onSubmit={salvar} style={{ display: "flex", flexWrap: "wrap", gap: "1rem" }}>
          <div style={{ flex: "1 1 220px" }}>
            <label style={labelStyle}>Nome completo *</label>
            <input value={nome} onChange={e => setNome(e.target.value)} required placeholder="Nome do fisioterapeuta" style={inputStyle} />
          </div>
          <div style={{ flex: "1 1 150px" }}>
            <label style={labelStyle}>CREFITO *</label>
            <input value={crefito} onChange={e => setCrefito(e.target.value)} required placeholder="Ex: 12345-F" style={inputStyle} />
          </div>
          <div style={{ flex: "1 1 180px" }}>
            <label style={labelStyle}>Especialidade</label>
            <input value={especialidade} onChange={e => setEspecialidade(e.target.value)} placeholder="Ex: Ortopedia" style={inputStyle} />
          </div>
          <div style={{ flex: "1 1 160px" }}>
            <label style={labelStyle}>CPF *</label>
            <input value={cpf} onChange={e => setCpf(e.target.value)} required placeholder="000.000.000-00" style={inputStyle} />
          </div>
          <div style={{ flex: "1 1 200px" }}>
            <label style={labelStyle}>E-mail</label>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="email@exemplo.com" style={inputStyle} />
          </div>
          <div style={{ flex: "1 1 150px" }}>
            <label style={labelStyle}>Celular</label>
            <input value={celular} onChange={e => setCelular(e.target.value)} placeholder="(00) 00000-0000" style={inputStyle} />
          </div>
          <div style={{ flex: "0 0 100%", display: "flex", gap: "0.75rem" }}>
            <button type="submit" disabled={salvando} style={{ padding: "0.6rem 1.5rem", background: "var(--btn-success)", color: "white", border: "none", fontSize: "14px" }}>
              {salvando ? "Salvando..." : editando ? "Salvar Alterações" : "Adicionar"}
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
          <input value={busca} onChange={e => setBusca(e.target.value)} placeholder="Buscar por nome, CREFITO ou especialidade..." style={{ maxWidth: "340px", padding: "0.5rem 0.75rem", fontSize: "13px" }} />
          <span style={{ fontSize: "13px", color: "var(--text-muted)", marginLeft: "auto" }}>{filtrados.length} registros</span>
        </div>
        <div style={{ overflowX: "auto" }}>
          <table>
            <thead>
              <tr style={{ background: "var(--bg-subtle)" }}>
                {["ID", "Nome", "CREFITO", "Especialidade", "CPF", "Celular", "Ações"].map(h => (
                  <th key={h} style={{ padding: "0.75rem 1rem", textAlign: "left", whiteSpace: "nowrap" }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filtrados.map((f) => (
                <tr key={f.id} style={{ borderTop: "1px solid var(--border)" }}>
                  <td style={{ padding: "0.75rem 1rem", color: "var(--text-muted)", fontSize: "13px", fontFamily: "'DM Mono', monospace" }}>{f.id}</td>
                  <td style={{ padding: "0.75rem 1rem", fontWeight: 500, color: "var(--text-main)", fontSize: "14px" }}>{f.nome}</td>
                  <td style={{ padding: "0.75rem 1rem", color: "var(--text-muted)", fontSize: "13px", fontFamily: "'DM Mono', monospace" }}>{f.crefito}</td>
                  <td style={{ padding: "0.75rem 1rem", color: "var(--text-muted)", fontSize: "13px" }}>{f.especialidade || "—"}</td>
                  <td style={{ padding: "0.75rem 1rem", color: "var(--text-muted)", fontSize: "13px", fontFamily: "'DM Mono', monospace" }}>{f.cpf}</td>
                  <td style={{ padding: "0.75rem 1rem", color: "var(--text-muted)", fontSize: "13px" }}>{f.celular || "—"}</td>
                  <td style={{ padding: "0.75rem 1rem" }}>
                    <div style={{ display: "flex", gap: "0.5rem" }}>
                      <button onClick={() => preencherEdicao(f)} style={{ background: "rgba(37,99,235,0.1)", color: "var(--btn-primary)", border: "none", padding: "0.3rem 0.75rem", fontSize: "12px", fontWeight: 600 }}>Editar</button>
                      <button onClick={() => deletar(f.id, f.nome)} style={{ background: "rgba(220,38,38,0.1)", color: "var(--btn-danger)", border: "none", padding: "0.3rem 0.75rem", fontSize: "12px", fontWeight: 600 }}>Excluir</button>
                    </div>
                  </td>
                </tr>
              ))}
              {filtrados.length === 0 && (
                <tr><td colSpan={7} style={{ padding: "2rem", textAlign: "center", color: "var(--text-muted)", fontSize: "14px" }}>
                  {busca ? "Nenhum resultado encontrado." : "Nenhum fisioterapeuta cadastrado."}
                </td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}