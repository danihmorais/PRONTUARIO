import { useState, useEffect } from "react";
import { dbQuery } from "../db";

interface Metricas {
  totalPacientes: number;
  consultasPendentes: number;
  totalProntuarios: number;
  totalFisios: number;
}

interface ConsultaRecente {
  paciente_nome: string;
  fisio_nome: string;
  data_consulta: string;
  horario: string;
  status: string;
}

const cardStyle = (cor: string): React.CSSProperties => ({
  background: "var(--bg-panel)",
  borderRadius: "12px",
  padding: "1.5rem",
  boxShadow: "var(--shadow-sm)",
  border: "1px solid var(--border)",
  flex: "1 1 180px",
  display: "flex",
  flexDirection: "column",
  gap: "0.5rem",
  borderTop: `3px solid ${cor}`,
});

export default function Dashboard() {
  const [metricas, setMetricas] = useState<Metricas>({ totalPacientes: 0, consultasPendentes: 0, totalProntuarios: 0, totalFisios: 0 });
  const [recentes, setRecentes] = useState<ConsultaRecente[]>([]);
  const [carregando, setCarregando] = useState(true);

  const carregar = async () => {
    try {
      const [pac, cons, pron, fisios, consultasRec] = await Promise.all([
        dbQuery<{ total: number }>("SELECT COUNT(*) as total FROM pacientes"),
        dbQuery<{ total: number }>("SELECT COUNT(*) as total FROM consultas WHERE status = 'Pendente'"),
        dbQuery<{ total: number }>("SELECT COUNT(*) as total FROM prontuarios"),
        dbQuery<{ total: number }>("SELECT COUNT(*) as total FROM fisioterapeutas"),
        dbQuery<ConsultaRecente>(`
          SELECT p.nome as paciente_nome, f.nome as fisio_nome, c.data_consulta, c.horario, c.status
          FROM consultas c
          LEFT JOIN pacientes p ON c.id_paciente = p.id
          LEFT JOIN fisioterapeutas f ON c.id_fisioterapeuta = f.id
          ORDER BY c.id DESC LIMIT 5
        `),
      ]);
      setMetricas({
        totalPacientes: pac[0]?.total ?? 0,
        consultasPendentes: cons[0]?.total ?? 0,
        totalProntuarios: pron[0]?.total ?? 0,
        totalFisios: fisios[0]?.total ?? 0,
      });
      setRecentes(consultasRec);
    } catch (e) {
      console.error(e);
    } finally {
      setCarregando(false);
    }
  };

  useEffect(() => {
    carregar();
    const intervalo = setInterval(carregar, 30000);
    return () => clearInterval(intervalo);
  }, []);

  const statusBadge = (status: string) => {
    const classe = status === "Pendente" ? "badge-pendente" : status === "Concluída" ? "badge-concluida" : "badge-cancelada";
    return <span className={`badge ${classe}`}>{status}</span>;
  };

  if (carregando) {
    return (
      <div style={{ display: "flex", alignItems: "center", justifyContent: "center", height: "200px", color: "var(--text-muted)" }}>
        Carregando...
      </div>
    );
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1.5rem" }}>
      <div style={{ display: "flex", gap: "1rem", flexWrap: "wrap" }}>
        <div style={cardStyle("#2563eb")}>
          <div style={{ fontSize: "12px", fontWeight: 600, color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.06em" }}>Pacientes</div>
          <div style={{ fontSize: "2.5rem", fontWeight: 700, color: "var(--text-main)", lineHeight: 1 }}>{metricas.totalPacientes}</div>
          <div style={{ fontSize: "12px", color: "var(--text-light)" }}>cadastrados</div>
        </div>
        <div style={cardStyle("#d97706")}>
          <div style={{ fontSize: "12px", fontWeight: 600, color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.06em" }}>Consultas</div>
          <div style={{ fontSize: "2.5rem", fontWeight: 700, color: "#d97706", lineHeight: 1 }}>{metricas.consultasPendentes}</div>
          <div style={{ fontSize: "12px", color: "var(--text-light)" }}>pendentes</div>
        </div>
        <div style={cardStyle("#059669")}>
          <div style={{ fontSize: "12px", fontWeight: 600, color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.06em" }}>Prontuários</div>
          <div style={{ fontSize: "2.5rem", fontWeight: 700, color: "#059669", lineHeight: 1 }}>{metricas.totalProntuarios}</div>
          <div style={{ fontSize: "12px", color: "var(--text-light)" }}>registros</div>
        </div>
        <div style={cardStyle("#7c3aed")}>
          <div style={{ fontSize: "12px", fontWeight: 600, color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.06em" }}>Fisioterapeutas</div>
          <div style={{ fontSize: "2.5rem", fontWeight: 700, color: "#7c3aed", lineHeight: 1 }}>{metricas.totalFisios}</div>
          <div style={{ fontSize: "12px", color: "var(--text-light)" }}>ativos</div>
        </div>
      </div>

      <div style={{ background: "var(--bg-panel)", borderRadius: "12px", border: "1px solid var(--border)", boxShadow: "var(--shadow-sm)", overflow: "hidden" }}>
        <div style={{ padding: "1rem 1.5rem", borderBottom: "1px solid var(--border)", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <h3 style={{ margin: 0, fontSize: "14px", fontWeight: 700, color: "var(--text-main)" }}>Consultas Recentes</h3>
          <button onClick={carregar} style={{ background: "transparent", border: "1px solid var(--border)", color: "var(--text-muted)", padding: "0.3rem 0.75rem", borderRadius: "6px", fontSize: "12px", cursor: "pointer" }}>
            Atualizar
          </button>
        </div>
        {recentes.length === 0 ? (
          <div style={{ padding: "2rem", textAlign: "center", color: "var(--text-muted)", fontSize: "14px" }}>
            Nenhuma consulta cadastrada ainda.
          </div>
        ) : (
          <table>
            <thead>
              <tr style={{ background: "var(--bg-subtle)" }}>
                <th style={{ padding: "0.75rem 1.5rem", textAlign: "left" }}>Paciente</th>
                <th style={{ padding: "0.75rem 1rem", textAlign: "left" }}>Fisioterapeuta</th>
                <th style={{ padding: "0.75rem 1rem", textAlign: "left" }}>Data / Hora</th>
                <th style={{ padding: "0.75rem 1.5rem", textAlign: "left" }}>Status</th>
              </tr>
            </thead>
            <tbody>
              {recentes.map((c, i) => (
                <tr key={i} style={{ borderTop: "1px solid var(--border)" }}>
                  <td style={{ padding: "0.75rem 1.5rem", fontWeight: 500, color: "var(--text-main)", fontSize: "14px" }}>{c.paciente_nome}</td>
                  <td style={{ padding: "0.75rem 1rem", color: "var(--text-muted)", fontSize: "14px" }}>{c.fisio_nome}</td>
                  <td style={{ padding: "0.75rem 1rem", color: "var(--text-muted)", fontSize: "13px", fontFamily: "'DM Mono', monospace" }}>{c.data_consulta} {c.horario}</td>
                  <td style={{ padding: "0.75rem 1.5rem" }}>{statusBadge(c.status)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}