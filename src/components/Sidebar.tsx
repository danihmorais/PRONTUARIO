import { useContext } from "react";
import { ThemeContext } from "../contexts/ThemeContext";
import logo from "../assets/logo.png";

interface SidebarProps {
  paginaAtual: string;
  setPaginaAtual: (pagina: string) => void;
  onLogout: () => void;
  usuario: string;
}

const menuItens = [
  { nome: "Dashboard", icone: "⊞" },
  { nome: "Pacientes", icone: "👤" },
  { nome: "Funcionários", icone: "👥" },
  { nome: "Consultas", icone: "📅" },
  { nome: "Prontuários", icone: "📋" },
  { nome: "Exportação", icone: "⬇" },
  { nome: "Configurações", icone: "⚙" },
];

export default function Sidebar({
  paginaAtual,
  setPaginaAtual,
  onLogout,
  usuario,
}: SidebarProps) {
  const { theme, toggleTheme } = useContext(ThemeContext);

  return (
    <aside
      style={{
        width: "200px",
        minWidth: "200px",
        background: "var(--sidebar-bg)",
        borderRight: "1px solid rgba(255,255,255,0.06)",
        display: "flex",
        flexDirection: "column",
        height: "100vh",
        position: "sticky",
        top: 0,
      }}
    >
      <div
        style={{
          padding: "1.35rem 1rem 1rem",
          borderBottom: "1px solid rgba(255,255,255,0.06)",
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "0.85rem",
          }}
        >
          <div
            style={{
              width: 42,
              height: 42,
              borderRadius: "12px",
              background: "rgba(255,255,255,0.04)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              overflow: "hidden",
              flexShrink: 0,
            }}
          >
            <img
              src={logo}
              alt="Logo"
              style={{
                width: "28px",
                height: "28px",
                objectFit: "contain",
              }}
            />
          </div>

          <div
            style={{
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              minWidth: 0,
              marginTop: "5px",
            }}
          >
            <span
              style={{
                fontSize: "15px",
                fontWeight: 700,
                color: "#f8fafc",
                lineHeight: 1.1,
                letterSpacing: "-0.02em",
              }}
            >
              Prontuário
            </span>

            <span
              style={{
                fontSize: "11px",
                color: "var(--sidebar-muted)",
                marginTop: "2px",
              }}
            >
              Sistema Clínico
            </span>
          </div>
        </div>
      </div>

      <nav
        style={{
          flex: 1,
          padding: "0.9rem 0.75rem",
          overflowY: "auto",
          display: "flex",
          flexDirection: "column",
          gap: "0.2rem",
        }}
      >
        {menuItens.map((item) => {
          const ativo = paginaAtual === item.nome;

          return (
            <button
              key={item.nome}
              onClick={() => setPaginaAtual(item.nome)}
              style={{
                display: "flex",
                alignItems: "center",
                gap: "0.8rem",
                width: "100%",
                minHeight: "44px",
                padding: "0 0.9rem",
                textAlign: "left",
                background: ativo
                  ? "var(--sidebar-active-bg)"
                  : "transparent",
                color: ativo ? "#60a5fa" : "var(--sidebar-text)",
                border: ativo
                  ? "1px solid rgba(59,130,246,0.22)"
                  : "1px solid transparent",
                borderRadius: "10px",
                cursor: "pointer",
                fontSize: "14px",
                fontWeight: ativo ? 600 : 500,
                transition: "all 0.15s ease",
              }}
              onMouseEnter={(e) => {
                if (!ativo) {
                  (
                    e.currentTarget as HTMLButtonElement
                  ).style.background = "var(--sidebar-hover)";
                }
              }}
              onMouseLeave={(e) => {
                if (!ativo) {
                  (
                    e.currentTarget as HTMLButtonElement
                  ).style.background = "transparent";
                }
              }}
            >
              <span
                style={{
                  width: "20px",
                  minWidth: "20px",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: "15px",
                  opacity: ativo ? 1 : 0.9,
                }}
              >
                {item.icone}
              </span>

              <span
                style={{
                  whiteSpace: "nowrap",
                  overflow: "hidden",
                  textOverflow: "ellipsis",
                }}
              >
                {item.nome}
              </span>
            </button>
          );
        })}
      </nav>

      <div
        style={{
          padding: "0.75rem",
          borderTop: "1px solid rgba(255,255,255,0.06)",
          display: "flex",
          flexDirection: "column",
          gap: "0.65rem",
        }}
      >
        <div
          style={{
            padding: "0.75rem",
            background: "rgba(255,255,255,0.04)",
            borderRadius: "10px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            gap: "0.75rem",
          }}
        >
          <div
            style={{
              minWidth: 0,
              flex: 1,
            }}
          >
            <div
              style={{
                fontSize: "11px",
                color: "var(--sidebar-muted)",
                marginBottom: "2px",
              }}
            >
              Usuário
            </div>

            <div
              style={{
                fontSize: "13px",
                fontWeight: 600,
                color: "var(--sidebar-text)",
                overflow: "hidden",
                textOverflow: "ellipsis",
                whiteSpace: "nowrap",
              }}
            >
              {usuario}
            </div>
          </div>

          <button
            onClick={toggleTheme}
            title="Alternar tema"
            style={{
              width: "36px",
              height: "36px",
              minWidth: "36px",
              background: "rgba(255,255,255,0.06)",
              border: "1px solid rgba(255,255,255,0.05)",
              color: "var(--sidebar-text)",
              borderRadius: "8px",
              cursor: "pointer",
              fontSize: "15px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            {theme === "light" ? "🌙" : "☀️"}
          </button>
        </div>

        <button
          onClick={onLogout}
          style={{
            width: "100%",
            height: "42px",
            background: "rgba(220,38,38,0.12)",
            color: "#f87171",
            border: "1px solid rgba(220,38,38,0.18)",
            borderRadius: "10px",
            cursor: "pointer",
            fontSize: "13px",
            fontWeight: 600,
            transition: "all 0.15s ease",
          }}
        >
          Sair do sistema
        </button>
      </div>
    </aside>
  );
}