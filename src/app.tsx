import { useState, useEffect } from "react";
import { invoke } from "@tauri-apps/api/tauri";
import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";
import Pacientes from "./pages/Pacientes";
import Consultas from "./pages/Consultas";
import Prontuarios from "./pages/Prontuarios";
import Exportacao from "./pages/Exportacao";
import Configuracoes from "./pages/Configuracoes";
import logo from "./assets/logo.png";
import { dbQuery } from "./db";

interface Configuracao {
  chave: string;
  valor: string;
}

function App() {
  const [autenticado, setAutenticado] = useState(false);
  const [usuario, setUsuario] = useState("");
  const [nivelUsuario, setNivelUsuario] = useState("");
  const [senhaInput, setSenhaInput] = useState("");
  const [erro, setErro] = useState("");
  const [carregando, setCarregando] = useState(false);
  const [paginaAtual, setPaginaAtual] = useState("Dashboard");

  const realizarLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setCarregando(true);
    setErro("");
    try {
      const nivel = await invoke<string>("login", { usuario, senha: senhaInput });
      setNivelUsuario(nivel);
      setAutenticado(true);
    } catch (err) {
      setErro(String(err));
    } finally {
      setCarregando(false);
    }
  };

  const realizarLogout = () => {
    setAutenticado(false);
    setUsuario("");
    setSenhaInput("");
    setNivelUsuario("");
    setPaginaAtual("Dashboard");
    setErro("");
  };

  const renderizarPagina = () => {
    switch (paginaAtual) {
      case "Dashboard": return <Dashboard />;
      case "Pacientes": return <Pacientes />;
      case "Consultas": return <Consultas />;
      case "Prontuários": return <Prontuarios />;
      case "Exportação": return <Exportacao />;
      case "Configurações": return <Configuracoes usuario={usuario} nivel={nivelUsuario} />;
      default: return <Dashboard />;
    }
  };
  
  const [fisioterapeutaNome, setFisioterapeutaNome] = useState("");

  useEffect(() => {
    carregarConfiguracoes();
  }, []);

  const carregarConfiguracoes = async () => {
    try {
      const resConf = await dbQuery<Configuracao>(`
        SELECT chave, valor
        FROM configuracoes
        WHERE chave = 'fisioterapeuta_nome'
      `);

      const nome =
        resConf.find((c) => c.chave === "fisioterapeuta_nome")?.valor || "";

      setFisioterapeutaNome(nome);
    } catch (err) {
      console.error(err);
    }
  };

  if (autenticado) {
    return (
      <div style={{ display: "flex", height: "100vh", width: "100vw", overflow: "hidden", background: "var(--bg-base)" }}>
        <Sidebar
          paginaAtual={paginaAtual}
          setPaginaAtual={setPaginaAtual}
          onLogout={realizarLogout}
          usuario={usuario}
        />
        <main style={{ flex: 1, display: "flex", flexDirection: "column", overflow: "hidden" }}>
          <div style={{
            padding: "1rem 2rem",
            borderBottom: "1px solid var(--border)",
            height:"80px",
            background: "var(--bg-panel)",
            display: "flex",
            alignItems: "center",
            gap: "0.75rem",
            flexShrink: 0,
            boxShadow: "var(--shadow-sm)",
          }}>
            <h1 style={{ margin: 0, fontSize: "1.1rem", fontWeight: 700, color: "var(--text-main)", letterSpacing: "-0.02em" }}>
              {paginaAtual}
            </h1>
            {nivelUsuario === "admin" && (
              <span style={{
                background: "rgba(37,99,235,0.1)",
                color: "var(--btn-primary)",
                fontSize: "11px",
                fontWeight: 700,
                padding: "2px 8px",
                borderRadius: "999px",
                textTransform: "uppercase",
                letterSpacing: "0.05em",
              }}>
                {fisioterapeutaNome
                ? fisioterapeutaNome.split(" ")[0]
                : "Fisioterapeuta"}
              </span>
            )}
          </div>
          <div style={{ flex: 1, padding: "1.5rem 2rem", overflowY: "auto" }}>
            {renderizarPagina()}
          </div>
        </main>
      </div>
    );
  }

  return (
    <div style={{
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      height: "100vh",
      width: "100vw",
      background: "var(--bg-base)",
    }}>
      <div style={{
        width: "100%",
        maxWidth: "380px",
        padding: "0 1.5rem",
      }}>
        <div style={{
          background: "var(--bg-panel)",
          borderRadius: "16px",
          padding: "2.5rem",
          boxShadow: "var(--shadow-lg)",
          border: "1px solid var(--border)",
        }}>
          <div style={{ textAlign: "center", marginBottom: "2rem" }}>
          <img
            src={logo}
            alt="Logo"
            style={{
              width: 72,
              height: 72,
              objectFit: "contain",
              margin: "0 auto 1rem",
              display: "block",
            }}
          />

          <h2
            style={{
              margin: "0 0 0.25rem",
              fontSize: "1.4rem",
              fontWeight: 700,
              color: "var(--text-main)",
              letterSpacing: "-0.03em",
            }}
          >
            Prontuário
          </h2>

          <p
            style={{
              margin: 0,
              fontSize: "14px",
              color: "var(--text-muted)",
            }}
          >
            Sistema de Gestão Clínica
          </p>
        </div>

          <form onSubmit={realizarLogin} style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
            <div style={{ display: "flex", flexDirection: "column", gap: "0.4rem" }}>
              <label style={{ fontSize: "13px", fontWeight: 600, color: "var(--text-muted)" }}>Usuário</label>
              <input
                type="text"
                value={usuario}
                onChange={(e) => setUsuario(e.target.value)}
                placeholder="Digite seu usuário"
                required
                autoFocus
                style={{ padding: "0.65rem 0.85rem" }}
              />
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: "0.4rem" }}>
              <label style={{ fontSize: "13px", fontWeight: 600, color: "var(--text-muted)" }}>Senha</label>
              <input
                type="password"
                value={senhaInput}
                onChange={(e) => setSenhaInput(e.target.value)}
                placeholder="Digite sua senha"
                required
                style={{ padding: "0.65rem 0.85rem" }}
              />
            </div>
            {erro && (
              <div style={{
                padding: "0.6rem 0.85rem",
                background: "rgba(220,38,38,0.08)",
                border: "1px solid rgba(220,38,38,0.2)",
                borderRadius: "8px",
                color: "var(--btn-danger)",
                fontSize: "13px",
                fontWeight: 500,
              }}>
                {erro}
              </div>
            )}
            <button
              type="submit"
              disabled={carregando}
              style={{
                padding: "0.75rem",
                marginTop: "0.5rem",
                background: carregando ? "var(--text-light)" : "var(--btn-primary)",
                color: "white",
                border: "none",
                borderRadius: "8px",
                fontSize: "15px",
                fontWeight: 600,
                cursor: carregando ? "not-allowed" : "pointer",
              }}
            >
              {carregando ? "Entrando..." : "Entrar"}
            </button>
          </form>
        </div>
        <p style={{ textAlign: "center", marginTop: "1.5rem", fontSize: "12px", color: "var(--text-light)" }}>
          Padrão: admin / admin
        </p>
      </div>
    </div>
  );
}

export default App;