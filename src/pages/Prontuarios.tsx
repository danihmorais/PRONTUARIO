import React, { useState, useEffect, useMemo, useRef } from "react";
import { dbQuery, dbExecute } from "../db";

interface Prontuario {
  id: number;
  id_paciente: number;
  paciente_nome: string;
  idade: string;
  telefone: string;
  profissao: string;
  data_registro: string;
  queixa: string;
  historia_atual: string;
  medicamentos: string;
  exame_rx: number;
  exame_rm: number;
  exame_usg: number;
  exame_tc: number;
  exames_obs: string;
  dor_local: string;
  dor_eva: number;
  dor_irradia: number;
  dor_formigamento: number;
  dor_limitacao: number;
  inspecao: string;
  palpacao: string;
  adm: string;
  forca: string;
  diagnostico: string;
  objetivo_tratamento: string;
  conduta_terapia_manual: number;
  conduta_liberacao: number;
  conduta_mobilizacao: number;
  conduta_alongamento: number;
  conduta_exercicios: number;
  conduta_outras: string;
  evolucao_data: string;
  evolucao: string;
  fisioterapeuta_nome: string;
  fisioterapeuta_crefito: string;
}

interface ItemSeletor {
  id: number;
  nome: string;
}

interface Configuracao {
  chave: string;
  valor: string;
}

const inputStyle: React.CSSProperties = {
  padding: "0.6rem 0.75rem",
  width: "100%",
  border: "1px solid var(--border)",
  borderRadius: "8px",
  background: "var(--bg-input)",
  color: "var(--text-main)",
  outline: "none",
  fontSize: "14px",
  boxSizing: "border-box",
};

const inputReadonlyStyle: React.CSSProperties = {
  ...inputStyle,
  background: "var(--bg-subtle)",
  color: "var(--text-muted)",
  cursor: "default",
  userSelect: "none",
};

const labelStyle: React.CSSProperties = {
  fontSize: "13px",
  fontWeight: 600,
  color: "var(--text-muted)",
  marginBottom: "0.3rem",
  display: "block",
};

const textareaStyle: React.CSSProperties = {
  padding: "0.6rem 0.75rem",
  minHeight: "70px",
  resize: "vertical",
  width: "100%",
  border: "1px solid var(--border)",
  borderRadius: "8px",
  background: "var(--bg-input)",
  color: "var(--text-main)",
  outline: "none",
  fontSize: "14px",
  boxSizing: "border-box",
};

const checkboxContainerStyle: React.CSSProperties = {
  display: "flex",
  alignItems: "center",
  gap: "0.5rem",
  fontSize: "14px",
  color: "var(--text-main)",
  cursor: "pointer",
};

const cardStyle: React.CSSProperties = {
  background: "var(--bg-panel)",
  border: "1px solid var(--border)",
  borderRadius: "10px",
  padding: "1.5rem",
  boxShadow: "var(--shadow-sm)",
  display: "flex",
  flexDirection: "column",
  gap: "1.25rem",
};

const cardHeaderStyle: React.CSSProperties = {
  margin: 0,
  paddingBottom: "0.75rem",
  borderBottom: "1px solid var(--border)",
  fontSize: "14px",
  fontWeight: 700,
  color: "var(--text-main)",
  textTransform: "uppercase",
  letterSpacing: "0.05em",
};

const cardBodyStyle: React.CSSProperties = {
  display: "flex",
  flexWrap: "wrap",
  gap: "1rem",
};

export default function Prontuarios() {
  const [prontuarios, setProntuarios] = useState<Prontuario[]>([]);
  const [pacientes, setPacientes] = useState<ItemSeletor[]>([]);
  const [busca, setBusca] = useState("");
  const [expandido, setExpandido] = useState<number | null>(null);
  const [editando, setEditando] = useState<Prontuario | null>(null);

  const [fisioterapeutaNome, setFisioterapeutaNome] = useState("");
  const [fisioterapeutaCrefito, setFisioterapeutaCrefito] = useState("");

  const [idPaciente, setIdPaciente] = useState("");
  const [buscaPaciente, setBuscaPaciente] = useState("");
  const [dropdownPaciente, setDropdownPaciente] = useState(false);
  const pacienteRef = useRef<HTMLDivElement>(null);

  const [idade, setIdade] = useState("");
  const [telefone, setTelefone] = useState("");
  const [profissao, setProfissao] = useState("");
  const [dataRegistro, setDataRegistro] = useState(new Date().toISOString().split("T")[0]);
  
  const [queixa, setQueixa] = useState("");
  const [historiaAtual, setHistoriaAtual] = useState("");
  const [medicamentos, setMedicamentos] = useState("");
  
  const [exameRx, setExameRx] = useState(false);
  const [exameRm, setExameRm] = useState(false);
  const [exameUsg, setExameUsg] = useState(false);
  const [exameTc, setExameTc] = useState(false);
  const [examesObs, setExamesObs] = useState("");
  
  const [dorLocal, setDorLocal] = useState("");
  const [dorEva, setDorEva] = useState(0);
  const [dorIrradia, setDorIrradia] = useState(false);
  const [dorFormigamento, setDorFormigamento] = useState(false);
  const [dorLimitacao, setDorLimitacao] = useState(false);
  
  const [inspecao, setInspecao] = useState("");
  const [palpacao, setPalpacao] = useState("");
  const [adm, setAdm] = useState("");
  const [forca, setForca] = useState("");
  
  const [diagnostico, setDiagnostico] = useState("");
  const [objetivoTratamento, setObjetivoTratamento] = useState("");
  
  const [condutaTerapiaManual, setCondutaTerapiaManual] = useState(false);
  const [condutaLiberacao, setCondutaLiberacao] = useState(false);
  const [condutaMobilizacao, setCondutaMobilizacao] = useState(false);
  const [condutaAlongamento, setCondutaAlongamento] = useState(false);
  const [condutaExercicios, setCondutaExercicios] = useState(false);
  const [condutaOutras, setCondutaOutras] = useState("");
  
  const [evolucaoData, setEvolucaoData] = useState(new Date().toISOString().split("T")[0]);
  const [evolucao, setEvolucao] = useState("");

  const [salvando, setSalvando] = useState(false);

  const carregar = async () => {
    try {
      const [resPron, resPac, resConf] = await Promise.all([
        dbQuery<Prontuario>(`
          SELECT 
            pr.id,
            pr.id_paciente,
            p.nome as paciente_nome,
            pr.idade,
            pr.telefone,
            pr.profissao,
            pr.data_registro,
            pr.queixa,
            pr.historia_atual,
            pr.medicamentos,
            pr.exame_rx,
            pr.exame_rm,
            pr.exame_usg,
            pr.exame_tc,
            pr.exames_obs,
            pr.dor_local,
            pr.dor_eva,
            pr.dor_irradia,
            pr.dor_formigamento,
            pr.dor_limitacao,
            pr.inspecao,
            pr.palpacao,
            pr.adm,
            pr.forca,
            pr.diagnostico,
            pr.objetivo_tratamento,
            pr.conduta_terapia_manual,
            pr.conduta_liberacao,
            pr.conduta_mobilizacao,
            pr.conduta_alongamento,
            pr.conduta_exercicios,
            pr.conduta_outras,
            pr.evolucao_data,
            pr.evolucao,
            pr.fisioterapeuta_nome,
            pr.fisioterapeuta_crefito
          FROM prontuarios pr
          LEFT JOIN pacientes p
            ON pr.id_paciente = p.id
          ORDER BY pr.id DESC
        `),
        dbQuery<ItemSeletor>(`
          SELECT id, nome
          FROM pacientes
          ORDER BY nome
        `),
        dbQuery<Configuracao>(`
          SELECT chave, valor
          FROM configuracoes
          WHERE chave IN ('fisioterapeuta_nome', 'fisioterapeuta_crefito')
        `),
      ]);
      setProntuarios(resPron);
      setPacientes(resPac);

      const nome = resConf.find((c) => c.chave === "fisioterapeuta_nome")?.valor ?? "";
      const crefito = resConf.find((c) => c.chave === "fisioterapeuta_crefito")?.valor ?? "";
      setFisioterapeutaNome(nome);
      setFisioterapeutaCrefito(crefito);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    carregar();
  }, []);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        pacienteRef.current &&
        !pacienteRef.current.contains(event.target as Node)
      ) {
        setDropdownPaciente(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const pacientesFiltrados = useMemo(() => {
    return pacientes
      .filter((p) =>
        p.nome.toLowerCase().includes(buscaPaciente.toLowerCase())
      )
      .slice(0, 30);
  }, [pacientes, buscaPaciente]);

  const limparForm = () => {
    setIdPaciente("");
    setBuscaPaciente("");
    setIdade("");
    setTelefone("");
    setProfissao("");
    setDataRegistro(new Date().toISOString().split("T")[0]);
    setQueixa("");
    setHistoriaAtual("");
    setMedicamentos("");
    setExameRx(false);
    setExameRm(false);
    setExameUsg(false);
    setExameTc(false);
    setExamesObs("");
    setDorLocal("");
    setDorEva(0);
    setDorIrradia(false);
    setDorFormigamento(false);
    setDorLimitacao(false);
    setInspecao("");
    setPalpacao("");
    setAdm("");
    setForca("");
    setDiagnostico("");
    setObjetivoTratamento("");
    setCondutaTerapiaManual(false);
    setCondutaLiberacao(false);
    setCondutaMobilizacao(false);
    setCondutaAlongamento(false);
    setCondutaExercicios(false);
    setCondutaOutras("");
    setEvolucaoData(new Date().toISOString().split("T")[0]);
    setEvolucao("");
    setEditando(null);
  };

  const preencherEdicao = (pr: Prontuario) => {
    setEditando(pr);
    setIdPaciente(String(pr.id_paciente));
    setBuscaPaciente(pr.paciente_nome);
    setIdade(pr.idade || "");
    setTelefone(pr.telefone || "");
    setProfissao(pr.profissao || "");
    setDataRegistro(pr.data_registro);
    setQueixa(pr.queixa || "");
    setHistoriaAtual(pr.historia_atual || "");
    setMedicamentos(pr.medicamentos || "");
    setExameRx(Boolean(pr.exame_rx));
    setExameRm(Boolean(pr.exame_rm));
    setExameUsg(Boolean(pr.exame_usg));
    setExameTc(Boolean(pr.exame_tc));
    setExamesObs(pr.exames_obs || "");
    setDorLocal(pr.dor_local || "");
    setDorEva(pr.dor_eva || 0);
    setDorIrradia(Boolean(pr.dor_irradia));
    setDorFormigamento(Boolean(pr.dor_formigamento));
    setDorLimitacao(Boolean(pr.dor_limitacao));
    setInspecao(pr.inspecao || "");
    setPalpacao(pr.palpacao || "");
    setAdm(pr.adm || "");
    setForca(pr.forca || "");
    setDiagnostico(pr.diagnostico || "");
    setObjetivoTratamento(pr.objetivo_tratamento || "");
    setCondutaTerapiaManual(Boolean(pr.conduta_terapia_manual));
    setCondutaLiberacao(Boolean(pr.conduta_liberacao));
    setCondutaMobilizacao(Boolean(pr.conduta_mobilizacao));
    setCondutaAlongamento(Boolean(pr.conduta_alongamento));
    setCondutaExercicios(Boolean(pr.conduta_exercicios));
    setCondutaOutras(pr.conduta_outras || "");
    setEvolucaoData(pr.evolucao_data || "");
    setEvolucao(pr.evolucao || "");

    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const salvar = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!idPaciente) {
      alert("Selecione o paciente.");
      return;
    }
    setSalvando(true);

    const params = [
      idPaciente,
      idade,
      telefone,
      profissao,
      dataRegistro,
      queixa,
      historiaAtual,
      medicamentos,
      String(exameRx ? 1 : 0),
      String(exameRm ? 1 : 0),
      String(exameUsg ? 1 : 0),
      String(exameTc ? 1 : 0),
      examesObs,
      dorLocal,
      String(dorEva),
      String(dorIrradia ? 1 : 0),
      String(dorFormigamento ? 1 : 0),
      String(dorLimitacao ? 1 : 0),
      inspecao,
      palpacao,
      adm,
      forca,
      diagnostico,
      objetivoTratamento,
      String(condutaTerapiaManual ? 1 : 0),
      String(condutaLiberacao ? 1 : 0),
      String(condutaMobilizacao ? 1 : 0),
      String(condutaAlongamento ? 1 : 0),
      String(condutaExercicios ? 1 : 0),
      condutaOutras,
      evolucaoData,
      evolucao,
      fisioterapeutaNome,
      fisioterapeutaCrefito,
    ];

    try {
      if (editando) {
        await dbExecute(
          `
          UPDATE prontuarios SET
            id_paciente=?, idade=?, telefone=?, profissao=?, data_registro=?, queixa=?, historia_atual=?, medicamentos=?,
            exame_rx=?, exame_rm=?, exame_usg=?, exame_tc=?, exames_obs=?,
            dor_local=?, dor_eva=?, dor_irradia=?, dor_formigamento=?, dor_limitacao=?,
            inspecao=?, palpacao=?, adm=?, forca=?, diagnostico=?, objetivo_tratamento=?,
            conduta_terapia_manual=?, conduta_liberacao=?, conduta_mobilizacao=?,
            conduta_alongamento=?, conduta_exercicios=?, conduta_outras=?,
            evolucao_data=?, evolucao=?, fisioterapeuta_nome=?, fisioterapeuta_crefito=?
          WHERE id=?
          `,
          [...params, String(editando.id)]
        );
      } else {
        await dbExecute(
          `
          INSERT INTO prontuarios (
            id_paciente, idade, telefone, profissao, data_registro, queixa, historia_atual, medicamentos,
            exame_rx, exame_rm, exame_usg, exame_tc, exames_obs,
            dor_local, dor_eva, dor_irradia, dor_formigamento, dor_limitacao,
            inspecao, palpacao, adm, forca, diagnostico, objetivo_tratamento,
            conduta_terapia_manual, conduta_liberacao, conduta_mobilizacao,
            conduta_alongamento, conduta_exercicios, conduta_outras,
            evolucao_data, evolucao, fisioterapeuta_nome, fisioterapeuta_crefito
          ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
          `,
          params
        );
      }
      limparForm();
      await carregar();
    } catch (e) {
      alert("Erro ao salvar: " + e);
    } finally {
      setSalvando(false);
    }
  };

  const deletar = async (id: number, nome: string) => {
    if (!confirm(`Excluir prontuário de "${nome}"?`)) return;
    try {
      await dbExecute("DELETE FROM prontuarios WHERE id = ?", [String(id)]);
      carregar();
    } catch (e) {
      alert("Erro ao excluir: " + e);
    }
  };

  const truncar = (texto: string | null | undefined, len = 50) => {
    if (!texto) return "—";
    return texto.length > len ? texto.substring(0, len) + "..." : texto;
  };

  const filtrados = prontuarios.filter(
    (pr) =>
      pr.paciente_nome?.toLowerCase().includes(busca.toLowerCase()) ||
      pr.queixa?.toLowerCase().includes(busca.toLowerCase()) ||
      pr.diagnostico?.toLowerCase().includes(busca.toLowerCase())
  );

  const evaColor = (val: number) => {
    if (val <= 3) return "#22c55e";
    if (val <= 6) return "#f59e0b";
    return "#ef4444";
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1.5rem", width: "calc(100% + 6px)" }}>
      <div>
        <h3 style={{ margin: "0 0 1.25rem", fontSize: "18px", fontWeight: 700, color: "var(--text-main)" }}>
          {editando
            ? `Editando Avaliação — ${editando.paciente_nome}`
            : "Ficha de Avaliação — Traumato Ortopédica / Terapia Manual"}
        </h3>

        <form onSubmit={salvar} style={{ display: "flex", flexDirection: "column", gap: "1.5rem" }}>
          
          <div style={cardStyle}>
            <h4 style={cardHeaderStyle}>Identificação</h4>
            <div style={cardBodyStyle}>
              <div ref={pacienteRef} style={{ flex: "1 1 300px", position: "relative" }}>
                <label style={labelStyle}>Nome *</label>
                <input
                  value={buscaPaciente}
                  onChange={(e) => { setBuscaPaciente(e.target.value); setIdPaciente(""); setDropdownPaciente(true); }}
                  onFocus={() => setDropdownPaciente(true)}
                  placeholder="Pesquisar paciente..."
                  required
                  style={inputStyle}
                />
                {dropdownPaciente && buscaPaciente && (
                  <div style={{
                    position: "absolute", top: "100%", left: 0, right: 0, marginTop: "6px",
                    background: "var(--bg-panel)", border: "1px solid var(--border)",
                    borderRadius: "10px", overflow: "hidden", maxHeight: "260px",
                    overflowY: "auto", zIndex: 100, boxShadow: "var(--shadow-md)",
                  }}>
                    {pacientesFiltrados.length > 0 ? pacientesFiltrados.map((p) => (
                      <button type="button" key={p.id}
                        onClick={() => { setIdPaciente(String(p.id)); setBuscaPaciente(p.nome); setDropdownPaciente(false); }}
                        style={{
                          width: "100%", textAlign: "left", padding: "0.75rem",
                          border: "none", borderBottom: "1px solid var(--border)",
                          background: "transparent", cursor: "pointer",
                          color: "var(--text-main)", fontSize: "14px",
                        }}>
                        {p.nome}
                      </button>
                    )) : (
                      <div style={{ padding: "0.85rem", fontSize: "13px", color: "var(--text-muted)" }}>
                        Nenhum paciente encontrado
                      </div>
                    )}
                  </div>
                )}
              </div>

              <div style={{ flex: "1 1 80px" }}>
                <label style={labelStyle}>Idade</label>
                <input value={idade} onChange={(e) => setIdade(e.target.value)} style={inputStyle} />
              </div>

              <div style={{ flex: "1 1 150px" }}>
                <label style={labelStyle}>Telefone</label>
                <input value={telefone} onChange={(e) => setTelefone(e.target.value)} style={inputStyle} />
              </div>

              <div style={{ flex: "1 1 200px" }}>
                <label style={labelStyle}>Profissão</label>
                <input value={profissao} onChange={(e) => setProfissao(e.target.value)} style={inputStyle} />
              </div>

              <div style={{ flex: "0 1 180px" }}>
                <label style={labelStyle}>Data da Avaliação *</label>
                <input type="date" value={dataRegistro}
                  onChange={(e) => setDataRegistro(e.target.value)} required style={inputStyle} />
              </div>
            </div>
          </div>

          <div style={cardStyle}>
            <h4 style={cardHeaderStyle}>Histórico Clínico</h4>
            <div style={cardBodyStyle}>
              <div style={{ flex: "1 1 100%" }}>
                <label style={labelStyle}>Queixa Principal *</label>
                <textarea value={queixa} onChange={(e) => setQueixa(e.target.value)} required style={textareaStyle} />
              </div>

              <div style={{ flex: "1 1 calc(50% - 0.5rem)" }}>
                <label style={labelStyle}>História Atual</label>
                <textarea value={historiaAtual} onChange={(e) => setHistoriaAtual(e.target.value)}
                  style={{ ...textareaStyle, minHeight: "90px" }} />
              </div>

              <div style={{ flex: "1 1 calc(50% - 0.5rem)" }}>
                <label style={labelStyle}>Medicamentos</label>
                <textarea value={medicamentos} onChange={(e) => setMedicamentos(e.target.value)}
                  style={{ ...textareaStyle, minHeight: "90px" }} />
              </div>
            </div>
          </div>

          <div style={cardStyle}>
            <h4 style={cardHeaderStyle}>Exames</h4>
            <div style={cardBodyStyle}>
              <div style={{ flex: "1 1 100%", display: "flex", flexDirection: "column", gap: "1.25rem" }}>
                <div style={{ display: "flex", gap: "2rem", flexWrap: "wrap", justifyContent: "center", width: "100%", paddingTop: "0.25rem" }}>
                  {[
                    { label: "RX",  value: exameRx,  set: setExameRx  },
                    { label: "RM",  value: exameRm,  set: setExameRm  },
                    { label: "USG", value: exameUsg, set: setExameUsg },
                    { label: "TC",  value: exameTc,  set: setExameTc  },
                  ].map(({ label, value, set }) => (
                    <label key={label} style={checkboxContainerStyle}>
                      <input type="checkbox" checked={value} onChange={(e) => set(e.target.checked)} />
                      {label}
                    </label>
                  ))}
                </div>
                <div style={{ width: "100%" }}>
                  <label style={labelStyle}>Observações</label>
                  <textarea value={examesObs} onChange={(e) => setExamesObs(e.target.value)}
                    style={{ ...textareaStyle, minHeight: "70px" }} />
                </div>
              </div>
            </div>
          </div>

          <div style={cardStyle}>
            <h4 style={cardHeaderStyle}>Dor</h4>
            <div style={cardBodyStyle}>
              <div style={{ flex: "1 1 220px" }}>
                <label style={labelStyle}>Local da Dor</label>
                <input value={dorLocal} onChange={(e) => setDorLocal(e.target.value)} style={inputStyle} />
              </div>

              <div style={{ flex: "0 1 auto", display: "flex", flexDirection: "column", justifyContent: "flex-end", gap: "0.5rem" }}>
                <label style={labelStyle}>Características</label>
                <div style={{ display: "flex", gap: "1.25rem", flexWrap: "wrap", paddingBottom: "0.1rem" }}>
                  {[
                    { label: "Irradia",      value: dorIrradia,      set: setDorIrradia      },
                    { label: "Formigamento", value: dorFormigamento, set: setDorFormigamento },
                    { label: "Limitação de movimento", value: dorLimitacao,   set: setDorLimitacao    },
                  ].map(({ label, value, set }) => (
                    <label key={label} style={checkboxContainerStyle}>
                      <input type="checkbox" checked={value} onChange={(e) => set(e.target.checked)} />
                      <span style={{ whiteSpace: "nowrap" }}>{label}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div style={{ flex: "1 1 100%" }}>
                <label style={labelStyle}>
                  Escala Visual Analógica (EVA):{" "}
                  <span style={{ color: evaColor(dorEva), fontWeight: 700, fontSize: "15px" }}>{dorEva}</span>
                  {dorEva === 0 && <span style={{ color: "var(--text-muted)", fontWeight: 400 }}> — Sem dor</span>}
                  {dorEva >= 1 && dorEva <= 3 && <span style={{ color: "#22c55e", fontWeight: 400 }}> — Leve</span>}
                  {dorEva >= 4 && dorEva <= 6 && <span style={{ color: "#f59e0b", fontWeight: 400 }}> — Moderada</span>}
                  {dorEva >= 7 && dorEva <= 9 && <span style={{ color: "#ef4444", fontWeight: 400 }}> — Intensa</span>}
                  {dorEva === 10 && <span style={{ color: "#ef4444", fontWeight: 400 }}> — Pior dor possível</span>}
                </label>
                <input type="range" min="0" max="10" value={dorEva}
                  onChange={(e) => setDorEva(Number(e.target.value))}
                  style={{
                    width: "100%", height: "8px", borderRadius: "4px", outline: "none",
                    background: `linear-gradient(to right, #22c55e 0%, #facc15 50%, #ef4444 100%)`,
                    WebkitAppearance: "none", appearance: "none", cursor: "pointer", marginTop: "0.5rem",
                  }} />
                <div style={{ display: "flex", justifyContent: "space-between", fontSize: "11px", color: "var(--text-muted)", marginTop: "0.4rem" }}>
                  <span>0 — Sem dor</span><span>5 — Moderada</span><span>10 — Pior dor</span>
                </div>
              </div>
            </div>
          </div>

          <div style={cardStyle}>
            <h4 style={cardHeaderStyle}>Avaliação Física</h4>
            <div style={cardBodyStyle}>
              <div style={{ flex: "1 1 calc(50% - 0.5rem)" }}>
                <label style={labelStyle}>Inspeção / Postura</label>
                <textarea value={inspecao} onChange={(e) => setInspecao(e.target.value)}
                  style={{ ...textareaStyle, minHeight: "80px" }} />
              </div>

              <div style={{ flex: "1 1 calc(50% - 0.5rem)" }}>
                <label style={labelStyle}>Palpação</label>
                <textarea value={palpacao} onChange={(e) => setPalpacao(e.target.value)}
                  style={{ ...textareaStyle, minHeight: "80px" }} />
              </div>

              <div style={{ flex: "1 1 calc(50% - 0.5rem)" }}>
                <label style={labelStyle}>ADM</label>
                <div style={{ display: "flex", gap: "1.5rem", paddingTop: "0.35rem" }}>
                  {["Normal", "Reduzida"].map((v) => (
                    <label key={v} style={checkboxContainerStyle}>
                      <input type="radio" name="adm" value={v} checked={adm === v} onChange={(e) => setAdm(e.target.value)} />
                      {v}
                    </label>
                  ))}
                </div>
              </div>

              <div style={{ flex: "1 1 calc(50% - 0.5rem)" }}>
                <label style={labelStyle}>Força Muscular</label>
                <div style={{ display: "flex", gap: "1.5rem", paddingTop: "0.35rem" }}>
                  {["Preservada", "Reduzida"].map((v) => (
                    <label key={v} style={checkboxContainerStyle}>
                      <input type="radio" name="forca" value={v} checked={forca === v} onChange={(e) => setForca(e.target.value)} />
                      {v}
                    </label>
                  ))}
                </div>
              </div>
            </div>
          </div>

          <div style={cardStyle}>
            <h4 style={cardHeaderStyle}>Diagnóstico e Objetivos</h4>
            <div style={cardBodyStyle}>
              <div style={{ flex: "1 1 100%" }}>
                <label style={labelStyle}>Diagnóstico Fisioterapêutico</label>
                <textarea value={diagnostico} onChange={(e) => setDiagnostico(e.target.value)}
                  style={{ ...textareaStyle, minHeight: "80px" }} />
              </div>

              <div style={{ flex: "1 1 100%" }}>
                <label style={labelStyle}>Objetivo do Tratamento</label>
                <textarea value={objetivoTratamento} onChange={(e) => setObjetivoTratamento(e.target.value)}
                  style={{ ...textareaStyle, minHeight: "80px" }} />
              </div>
            </div>
          </div>

          <div style={cardStyle}>
            <h4 style={cardHeaderStyle}>Conduta / Plano Terapêutico</h4>
            <div style={cardBodyStyle}>
              <div style={{ flex: "1 1 100%" }}>
                <div style={{
                  display: "flex", flexWrap: "wrap", gap: "0.6rem 1.75rem",
                  marginBottom: "0.75rem",
                  padding: "0.75rem 1rem",
                  background: "var(--bg-subtle)",
                  borderRadius: "8px",
                  border: "1px solid var(--border)",
                }}>
                  {[
                    { label: "Terapia manual",        value: condutaTerapiaManual, set: setCondutaTerapiaManual },
                    { label: "Liberação miofascial",  value: condutaLiberacao,     set: setCondutaLiberacao     },
                    { label: "Mobilização articular", value: condutaMobilizacao,   set: setCondutaMobilizacao   },
                    { label: "Alongamento",           value: condutaAlongamento,   set: setCondutaAlongamento   },
                    { label: "Exercícios terapêuticos", value: condutaExercicios,  set: setCondutaExercicios    },
                  ].map(({ label, value, set }) => (
                    <label key={label} style={{ ...checkboxContainerStyle, whiteSpace: "nowrap" }}>
                      <input type="checkbox" checked={value} onChange={(e) => set(e.target.checked)} />
                      {label}
                    </label>
                  ))}
                </div>
                <label style={labelStyle}>Outras condutas</label>
                <textarea value={condutaOutras} onChange={(e) => setCondutaOutras(e.target.value)} style={textareaStyle} />
              </div>
            </div>
          </div>

          <div style={cardStyle}>
            <h4 style={cardHeaderStyle}>Evolução</h4>
            <div style={cardBodyStyle}>
              <div style={{ flex: "0 1 180px" }}>
                <label style={labelStyle}>Data da Evolução</label>
                <input type="date" value={evolucaoData} onChange={(e) => setEvolucaoData(e.target.value)} style={inputStyle} />
              </div>

              <div style={{ flex: "1 1 100%" }}>
                <label style={labelStyle}>Evolução Clínica</label>
                <textarea value={evolucao} onChange={(e) => setEvolucao(e.target.value)}
                  style={{ ...textareaStyle, minHeight: "100px" }} />
              </div>
            </div>
          </div>

          <div style={{ ...cardStyle, background: "var(--bg-subtle)" }}>
            <h4 style={{ ...cardHeaderStyle, borderBottom: "none", paddingBottom: 0, display: "flex", alignItems: "center", gap: "0.5rem" }}>
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
              Profissional Responsável
            </h4>
            <div style={cardBodyStyle}>
              <div style={{ flex: "1 1 200px" }}>
                <label style={{ ...labelStyle, marginBottom: "0.2rem" }}>Fisioterapeuta</label>
                <input
                  value={fisioterapeutaNome || "—"}
                  readOnly
                  tabIndex={-1}
                  style={inputReadonlyStyle}
                />
              </div>

              <div style={{ flex: "0 1 180px" }}>
                <label style={{ ...labelStyle, marginBottom: "0.2rem" }}>CREFITO</label>
                <input
                  value={fisioterapeutaCrefito || "—"}
                  readOnly
                  tabIndex={-1}
                  style={inputReadonlyStyle}
                />
              </div>

              <div style={{ flex: "1 1 200px" }}>
                <label style={{ ...labelStyle, marginBottom: "0.2rem" }}>Assinatura/Carimbo</label>
                <input
                  value=""
                  readOnly
                  tabIndex={-1}
                  style={inputReadonlyStyle}
                />
              </div>
            </div>
          </div>

          <div style={{ flex: "0 0 100%", display: "flex", gap: "0.75rem", marginTop: "0.5rem" }}>
            <button type="submit" disabled={salvando} style={{
              padding: "0.65rem 1.75rem",
              background: "var(--btn-success)",
              color: "white",
              border: "none",
              borderRadius: "8px",
              fontSize: "14px",
              fontWeight: 600,
              cursor: salvando ? "not-allowed" : "pointer",
              opacity: salvando ? 0.7 : 1,
            }}>
              {salvando ? "Salvando..." : editando ? "Salvar Alterações" : "Salvar Avaliação"}
            </button>

            {editando && (
              <button type="button" onClick={limparForm} style={{
                padding: "0.65rem 1.25rem",
                background: "transparent",
                color: "var(--text-muted)",
                border: "1px solid var(--border)",
                borderRadius: "8px",
                fontSize: "14px",
                cursor: "pointer",
              }}>
                Cancelar
              </button>
            )}
          </div>
        </form>
      </div>

      <div style={{
        background: "var(--bg-panel)",
        borderRadius: "12px",
        border: "1px solid var(--border)",
        boxShadow: "var(--shadow-sm)",
        overflow: "hidden",
        marginTop: "1rem",
      }}>
        <div style={{
          padding: "1rem 1.5rem",
          borderBottom: "1px solid var(--border)",
          display: "flex",
          alignItems: "center",
          gap: "1rem",
        }}>
          <input
            value={busca}
            onChange={(e) => setBusca(e.target.value)}
            placeholder="Buscar por paciente, queixa ou diagnóstico..."
            style={{ ...inputStyle, maxWidth: "360px" }}
          />
          <span style={{ fontSize: "13px", color: "var(--text-muted)", marginLeft: "auto" }}>
            {filtrados.length} {filtrados.length === 1 ? "registro" : "registros"}
          </span>
        </div>

        <div style={{ overflowX: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ background: "var(--bg-subtle)" }}>
                {["ID", "Paciente", "Data", "Queixa", "Diagnóstico", "Ações"].map((h) => (
                  <th key={h} style={{
                    padding: "0.75rem 1rem",
                    textAlign: "left",
                    whiteSpace: "nowrap",
                    fontSize: "13px",
                    color: "var(--text-main)",
                    fontWeight: 600,
                  }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filtrados.map((pr) => (
                <React.Fragment key={pr.id}>
                  <tr style={{ borderTop: "1px solid var(--border)" }}>
                    <td style={{ padding: "0.75rem 1rem", color: "var(--text-muted)", fontSize: "13px", fontFamily: "'DM Mono', monospace" }}>
                      {pr.id}
                    </td>
                    <td style={{ padding: "0.75rem 1rem", fontWeight: 500, color: "var(--text-main)", fontSize: "14px" }}>
                      {pr.paciente_nome}
                    </td>
                    <td style={{ padding: "0.75rem 1rem", color: "var(--text-muted)", fontSize: "13px", whiteSpace: "nowrap" }}>
                      {pr.data_registro}
                    </td>
                    <td style={{ padding: "0.75rem 1rem", color: "var(--text-muted)", fontSize: "13px", maxWidth: "220px", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
                      {truncar(pr.queixa, 55)}
                    </td>
                    <td style={{ padding: "0.75rem 1rem", color: "var(--text-muted)", fontSize: "13px", maxWidth: "200px", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
                      {truncar(pr.diagnostico, 55)}
                    </td>
                    <td style={{ padding: "0.75rem 1rem" }}>
                      <div style={{ display: "flex", gap: "0.5rem" }}>
                        <button onClick={() => setExpandido(expandido === pr.id ? null : pr.id)} style={{
                          background: "rgba(124,58,237,0.1)", color: "#7c3aed",
                          border: "none", padding: "0.35rem 0.8rem", borderRadius: "6px",
                          fontSize: "12px", fontWeight: 600, cursor: "pointer",
                        }}>
                          {expandido === pr.id ? "Fechar" : "Ver"}
                        </button>
                        <button onClick={() => preencherEdicao(pr)} style={{
                          background: "rgba(37,99,235,0.1)", color: "var(--btn-primary)",
                          border: "none", padding: "0.35rem 0.8rem", borderRadius: "6px",
                          fontSize: "12px", fontWeight: 600, cursor: "pointer",
                        }}>
                          Editar
                        </button>
                        <button onClick={() => deletar(pr.id, pr.paciente_nome)} style={{
                          background: "rgba(220,38,38,0.1)", color: "var(--btn-danger)",
                          border: "none", padding: "0.35rem 0.8rem", borderRadius: "6px",
                          fontSize: "12px", fontWeight: 600, cursor: "pointer",
                        }}>
                          Excluir
                        </button>
                      </div>
                    </td>
                  </tr>

                  {expandido === pr.id && (
                    <tr key={`exp-${pr.id}`} style={{ background: "var(--bg-subtle)" }}>
                      <td colSpan={6} style={{ padding: "1.5rem" }}>
                        <div style={{
                          display: "grid",
                          gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
                          gap: "1.5rem",
                        }}>
                          {[
                            { label: "Idade",               valor: pr.idade },
                            { label: "Telefone",            valor: pr.telefone },
                            { label: "Profissão",           valor: pr.profissao },
                            { label: "Queixa Principal",    valor: pr.queixa },
                            { label: "História Atual",      valor: pr.historia_atual },
                            { label: "Medicamentos",        valor: pr.medicamentos },
                            {
                              label: "Exames Complementares",
                              valor: [pr.exame_rx ? "RX" : "", pr.exame_rm ? "RM" : "", pr.exame_usg ? "USG" : "", pr.exame_tc ? "TC" : ""]
                                .filter(Boolean).join(", ") || "Nenhum",
                            },
                            { label: "Obs. Exames",         valor: pr.exames_obs },
                            {
                              label: "Dor",
                              valor: `Local: ${pr.dor_local || "—"}\nEVA: ${pr.dor_eva}\nCaracterísticas: ${
                                [pr.dor_irradia ? "Irradia" : "", pr.dor_formigamento ? "Formigamento" : "", pr.dor_limitacao ? "Limitação de Mov." : ""]
                                  .filter(Boolean).join(", ") || "Nenhuma"}`,
                            },
                            { label: "Inspeção / Postura",  valor: pr.inspecao },
                            { label: "Palpação",            valor: pr.palpacao },
                            { label: "ADM",                 valor: pr.adm },
                            { label: "Força",               valor: pr.forca },
                            { label: "Diagnóstico",         valor: pr.diagnostico },
                            { label: "Objetivo do Tratamento", valor: pr.objetivo_tratamento },
                            {
                              label: "Conduta / Plano Terapêutico",
                              valor: [
                                pr.conduta_terapia_manual ? "Terapia manual" : "",
                                pr.conduta_liberacao      ? "Liberação miofascial" : "",
                                pr.conduta_mobilizacao    ? "Mobilização articular" : "",
                                pr.conduta_alongamento    ? "Alongamento" : "",
                                pr.conduta_exercicios     ? "Exercícios terapêuticos" : "",
                              ].filter(Boolean).join("\n") + (pr.conduta_outras ? `\nOutras: ${pr.conduta_outras}` : ""),
                            },
                            { label: "Data da Evolução",    valor: pr.evolucao_data },
                            { label: "Evolução",            valor: pr.evolucao },
                            {
                              label: "Profissional Responsável",
                              valor: `Fisioterapeuta: ${pr.fisioterapeuta_nome || "—"}\nCREFITO: ${pr.fisioterapeuta_crefito || "—"}`,
                            },
                          ].map(({ label, valor }) => (
                            <div key={label}>
                              <div style={{ fontSize: "11px", fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.05em", color: "var(--text-muted)", marginBottom: "0.4rem" }}>
                                {label}
                              </div>
                              <div style={{ fontSize: "13px", color: "var(--text-main)", lineHeight: 1.6, whiteSpace: "pre-wrap" }}>
                                {valor || "—"}
                              </div>
                            </div>
                          ))}
                        </div>
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              ))}

              {filtrados.length === 0 && (
                <tr>
                  <td colSpan={6} style={{ padding: "2rem", textAlign: "center", color: "var(--text-muted)", fontSize: "14px" }}>
                    {busca ? "Nenhum resultado encontrado." : "Nenhuma avaliação registrada."}
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