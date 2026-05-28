import { useState } from "react";
import { dbQuery } from "../db";

const tabelas = [
  { id: "pacientes", label: "Pacientes", descricao: "Nome, CPF, contato e dados pessoais" },
  { id: "fisioterapeutas", label: "Fisioterapeutas", descricao: "CREFITO, especialidade e contato" },
  { id: "funcionarios", label: "Funcionários", descricao: "Cargo, CPF e dados cadastrais" },
  { id: "consultas", label: "Consultas", descricao: "Agendamentos e status" },
  { id: "prontuarios", label: "Prontuários", descricao: "Queixas, diagnósticos e prescrições" },
];

export default function Exportacao() {
  const [status, setStatus] = useState<Record<string, string>>({});
  const [exportando, setExportando] = useState<string | null>(null);

  const exportarCSV = async (tabela: string, label: string) => {
    setExportando(tabela);
    setStatus(prev => ({ ...prev, [tabela]: "Carregando dados..." }));
    try {
      const dados = await dbQuery<any>(`SELECT * FROM ${tabela}`);
      if (dados.length === 0) {
        setStatus(prev => ({ ...prev, [tabela]: `⚠ Tabela vazia — nenhum dado para exportar.` }));
        return;
      }

      const cabecalhos = Object.keys(dados[0]).join(",");
      const linhas = dados.map(linha =>
        Object.values(linha).map(v => {
          if (v === null || v === undefined) return '""';
          const str = String(v).replace(/"/g, '""');
          return `"${str}"`;
        }).join(",")
      );

      const bom = "\uFEFF";
      const csv = bom + [cabecalhos, ...linhas].join("\n");
      const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      const dataHoje = new Date().toLocaleDateString("pt-BR").replace(/\//g, "-");
      link.href = url;
      link.setAttribute("download", `prontuario_${tabela}_${dataHoje}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);

      setStatus(prev => ({ ...prev, [tabela]: `✓ ${dados.length} registros exportados com sucesso.` }));
    } catch (e) {
      setStatus(prev => ({ ...prev, [tabela]: `✗ Erro: ${String(e)}` }));
    } finally {
      setExportando(null);
    }
  };

  const exportarTudo = async () => {
    for (const t of tabelas) {
      await exportarCSV(t.id, t.label);
    }
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1.5rem" }}>
      <div style={{ background: "var(--bg-panel)", borderRadius: "12px", padding: "1.5rem", border: "1px solid var(--border)", boxShadow: "var(--shadow-sm)" }}>
        <h3 style={{ margin: "0 0 0.5rem", fontSize: "14px", fontWeight: 700, color: "var(--text-main)" }}>Exportação de Dados</h3>
        <p style={{ margin: "0 0 1.25rem", fontSize: "13px", color: "var(--text-muted)" }}>
          Os arquivos CSV exportados incluem BOM UTF-8 para compatibilidade com Excel. Selecione as tabelas desejadas ou exporte tudo de uma vez.
        </p>
        <button
          onClick={exportarTudo}
          disabled={exportando !== null}
          style={{
            padding: "0.65rem 1.5rem",
            background: "var(--btn-primary)",
            color: "white",
            border: "none",
            fontSize: "14px",
            fontWeight: 600,
          }}
        >
          {exportando ? "Exportando..." : "Exportar Tudo"}
        </button>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))", gap: "1rem" }}>
        {tabelas.map((t) => {
          const msg = status[t.id];
          const sucesso = msg?.startsWith("✓");
          const erro = msg?.startsWith("✗");
          return (
            <div key={t.id} style={{
              background: "var(--bg-panel)",
              borderRadius: "12px",
              padding: "1.25rem",
              border: "1px solid var(--border)",
              boxShadow: "var(--shadow-sm)",
              display: "flex",
              flexDirection: "column",
              gap: "0.75rem",
            }}>
              <div>
                <div style={{ fontWeight: 700, fontSize: "15px", color: "var(--text-main)", marginBottom: "0.25rem" }}>{t.label}</div>
                <div style={{ fontSize: "12px", color: "var(--text-muted)" }}>{t.descricao}</div>
              </div>
              {msg && (
                <div style={{
                  fontSize: "12px",
                  padding: "0.4rem 0.75rem",
                  borderRadius: "6px",
                  background: sucesso ? "rgba(5,150,105,0.1)" : erro ? "rgba(220,38,38,0.1)" : "rgba(59,130,246,0.1)",
                  color: sucesso ? "#059669" : erro ? "#dc2626" : "var(--btn-primary)",
                  fontWeight: 500,
                }}>
                  {msg}
                </div>
              )}
              <button
                onClick={() => exportarCSV(t.id, t.label)}
                disabled={exportando !== null}
                style={{
                  padding: "0.55rem 1rem",
                  background: "rgba(37,99,235,0.1)",
                  color: "var(--btn-primary)",
                  border: "1px solid rgba(37,99,235,0.2)",
                  fontSize: "13px",
                  fontWeight: 600,
                  marginTop: "auto",
                }}
              >
                {exportando === t.id ? "Exportando..." : "Exportar CSV"}
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
}