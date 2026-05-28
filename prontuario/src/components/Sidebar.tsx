interface SidebarProps {
  paginaAtual: string;
  setPaginaAtual: (pagina: string) => void;
  onLogout: () => void;
}

export default function Sidebar({ paginaAtual, setPaginaAtual, onLogout }: SidebarProps) {
  const menuItens = ["Dashboard", "Pacientes", "Fisioterapeutas", "Funcionários", "Consultas", "Prontuários"];

  return (
    <aside style={{ width: "250px", background: "#1f2937", color: "white", display: "flex", flexDirection: "column" }}>
      <div style={{ padding: "1.5rem", fontSize: "1.25rem", fontWeight: "bold", borderBottom: "1px solid #374151" }}>
        Sistema Prontuário
      </div>
      <nav style={{ flex: 1, padding: "1rem 0" }}>
        {menuItens.map((item) => (
          <button
            key={item}
            onClick={() => setPaginaAtual(item)}
            style={{
              display: "block",
              width: "100%",
              padding: "1rem 1.5rem",
              textAlign: "left",
              background: paginaAtual === item ? "#374151" : "transparent",
              color: "white",
              border: "none",
              cursor: "pointer",
              fontSize: "1rem",
            }}
          >
            {item}
          </button>
        ))}
      </nav>
      <div style={{ padding: "1rem", borderTop: "1px solid #374151" }}>
        <button
          onClick={onLogout}
          style={{ width: "100%", padding: "0.75rem", background: "#ef4444", color: "white", border: "none", borderRadius: "4px", cursor: "pointer" }}
        >
          Sair
        </button>
      </div>
    </aside>
  );
}