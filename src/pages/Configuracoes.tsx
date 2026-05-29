import { useState, useEffect } from "react";
import { invoke } from "@tauri-apps/api/tauri";
import { dbQuery, dbExecute } from "../db";
import { getVersion } from "@tauri-apps/api/app";
import { save } from "@tauri-apps/api/dialog";
import { copyFile, exists } from "@tauri-apps/api/fs";
import { appDataDir, join } from "@tauri-apps/api/path";
import { verificarAtualizacao } from "../updater";

interface Props {
  usuario: string;
  nivel: string;
}

interface Usuario {
  id: number;
  usuario: string;
  nivel: string;
}

const inputStyle: React.CSSProperties = {
  padding: "0.58rem 0.75rem",
  borderRadius: "8px",
  border: "1px solid var(--border)",
  background: "var(--bg-input)",
  color: "var(--text-main)",
  fontSize: "13px",
  outline: "none",
  width: "100%",
  boxSizing: "border-box",
  minWidth: 0,
};

const labelStyle: React.CSSProperties = {
  fontSize: "12px",
  fontWeight: 600,
  color: "var(--text-muted)",
  marginBottom: "0.32rem",
  display: "block",
};

const secaoStyle: React.CSSProperties = {
  background: "var(--bg-panel)",
  borderRadius: "10px",
  padding: "0.95rem 1rem",
  border: "1px solid var(--border)",
  boxShadow: "var(--shadow-sm)",
  display: "flex",
  flexDirection: "column",
  gap: "0.9rem",
};

const tituloSecao = (texto: string) => (
  <div
    style={{
      borderBottom: "1px solid var(--border)",
      paddingBottom: "0.55rem",
    }}
  >
    <h3
      style={{
        margin: 0,
        fontSize: "14px",
        fontWeight: 700,
        color: "var(--text-main)",
      }}
    >
      {texto}
    </h3>
  </div>
);

export default function Configuracoes({ usuario, nivel }: Props) {
  const [versao, setVersao] = useState("—");
  const [senhaAtual, setSenhaAtual] = useState("");
  const [novaSenha, setNovaSenha] = useState("");
  const [confirmarSenha, setConfirmarSenha] = useState("");

  const [nomeProfissional, setNomeProfissional] = useState("");
  const [crefitoProfissional, setCrefitoProfissional] = useState("");
  const [salvandoProfissional, setSalvandoProfissional] = useState(false);

  const [statusSenha, setStatusSenha] = useState<{
    tipo: "sucesso" | "erro";
    msg: string;
  } | null>(null);

  const [salvandoSenha, setSalvandoSenha] = useState(false);
  const [usuarios, setUsuarios] = useState<Usuario[]>([]);
  const [novoUsuario, setNovoUsuario] = useState("");
  const [novaSenhaUser, setNovaSenhaUser] = useState("");
  const [novoNivel, setNovoNivel] = useState("operador");
  const [salvandoUser, setSalvandoUser] = useState(false);

  const [statusUser, setStatusUser] = useState<{
    tipo: "sucesso" | "erro";
    msg: string;
  } | null>(null);

  const [dbPath, setDbPath] = useState("Carregando...");
  const [fazendoBackup, setFazendoBackup] = useState(false);
  const [atualizando, setAtualizando] = useState(false);

  useEffect(() => { getVersion() .then(setVersao) .catch(() => setVersao("—")); const carregarBanco = async () => { try { const dir = await appDataDir(); const caminhos = [ await join(dir, "prontuario.db"), await join(dir, ".prontuario.db"), ]; for (const caminho of caminhos) { const existe = await exists(caminho); if (existe) { setDbPath(caminho); return; } } setDbPath(caminhos[0]); } catch { setDbPath("Não encontrado"); } }; carregarBanco(); carregarProfissional(); if (nivel === "admin") { carregarUsuarios(); } }, [nivel]);
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
      setStatusSenha({
        tipo: "erro",
        msg: "A nova senha deve ter pelo menos 4 caracteres.",
      });
      return;
    }

    if (novaSenha !== confirmarSenha) {
      setStatusSenha({
        tipo: "erro",
        msg: "A nova senha e a confirmação não coincidem.",
      });
      return;
    }

    setSalvandoSenha(true);

    try {
      await invoke("alterar_senha", {
        usuario,
        senhaAtual,
        novaSenha,
      });

      setStatusSenha({
        tipo: "sucesso",
        msg: "Senha alterada com sucesso.",
      });

      setSenhaAtual("");
      setNovaSenha("");
      setConfirmarSenha("");
    } catch (err) {
      setStatusSenha({
        tipo: "erro",
        msg: String(err),
      });
    } finally {
      setSalvandoSenha(false);
    }
  };

  const criarUsuario = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatusUser(null);

    if (novaSenhaUser.length < 4) {
      setStatusUser({
        tipo: "erro",
        msg: "A senha deve ter pelo menos 4 caracteres.",
      });
      return;
    }

    setSalvandoUser(true);

    try {
      const encoder = new TextEncoder();
      const data = encoder.encode(novaSenhaUser);
      const buffer = await globalThis.crypto.subtle.digest("SHA-256", data);

      const hash = Array.from(new Uint8Array(buffer))
        .map((b) => b.toString(16).padStart(2, "0"))
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
        setStatusUser({
          tipo: "erro",
          msg: "Já existe um usuário com esse nome.",
        });
      } else {
        setStatusUser({
          tipo: "erro",
          msg,
        });
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

    if (nomeUser === "admin") return;

    if (!confirm(`Excluir o usuário "${nomeUser}"?`)) return;

    try {
      await dbExecute("DELETE FROM usuarios WHERE id = ?", [String(id)]);
      carregarUsuarios();
    } catch (e) {
      alert("Erro ao excluir: " + e);
    }
  };

  const realizarBackup = async () => {
    try {
      setFazendoBackup(true);
      const destino = await save({
        defaultPath: `backup-prontuario-${Date.now()}.db`,
        filters: [{ name: "Database", extensions: ["db"] }],
      });

      if (!destino) return;

      await copyFile(dbPath, destino);
      alert("Backup realizado com sucesso.");
    } catch (e) {
      alert("Erro ao realizar backup: " + e);
    } finally {
      setFazendoBackup(false);
    }
  };

  const acionarUpdate = () => {
    verificarAtualizacao(setAtualizando);
  };

  const carregarProfissional = async () => {
    try {
      const res = await dbQuery<{
        nome_profissional: string;
        crefito_profissional: string;
      }>(
        `SELECT
          nome_profissional,
          crefito_profissional
        FROM configuracoes
        LIMIT 1`
      );

      if (res.length > 0) {
        setNomeProfissional(res[0].nome_profissional || "");
        setCrefitoProfissional(res[0].crefito_profissional || "");
      }
    } catch (e) {
      console.error(e);
    }
  };

  const salvarProfissional = async ( e: React.FormEvent ) => { e.preventDefault(); try { setSalvandoProfissional(true); await dbExecute( `UPDATE configuracoes SET nome_profissional = ?, crefito_profissional = ? WHERE id = 1`, [ nomeProfissional, crefitoProfissional, ] ); alert("Dados profissionais salvos."); } catch (e) { alert("Erro ao salvar: " + e); } finally { setSalvandoProfissional(false); } };

  const msgStyle = (tipo: "sucesso" | "erro"): React.CSSProperties => ({
    padding: "0.55rem 0.85rem",
    borderRadius: "8px",
    fontSize: "12px",
    fontWeight: 500,
    background: tipo === "sucesso" ? "rgba(5,150,105,0.1)" : "rgba(220,38,38,0.1)",
    color: tipo === "sucesso" ? "#059669" : "#dc2626",
    border: `1px solid ${
      tipo === "sucesso" ? "rgba(5,150,105,0.2)" : "rgba(220,38,38,0.2)"
    }`,
  });

  return (
    <>
      {atualizando && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: "rgba(0,0,0,0.7)",
            zIndex: 9999,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            color: "white",
            backdropFilter: "blur(4px)",
          }}
        >
          <div
            style={{
              width: "40px",
              height: "40px",
              border: "4px solid rgba(255,255,255,0.3)",
              borderTopColor: "white",
              borderRadius: "50%",
              animation: "spin 1s linear infinite",
              marginBottom: "1rem",
            }}
          />
          <h2 style={{ margin: "0 0 0.5rem" }}>Atualizando o Sistema</h2>
          <p style={{ margin: 0, opacity: 0.8, fontSize: "14px" }}>
            Baixando a nova versão. O aplicativo será reiniciado em instantes...
          </p>
          <style>
            {`
              @keyframes spin {
                to { transform: rotate(360deg); }
              }
            `}
          </style>
        </div>
      )}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "minmax(0, 1.2fr) minmax(0, 0.9fr)",
          gap: "1rem",
          alignItems: "start",
          opacity: atualizando ? 0.5 : 1,
          pointerEvents: atualizando ? "none" : "auto",
        }}
      >
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: "1rem",
            minWidth: 0,
          }}
        >
          <div style={secaoStyle}>
            {tituloSecao("Alterar Minha Senha")}

            <form
              onSubmit={alterarSenha}
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(3, minmax(0, 1fr))",
                gap: "0.7rem",
              }}
            >
              <div>
                <label style={labelStyle}>Senha atual</label>
                <input
                  type="password"
                  value={senhaAtual}
                  onChange={(e) => setSenhaAtual(e.target.value)}
                  required
                  style={inputStyle}
                />
              </div>

              <div>
                <label style={labelStyle}>Nova senha</label>
                <input
                  type="password"
                  value={novaSenha}
                  onChange={(e) => setNovaSenha(e.target.value)}
                  required
                  style={inputStyle}
                />
              </div>

              <div>
                <label style={labelStyle}>Confirmar</label>
                <input
                  type="password"
                  value={confirmarSenha}
                  onChange={(e) => setConfirmarSenha(e.target.value)}
                  required
                  style={inputStyle}
                />
              </div>

              {statusSenha && (
                <div
                  style={{
                    ...msgStyle(statusSenha.tipo),
                    gridColumn: "1 / -1",
                  }}
                >
                  {statusSenha.msg}
                </div>
              )}

              <button
                type="submit"
                disabled={salvandoSenha}
                style={{
                  padding: "0.62rem",
                  background: salvandoSenha
                    ? "var(--text-light)"
                    : "var(--btn-primary)",
                  color: "white",
                  border: "none",
                  borderRadius: "8px",
                  fontSize: "13px",
                  fontWeight: 600,
                  cursor: salvandoSenha ? "not-allowed" : "pointer",
                  gridColumn: "1 / -1",
                }}
              >
                {salvandoSenha ? "Salvando..." : "Alterar Senha"}
              </button>
            </form>
          </div>

          {nivel === "admin" && (
            <div style={secaoStyle}>
              {tituloSecao("Criar Novo Usuário")}

              <form
                onSubmit={criarUsuario}
                style={{
                  display: "grid",
                  gridTemplateColumns: "repeat(2, minmax(0, 1fr))",
                  gap: "0.7rem",
                }}
              >
                <div>
                  <label style={labelStyle}>Usuário</label>
                  <input
                    value={novoUsuario}
                    onChange={(e) => setNovoUsuario(e.target.value)}
                    placeholder="Usuário"
                    style={inputStyle}
                  />
                </div>

                <div>
                  <label style={labelStyle}>Senha</label>
                  <input
                    type="password"
                    value={novaSenhaUser}
                    onChange={(e) => setNovaSenhaUser(e.target.value)}
                    placeholder="Senha"
                    style={inputStyle}
                  />
                </div>

                <div>
                  <label style={labelStyle}>Nível</label>
                  <select
                    value={novoNivel}
                    onChange={(e) => setNovoNivel(e.target.value)}
                    style={inputStyle}
                  >
                    <option value="operador">Operador</option>
                    <option value="admin">Administrador</option>
                  </select>
                </div>

                <div
                  style={{
                    display: "flex",
                    alignItems: "end",
                  }}
                >
                  <button
                    type="submit"
                    disabled={salvandoUser}
                    style={{
                      padding: "0.62rem",
                      background: salvandoUser
                        ? "var(--text-light)"
                        : "var(--btn-success)",
                      color: "white",
                      border: "none",
                      borderRadius: "8px",
                      fontSize: "13px",
                      fontWeight: 600,
                      cursor: salvandoUser ? "not-allowed" : "pointer",
                      width: "100%",
                    }}
                  >
                    {salvandoUser ? "Criando..." : "Criar Usuário"}
                  </button>
                </div>

                {statusUser && (
                  <div
                    style={{
                      ...msgStyle(statusUser.tipo),
                      gridColumn: "1 / -1",
                    }}
                  >
                    {statusUser.msg}
                  </div>
                )}
              </form>
            </div>
          )}
        
        <div style={secaoStyle}>
        {tituloSecao("Dados do Profissional")}

        <form
          onSubmit={salvarProfissional}
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(2, minmax(0, 1fr))",
            gap: "0.7rem",
          }}
        >
          <div>
            <label style={labelStyle}>
              Nome do profissional
            </label>

            <input
              value={nomeProfissional}
              onChange={(e) =>
                setNomeProfissional(e.target.value)
              }
              placeholder="Nome completo"
              style={inputStyle}
            />
          </div>

          <div>
            <label style={labelStyle}>
              CREFITO
            </label>

            <input
              value={crefitoProfissional}
              onChange={(e) =>
                setCrefitoProfissional(e.target.value)
              }
              placeholder="Ex: 12345-F"
              style={inputStyle}
            />
          </div>

          <button
            type="submit"
            disabled={salvandoProfissional}
            style={{
              padding: "0.62rem",
              background: "var(--btn-success)",
              color: "white",
              border: "none",
              borderRadius: "8px",
              fontSize: "13px",
              fontWeight: 600,
              cursor: "pointer",
              gridColumn: "1 / -1",
            }}
          >
            {salvandoProfissional
              ? "Salvando..."
              : "Salvar Dados"}
          </button>
        </form>
        </div>
        </div>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: "1rem",
            minWidth: 0,
          }}
        >
          {nivel === "admin" && (
            <div
              style={{
                ...secaoStyle,
                padding: 0,
                overflow: "hidden",
              }}
            >
              <div style={{ padding: "0.95rem 1rem 0" }}>
                {tituloSecao("Usuários")}
              </div>

              <table
                style={{
                  width: "calc(100% - 2rem)",
                  margin: "0 1rem 1rem",
                  borderCollapse: "collapse",
                  tableLayout: "auto",
                }}
              >
                <thead>
                  <tr
                    style={{
                      background: "var(--bg-subtle)",
                    }}
                  >
                    {["ID", "Usuário", "Nível", "Ações"].map((h) => (
                      <th
                        key={h}
                        style={{
                          padding: "0.6rem 1rem",
                          textAlign: "left",
                          fontSize: "12px",
                        }}
                      >
                        {h}
                      </th>
                    ))}
                  </tr>
                </thead>

                <tbody>
                  {usuarios.map((u) => (
                    <tr
                      key={u.id}
                      style={{
                        borderTop: "1px solid var(--border)",
                      }}
                    >
                      <td
                        style={{
                          padding: "0.7rem 1rem",
                          fontSize: "12px",
                        }}
                      >
                        {u.id}
                      </td>

                      <td
                        style={{
                          padding: "0.7rem 0.85rem",
                          fontSize: "12px",
                          fontWeight: 500,
                        }}
                      >
                        {u.usuario}
                      </td>

                      <td
                        style={{
                          padding: "0.7rem 0.85rem",
                          fontSize: "12px",
                        }}
                      >
                        {u.nivel}
                      </td>

                      <td
                        style={{
                          padding: "0.7rem 0.85rem",
                        }}
                      >
                        {u.usuario !== "admin" && (
                          <button
                            onClick={() => deletarUsuario(u.id, u.usuario)}
                            style={{
                              background: "rgba(220,38,38,0.1)",
                              color: "var(--btn-danger)",
                              border: "none",
                              padding: "0.35rem 0.75rem",
                              borderRadius: "6px",
                              fontSize: "11px",
                              fontWeight: 600,
                              cursor: "pointer",
                            }}
                          >
                            Excluir
                          </button>
                        )}
                      </td>
                    </tr>
                  ))}

                  {usuarios.length === 0 && (
                    <tr>
                      <td
                        colSpan={4}
                        style={{
                          padding: "1.2rem",
                          textAlign: "center",
                          fontSize: "12px",
                          color: "var(--text-muted)",
                        }}
                      >
                        Nenhum usuário encontrado.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          )}

          <div
            style={{
              ...secaoStyle,
              display: "flex",
              flexDirection: "column",
              gap: "0.75rem",
            }}
          >
            {tituloSecao("Informações do Sistema")}

            <div
              style={{
                display: "flex",
                flexDirection: "column",
                gap: "0.15rem",
              }}
            >
              {[
                { label: "Usuário do sistema", valor: usuario },
                {
                  label: "Nível",
                  valor: nivel === "admin" ? "Administrador" : "Operador",
                },
                { label: "Versão", valor: versao },
                { label: "Banco", valor: dbPath },
              ].map(({ label, valor }) => (
                <div
                  key={label}
                  style={{
                    display: "grid",
                    gridTemplateColumns: "145px minmax(0, 1fr)",
                    gap: "0.75rem",
                    alignItems: "start",
                    padding: "0.5rem 0",
                    borderBottom: "1px solid var(--border)",
                  }}
                >
                  <span
                    style={{
                      fontSize: "12px",
                      color: "var(--text-muted)",
                      paddingTop: "1px",
                    }}
                  >
                    {label}
                  </span>

                  <span
                    style={{
                      fontSize: "12px",
                      fontWeight: 600,
                      color: "var(--text-main)",
                      textAlign: "right",
                      wordBreak: "break-all",
                      lineHeight: 1.4,
                    }}
                  >
                    {valor}
                  </span>
                </div>
              ))}
            </div>

            <button
              onClick={realizarBackup}
              disabled={fazendoBackup}
              style={{
                padding: "0.62rem",
                background: "var(--btn-primary)",
                color: "white",
                border: "none",
                borderRadius: "8px",
                fontSize: "13px",
                fontWeight: 600,
                cursor: fazendoBackup ? "not-allowed" : "pointer",
                width: "100%",
              }}
            >
              {fazendoBackup ? "Realizando backup..." : "Realizar Backup"}
            </button>
            <button
              onClick={acionarUpdate}
              style={{
                padding: "0.62rem",
                background: "var(--bg-subtle)",
                color: "var(--text-main)",
                border: "1px solid var(--border)",
                borderRadius: "8px",
                fontSize: "13px",
                fontWeight: 600,
                cursor: "pointer",
                width: "100%",
              }}
            >
              Verificar Atualizações
            </button>
          </div>
        </div>      
      </div>
    </>
  );
}