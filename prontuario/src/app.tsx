import { useState } from "react";
import { invoke } from "@tauri-apps/api/tauri";
import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";
import Pacientes from "./pages/Pacientes";
import Fisioterapeutas from "./pages/Fisioterapeutas";
import Consultas from "./pages/Consultas";
import Prontuarios from "./pages/Prontuarios";
import Funcionarios from "./pages/Funcionarios";

function App() {
  const [autenticado, setAutenticado] = useState(false);
  const [usuario, setUsuario] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState("");
  const [paginaAtual, setPaginaAtual] = useState("Dashboard");

  const realizarLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const sucesso = await invoke<boolean>("login", { usuario, senha });
      if (sucesso) {
        setAutenticado(true);
        setErro("");
      } else {
        setErro("Usuário ou senha inválidos.");
      }
    } catch (err) {
      setErro(String(err));
    }
  };

  const realizarLogout = () => {
    setAutenticado(false);
    setUsuario("");
    setSenha("");
    setPaginaAtual("Dashboard");
  };

  const renderizarPagina = () => {
    switch (paginaAtual) {
      case "Dashboard": return <Dashboard />;
      case "Pacientes": return <Pacientes />;
      case "Fisioterapeutas": return <Fisioterapeutas />;
      case "Funcionários": return <Funcionarios />;
      case "Consultas": return <Consultas />;
      case "Prontuários": return <Prontuarios />;
      default: return <Dashboard />;
    }
  };

  if (autenticado) {
    return (
      <div style={{ display: "flex", height: "100vh", width: "100vw", overflow: "hidden" }}>
        <Sidebar paginaAtual={paginaAtual} setPaginaAtual={setPaginaAtual} onLogout={realizarLogout} />
        <main style={{ flex: 1, padding: "2rem", overflowY: "auto", background: "#f6f6f6" }}>
          <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center", borderBottom: "1px solid #e5e7eb", paddingBottom: "1rem", marginBottom: "2rem" }}>
            <h1 style={{ margin: 0, color: "#1f2937" }}>{paginaAtual}</h1>
            <div style={{ fontSize: "0.9rem", color: "#6b7280" }}>
              Usuário logado: <strong style={{ color: "#1f2937" }}>{usuario}</strong>
            </div>
          </header>
          {renderizarPagina()}
        </main>
      </div>
    );
  }

  return (
    <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100vh", width: "100vw", background: "#f0f2f5" }}>
      <form 
        onSubmit={realizarLogin} 
        style={{ display: "flex", flexDirection: "column", gap: "1rem", width: "300px", padding: "2rem", background: "#fff", borderRadius: "8px", boxShadow: "0 4px 6px rgba(0,0,0,0.1)" }}
      >
        <h2 style={{ textAlign: "center", margin: "0 0 1rem 0", color: "#1f2937" }}>Prontuário Login</h2>
        <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
          <label htmlFor="usuario" style={{ color: "#4b5563", fontSize: "0.9rem" }}>Usuário</label>
          <input id="usuario" type="text" value={usuario} onChange={(e) => setUsuario(e.target.value)} style={{ padding: "0.75rem", border: "1px solid #d1d5db", borderRadius: "4px" }} required />
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
          <label htmlFor="senha" style={{ color: "#4b5563", fontSize: "0.9rem" }}>Senha</label>
          <input id="senha" type="password" value={senha} onChange={(e) => setSenha(e.target.value)} style={{ padding: "0.75rem", border: "1px solid #d1d5db", borderRadius: "4px" }} required />
        </div>
        <button type="submit" style={{ padding: "0.75rem", marginTop: "1rem", cursor: "pointer", background: "#3b82f6", color: "white", border: "none", borderRadius: "4px", fontSize: "1rem", fontWeight: "bold" }}>
          Entrar
        </button>
        {erro && <p style={{ color: "#ef4444", textAlign: "center", margin: 0, fontSize: "0.9rem" }}>{erro}</p>}
      </form>
    </div>
  );
}

export default App;