import { useContext } from "react";
import { ThemeContext } from "../contexts/ThemeContext";

interface SidebarProps {
  paginaAtual: string;
  setPaginaAtual: (pagina: string) => void;
  onLogout: () => void;
}

export default function Sidebar({ paginaAtual, setPaginaAtual, onLogout }: SidebarProps) {
  const { theme, toggleTheme } = useContext(ThemeContext);
  const menuItens = ["Dashboard", "Pacientes", "Fisioterapeutas", "Funcionários", "Consultas", "Prontuários", "Exportação"];

  return (
    <aside style={{ width: "250px", background: "var(--sidebar-bg)", color: "var(--sidebar-text)", display: "flex", flexDirection: "column", transition: "background-color 0.3s" }}>
      <div style={{ padding: "1.5rem", fontSize: "1.25rem", fontWeight: "bold", borderBottom: "1px solid var(--border)", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <span>Prontuário</span>
        <button onClick={toggleTheme} style={{ background: "transparent", border: "1px solid var(--border)", color: "var(--sidebar-text)", padding: "0.2rem 0.5rem", borderRadius: "4px", cursor: "pointer", fontSize: "0.9rem" }} title="Alternar Tema">
          {theme === "light" ? "🌙" : "☀️"}
        </button>
      </div>
      <nav style={{ flex: 1, padding: "1rem 0", overflowY: "auto" }}>
        {menuItens.map((item) => (
          <button
            key={item}
            onClick={() => setPaginaAtual(item)}
            style={{
              display: "block",
              width: "100%",
              padding: "1rem 1.5rem",
              textAlign: "left",
              background: paginaAtual === item ? "var(--sidebar-hover)" : "transparent",
              color: "var(--sidebar-text)",
              border: "none",
              cursor: "pointer",
              fontSize: "1rem",
            }}
          >
            {item}
          </button>
        ))}
      </nav>
      <div style={{ padding: "1rem", borderTop: "1px solid var(--border)" }}>
        <button
          onClick={onLogout}
          style={{ width: "100%", padding: "0.75rem", background: "var(--btn-danger)", color: "white", border: "none", borderRadius: "4px", cursor: "pointer" }}
        >
          Sair
        </button>
      </div>
    </aside>
  );
}