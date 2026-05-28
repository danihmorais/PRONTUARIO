import { useState, useEffect } from "react";
import { invoke } from "@tauri-apps/api/tauri";
import { dbQuery, dbExecute } from "../db";
import { getVersion } from "@tauri-apps/api/app";

interface Props {
  usuario: string;
  nivel: string;
}

interface Usuario {
  id: number;
  usuario: string;
  nivel: string;
}

const inputStyle: React.CSSProperties = { padding: "0.6rem 0.75rem" };

const labelStyle: React.CSSProperties = {
  fontSize: "13px",
  fontWeight: 600,
  color: "var(--text-muted)",
  marginBottom: "0.3rem",
  display: "block",
};

const secaoStyle: React.CSSProperties = {
  background: "var(--bg-panel)",
  borderRadius: "12px",
  padding: "1.5rem",
  border: "1px solid var(--border)",
  boxShadow: "var(--shadow-sm)",
  display: "flex",
  flexDirection: "column",
  gap: "1.25rem",
};

const tituloSecao = (texto: string) => (
  <div style={{ borderBottom: "1px solid var(--border)", paddingBottom: "0.75rem" }}>
    <h3 style={{ margin: 0, fontSize: "14px", fontWeight: 700, color: "var(--text-main)" }}>
      {texto}
    </h3>
  </div>
);

export default function Configuracoes({ usuario, nivel }: Props) {
  const [versao, setVersao] = useState("—");

  const [senhaAtual, setSenhaAtual] = useState("");
  const [novaSenha, setNovaSenha] = useState("");
  const [confirmarSenha, setConfirmarSenha] = useState("");
  const [statusSenha, setStatusSenha] = useState<{ tipo: "sucesso" | "erro"; msg: string } | null>(null);
  const [salvandoSenha, setSalvandoSenha] = useState(false);

  const [usuarios, setUsuarios] = useState<Usuario[]>([]);
  const [novoUsuario, setNovoUsuario] = useState("");
  const [novaSenhaUser, setNovaSenhaUser] = useState("");
  const [novoNivel, setNovoNivel] = useState("operador");
  const [salvandoUser, setSalvandoUser] = useState(false);
  const [statusUser, setStatusUser] = useState<{ tipo: "sucesso" | "erro"; msg: string } | null>(null);

  useEffect(() => {
    getVersion().then(setVersao).catch(() => setVersao("—"));
    if (nivel === "admin") carregarUsuarios();
  }, [nivel]);

  const carregarUsuarios = async () => {
    try {
      const res = await dbQuery<Usuario>(
        "SELECT id, usuario, nivel FROM usuarios ORDER BY id ASC"
      );
      setUsuarios(res);
    } catch (e) {
      console.error(e);
    }
  };

  const alterarSenha = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatusSenha(null);

    if (novaSenha.length < 4) {
      setStatusSenha({ tipo: "erro", msg: "A nova senha deve ter pelo menos 4 caracteres." });
      return;
    }

    if (novaSenha !== confirmarSenha) {
      setStatusSenha({ tipo: "erro", msg: "A nova senha e a confirmação não coincidem." });
      return;
    }

    setSalvandoSenha(true);

    try {
      await invoke("alterar_senha", {
        usuario,
        senhaAtual,
        novaSenha,
      });

      setStatusSenha({ tipo: "sucesso", msg: "Senha alterada com sucesso." });
      setSenhaAtual("");
      setNovaSenha("");
      setConfirmarSenha("");
    } catch (err) {
      setStatusSenha({ tipo: "erro", msg: String(err) });
    } finally {
      setSalvandoSenha(false);
    }
  };

  const criarUsuario = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatusUser(null);

    if (novaSenhaUser.length < 4) {
      setStatusUser({ tipo: "erro", msg: "A senha deve ter pelo menos 4 caracteres." });
      return;
    }

    setSalvandoUser(true);

    try {
      const encoder = new TextEncoder();
      const data = encoder.encode(novaSenhaUser);

      const buffer = await globalThis.crypto.subtle.digest("SHA-256", data);

      const hash = Array.from(new Uint8Array(buffer))
        .map(b => b.toString(16).padStart(2, "0"))
        .join("");

      await dbExecute(
        "INSERT INTO usuarios (usuario, senha, nivel) VALUES (?, ?, ?)",
        [novoUsuario, hash, novoNivel]
      );

      setStatusUser({
        tipo: "sucesso",
        msg: `Usuário "${novoUsuario}" criado com sucesso.`,
      });

      setNovoUsuario("");
      setNovaSenhaUser("");
      setNovoNivel("operador");

      carregarUsuarios();
    } catch (err) {
      const msg = String(err);

      if (msg.includes("UNIQUE") || msg.includes("unique")) {
        setStatusUser({ tipo: "erro", msg: "Já existe um usuário com esse nome." });
      } else {
        setStatusUser({ tipo: "erro", msg });
      }
    } finally {
      setSalvandoUser(false);
    }
  };

  const deletarUsuario = async (id: number, nomeUser: string) => {
    if (nomeUser === usuario) {
      alert("Não é possível excluir o usuário atualmente logado.");
      return;
    }

    if (nomeUser === "admin") {
      alert("O usuário admin não pode ser excluído.");
      return;
    }

    if (!confirm(`Excluir o usuário "${nomeUser}"?`)) return;

    try {
      await dbExecute("DELETE FROM usuarios WHERE id = ?", [String(id)]);
      carregarUsuarios();
    } catch (e) {
      alert("Erro ao excluir: " + e);
    }
  };

  const msgStyle = (tipo: "sucesso" | "erro"): React.CSSProperties => ({
    padding: "0.55rem 0.85rem",
    borderRadius: "8px",
    fontSize: "13px",
    fontWeight: 500,
    background: tipo === "sucesso" ? "rgba(5,150,105,0.1)" : "rgba(220,38,38,0.1)",
    color: tipo === "sucesso" ? "#059669" : "#dc2626",
    border: `1px solid ${
      tipo === "sucesso" ? "rgba(5,150,105,0.2)" : "rgba(220,38,38,0.2)"
    }`,
  });

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1.5rem", maxWidth: "700px" }}>
      <div style={secaoStyle}>
        {tituloSecao("Informações do Sistema")}
        <div style={{ display: "flex", flexDirection: "column", gap: "0.6rem" }}>
          {[
            { label: "Usuário logado", valor: usuario },
            { label: "Nível de acesso", valor: nivel === "admin" ? "Administrador" : "Operador" },
            { label: "Versão do sistema", valor: versao },
          ].map(({ label, valor }) => (
            <div
              key={label}
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                padding: "0.6rem 0",
                borderBottom: "1px solid var(--border)",
              }}
            >
              <span style={{ fontSize: "13px", color: "var(--text-muted)" }}>{label}</span>
              <span style={{ fontSize: "13px", fontWeight: 600, color: "var(--text-main)" }}>
                {valor}
              </span>
            </div>
          ))}
        </div>
      </div>

      <div style={secaoStyle}>
        {tituloSecao("Alterar Minha Senha")}
        <form onSubmit={alterarSenha} style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
          <div>
            <label style={labelStyle}>Senha atual *</label>
            <input
              type="password"
              value={senhaAtual}
              onChange={e => setSenhaAtual(e.target.value)}
              required
              style={{ ...inputStyle, maxWidth: "360px" }}
            />
          </div>

          <div>
            <label style={labelStyle}>Nova senha *</label>
            <input
              type="password"
              value={novaSenha}
              onChange={e => setNovaSenha(e.target.value)}
              required
              style={{ ...inputStyle, maxWidth: "360px" }}
            />
          </div>

          <div>
            <label style={labelStyle}>Confirmar nova senha *</label>
            <input
              type="password"
              value={confirmarSenha}
              onChange={e => setConfirmarSenha(e.target.value)}
              required
              style={{ ...inputStyle, maxWidth: "360px" }}
            />
          </div>

          {statusSenha && <div style={msgStyle(statusSenha.tipo)}>{statusSenha.msg}</div>}

          <button
            type="submit"
            disabled={salvandoSenha}
            style={{
              padding: "0.6rem 1.5rem",
              background: salvandoSenha ? "var(--text-light)" : "var(--btn-primary)",
              color: "white",
              border: "none",
              cursor: salvandoSenha ? "not-allowed" : "pointer",
            }}
          >
            {salvandoSenha ? "Salvando..." : "Alterar Senha"}
          </button>
        </form>
      </div>

      {nivel === "admin" && (
        <>
          <div style={secaoStyle}>
            {tituloSecao("Criar Novo Usuário")}
            <form onSubmit={criarUsuario} style={{ display: "flex", flexWrap: "wrap", gap: "1rem" }}>
              <input
                value={novoUsuario}
                onChange={e => setNovoUsuario(e.target.value)}
                placeholder="Usuário"
                style={inputStyle}
              />

              <input
                type="password"
                value={novaSenhaUser}
                onChange={e => setNovaSenhaUser(e.target.value)}
                placeholder="Senha"
                style={inputStyle}
              />

              <select
                value={novoNivel}
                onChange={e => setNovoNivel(e.target.value)}
                style={inputStyle}
              >
                <option value="operador">Operador</option>
                <option value="admin">Administrador</option>
              </select>

              {statusUser && <div style={msgStyle(statusUser.tipo)}>{statusUser.msg}</div>}

              <button
                type="submit"
                disabled={salvandoUser}
                style={{
                  padding: "0.6rem 1.5rem",
                  background: salvandoUser ? "var(--text-light)" : "var(--btn-success)",
                  color: "white",
                  border: "none",
                  cursor: salvandoUser ? "not-allowed" : "pointer",
                }}
              >
                {salvandoUser ? "Criando..." : "Criar Usuário"}
              </button>
            </form>
          </div>

          <div style={{ background: "var(--bg-panel)", borderRadius: "12px", border: "1px solid var(--border)" }}>
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr>
                  {["ID", "Usuário", "Nível", "Ações"].map(h => (
                    <th key={h} style={{ padding: "0.75rem", textAlign: "left" }}>
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>

              <tbody>
                {usuarios.map(u => (
                  <tr key={u.id}>
                    <td style={{ padding: "0.75rem" }}>{u.id}</td>
                    <td style={{ padding: "0.75rem" }}>{u.usuario}</td>
                    <td style={{ padding: "0.75rem" }}>{u.nivel}</td>
                    <td style={{ padding: "0.75rem" }}>
                      <button onClick={() => deletarUsuario(u.id, u.usuario)}>
                        Excluir
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
}