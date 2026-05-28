import { useContext } from "react";
import { ThemeContext } from "../contexts/ThemeContext";

interface SidebarProps {
  paginaAtual: string;
  setPaginaAtual: (pagina: string) => void;
  onLogout: () => void;
  usuario: string;
}

const menuItens = [
  { nome: "Dashboard", icone: "⊡" },
  { nome: "Pacientes", icone: "👤" },
  { nome: "Fisioterapeutas", icone: "🩺" },
  { nome: "Funcionários", icone: "👥" },
  { nome: "Consultas", icone: "📅" },
  { nome: "Prontuários", icone: "📋" },
  { nome: "Exportação", icone: "⬇" },
  { nome: "Configurações", icone: "⚙" },
];

export default function Sidebar({ paginaAtual, setPaginaAtual, onLogout, usuario }: SidebarProps) {
  const { theme, toggleTheme } = useContext(ThemeContext);

  return (
    <aside style={{
      width: "240px",
      minWidth: "240px",
      background: "var(--sidebar-bg)",
      display: "flex",
      flexDirection: "column",
      height: "100vh",
      position: "sticky",
      top: 0,
    }}>
      <div style={{
        padding: "1.5rem 1.25rem 1rem",
        borderBottom: "1px solid rgba(255,255,255,0.06)",
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: "0.6rem", marginBottom: "0.25rem" }}>
          <div style={{
            width: 32, height: 32,
            background: "var(--btn-primary)",
            borderRadius: "8px",
            display: "flex", alignItems: "center", justifyContent: "center",
            fontSize: "16px",
            flexShrink: 0,
          }}>🏥</div>
          <span style={{ fontSize: "1rem", fontWeight: 700, color: "#f1f5f9", letterSpacing: "-0.02em" }}>
            Prontuário
          </span>
        </div>
        <div style={{ fontSize: "11px", color: "var(--sidebar-muted)", paddingLeft: "40px" }}>
          Sistema Clínico
        </div>
      </div>

      <nav style={{ flex: 1, padding: "0.75rem 0.75rem", overflowY: "auto", display: "flex", flexDirection: "column", gap: "2px" }}>
        {menuItens.map((item) => {
          const ativo = paginaAtual === item.nome;
          return (
            <button
              key={item.nome}
              onClick={() => setPaginaAtual(item.nome)}
              style={{
                display: "flex",
                alignItems: "center",
                gap: "0.75rem",
                width: "100%",
                padding: "0.6rem 0.75rem",
                textAlign: "left",
                background: ativo ? "var(--sidebar-active-bg)" : "transparent",
                color: ativo ? "#60a5fa" : "var(--sidebar-text)",
                border: ativo ? "1px solid rgba(59,130,246,0.25)" : "1px solid transparent",
                borderRadius: "8px",
                cursor: "pointer",
                fontSize: "14px",
                fontWeight: ativo ? 600 : 400,
                transition: "all 0.15s",
              }}
              onMouseEnter={(e) => { if (!ativo) (e.currentTarget as HTMLButtonElement).style.background = "var(--sidebar-hover)"; }}
              onMouseLeave={(e) => { if (!ativo) (e.currentTarget as HTMLButtonElement).style.background = "transparent"; }}
            >
              <span style={{ fontSize: "16px", width: "20px", textAlign: "center", flexShrink: 0 }}>{item.icone}</span>
              {item.nome}
            </button>
          );
        })}
      </nav>

      <div style={{ padding: "0.75rem", borderTop: "1px solid rgba(255,255,255,0.06)", display: "flex", flexDirection: "column", gap: "0.5rem" }}>
        <div style={{
          padding: "0.6rem 0.75rem",
          background: "rgba(255,255,255,0.04)",
          borderRadius: "8px",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}>
          <div>
            <div style={{ fontSize: "12px", color: "var(--sidebar-muted)" }}>Usuário</div>
            <div style={{ fontSize: "13px", fontWeight: 600, color: "var(--sidebar-text)" }}>{usuario}</div>
          </div>
          <button
            onClick={toggleTheme}
            title="Alternar tema"
            style={{
              background: "rgba(255,255,255,0.08)",
              border: "none",
              color: "var(--sidebar-text)",
              padding: "0.35rem 0.6rem",
              borderRadius: "6px",
              cursor: "pointer",
              fontSize: "14px",
            }}
          >
            {theme === "light" ? "🌙" : "☀️"}
          </button>
        </div>
        <button
          onClick={onLogout}
          style={{
            width: "100%",
            padding: "0.6rem",
            background: "rgba(220,38,38,0.15)",
            color: "#f87171",
            border: "1px solid rgba(220,38,38,0.2)",
            borderRadius: "8px",
            cursor: "pointer",
            fontSize: "13px",
            fontWeight: 600,
          }}
        >
          Sair do sistema
        </button>
      </div>
    </aside>
  );
}