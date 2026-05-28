import { useState, useEffect } from "react";
import { dbQuery } from "../db";

export default function Dashboard() {
  const [totalPacientes, setTotalPacientes] = useState<number>(0);
  const [totalConsultasPendentes, setTotalConsultasPendentes] = useState<number>(0);
  const [totalProntuarios, setTotalProntuarios] = useState<number>(0);

  useEffect(() => {
    async function carregarMetricas() {
      try {
        const pacientes = await dbQuery<{ total: number }>("SELECT COUNT(*) as total FROM pacientes");
        setTotalPacientes(pacientes[0]?.total || 0);

        const consultas = await dbQuery<{ total: number }>("SELECT COUNT(*) as total FROM consultas WHERE status = 'Pendente'");
        setTotalConsultasPendentes(consultas[0]?.total || 0);

        const prontuarios = await dbQuery<{ total: number }>("SELECT COUNT(*) as total FROM prontuarios");
        setTotalProntuarios(prontuarios[0]?.total || 0);
      } catch (e) {
        console.error(e);
      }
    }
    carregarMetricas();
  }, []);

  return (
    <div style={{ display: "flex", gap: "2rem", flexWrap: "wrap" }}>
      <div style={{ background: "#fff", padding: "2rem", borderRadius: "8px", boxShadow: "0 1px 3px rgba(0,0,0,0.1)", flex: "1 1 250px", textAlign: "center" }}>
        <h3 style={{ margin: "0 0 1rem 0", color: "#6b7280" }}>Total de Pacientes</h3>
        <p style={{ fontSize: "3rem", margin: 0, fontWeight: "bold", color: "#1f2937" }}>{totalPacientes}</p>
      </div>
      
      <div style={{ background: "#fff", padding: "2rem", borderRadius: "8px", boxShadow: "0 1px 3px rgba(0,0,0,0.1)", flex: "1 1 250px", textAlign: "center" }}>
        <h3 style={{ margin: "0 0 1rem 0", color: "#6b7280" }}>Consultas Pendentes</h3>
        <p style={{ fontSize: "3rem", margin: 0, fontWeight: "bold", color: "#f59e0b" }}>{totalConsultasPendentes}</p>
      </div>

      <div style={{ background: "#fff", padding: "2rem", borderRadius: "8px", boxShadow: "0 1px 3px rgba(0,0,0,0.1)", flex: "1 1 250px", textAlign: "center" }}>
        <h3 style={{ margin: "0 0 1rem 0", color: "#6b7280" }}>Prontuários Registrados</h3>
        <p style={{ fontSize: "3rem", margin: 0, fontWeight: "bold", color: "#10b981" }}>{totalProntuarios}</p>
      </div>
    </div>
  );
}