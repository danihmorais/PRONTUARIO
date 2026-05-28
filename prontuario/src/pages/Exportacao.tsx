import { useState } from "react";
import { dbQuery } from "../db";

export default function Exportacao() {
  const [status, setStatus] = useState("");

  const exportarCSV = async (tabela: string) => {
    try {
      setStatus(`A exportar ${tabela}...`);
      const dados = await dbQuery<any>(`SELECT * FROM ${tabela}`);
      
      if (dados.length === 0) {
        setStatus(`A tabela ${tabela} está vazia. Nenhuma exportação gerada.`);
        return;
      }

      const cabecalhos = Object.keys(dados[0]).join(",");
      const linhas = dados.map((linha) => 
        Object.values(linha).map(v => `"${v}"`).join(",")
      );
      
      const csv = [cabecalhos, ...linhas].join("\n");
      const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      
      link.href = url;
      link.setAttribute("download", `prontuario_${tabela}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      setStatus(`Exportação de ${tabela} concluída com sucesso! (Ficheiro guardado nas Transferências)`);
    } catch (e) {
      setStatus(`Erro ao exportar ${tabela}: ` + String(e));
    }
  };

  const tabelas = ["pacientes", "fisioterapeutas", "funcionarios", "consultas", "prontuarios"];

  return (
    <div style={{ background: "var(--bg-panel)", padding: "2rem", borderRadius: "8px", boxShadow: "0 1px 3px rgba(0,0,0,0.1)" }}>
      <h2 style={{ marginTop: 0, color: "var(--text-main)" }}>Exportação de Dados (CSV)</h2>
      <p style={{ color: "var(--text-muted)" }}>Selecione a tabela que deseja exportar. O ficheiro resultante pode ser aberto diretamente no Excel ou Google Sheets.</p>
      
      <div style={{ display: "flex", gap: "1rem", flexWrap: "wrap", margin: "2rem 0" }}>
        {tabelas.map((tabela) => (
          <button
            key={tabela}
            onClick={() => exportarCSV(tabela)}
            style={{ padding: "0.75rem 1.5rem", background: "var(--btn-primary)", color: "white", border: "none", borderRadius: "4px", cursor: "pointer", textTransform: "capitalize", fontSize: "1rem" }}
          >
            Exportar {tabela}
          </button>
        ))}
      </div>
      
      {status && <p style={{ fontWeight: "bold", color: "var(--text-main)" }}>{status}</p>}
    </div>
  );
}