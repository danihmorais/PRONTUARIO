import { useEffect, useMemo, useState } from "react";
import { dbExecute, dbQuery } from "../db";

interface Paciente {
  id: number;
  nome: string;
  cpf: string;
  rg: string;
  celular: string;
  telefone: string;
  email: string;
  data_nascimento: string;
  sexo: string;
  estado_civil: string;
  profissao: string;
  convenio: string;
  numero_convenio: string;
  cep: string;
  endereco: string;
  numero: string;
  bairro: string;
  cidade: string;
  estado: string;
  observacoes: string;
}

const inputStyle: React.CSSProperties = {
  width: "100%",
  padding: "0.55rem 0.75rem",
  borderRadius: "8px",
  border: "1px solid var(--border)",
  background: "var(--bg-input)",
  color: "var(--text-main)",
  fontSize: "13px",
  outline: "none",
  boxSizing: "border-box",
};

const textareaStyle: React.CSSProperties = {
  ...inputStyle,
  minHeight: "80px",
  resize: "vertical",
};

const labelStyle: React.CSSProperties = {
  fontSize: "12px",
  fontWeight: 700,
  color: "var(--text-muted)",
  marginBottom: "0.3rem",
  display: "block",
  textTransform: "uppercase",
  letterSpacing: "0.03em",
};

const sectionTitleStyle: React.CSSProperties = {
  fontSize: "12px",
  fontWeight: 700,
  color: "var(--text-main)",
  margin: "0 0 0.75rem",
  textTransform: "uppercase",
  letterSpacing: "0.04em",
};

export default function Pacientes() {
  const [aba, setAba] = useState<"cadastro" | "visualizar">("cadastro");

  const [pacientes, setPacientes] = useState<Paciente[]>([]);
  const [busca, setBusca] = useState("");
  const [editando, setEditando] = useState<Paciente | null>(null);

  const [nome, setNome] = useState("");
  const [cpf, setCpf] = useState("");
  const [rg, setRg] = useState("");
  const [celular, setCelular] = useState("");
  const [telefone, setTelefone] = useState("");
  const [email, setEmail] = useState("");
  const [dataNascimento, setDataNascimento] = useState("");
  const [sexo, setSexo] = useState("");
  const [estadoCivil, setEstadoCivil] = useState("");
  const [profissao, setProfissao] = useState("");
  const [convenio, setConvenio] = useState("");
  const [numeroConvenio, setNumeroConvenio] = useState("");
  const [cep, setCep] = useState("");
  const [endereco, setEndereco] = useState("");
  const [numero, setNumero] = useState("");
  const [bairro, setBairro] = useState("");
  const [cidade, setCidade] = useState("");
  const [estado, setEstado] = useState("");
  const [observacoes, setObservacoes] = useState("");

  const [salvando, setSalvando] = useState(false);

  const carregar = async () => {
    try {
      const res = await dbQuery<Paciente>(`
        SELECT 
          id,
          nome,
          cpf,
          rg,
          celular,
          telefone,
          email,
          data_nascimento,
          sexo,
          estado_civil,
          profissao,
          convenio,
          numero_convenio,
          cep,
          endereco,
          numero,
          bairro,
          cidade,
          estado,
          observacoes
        FROM pacientes
        ORDER BY nome ASC
      `);

      setPacientes(res);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    carregar();
  }, []);

  const apenasNumeros = (valor: string) => {
    return valor.replace(/\D/g, "");
  };

  const mascararCPF = (valor: string) => {
    const v = apenasNumeros(valor).slice(0, 11);

    return v
      .replace(/^(\d{3})(\d)/, "$1.$2")
      .replace(/^(\d{3})\.(\d{3})(\d)/, "$1.$2.$3")
      .replace(/\.(\d{3})(\d)/, ".$1-$2");
  };

  const mascararTelefone = (valor: string) => {
    const v = apenasNumeros(valor).slice(0, 11);

    if (v.length <= 10) {
      return v
        .replace(/^(\d{2})(\d)/g, "($1) $2")
        .replace(/(\d{4})(\d)/, "$1-$2");
    }

    return v
      .replace(/^(\d{2})(\d)/g, "($1) $2")
      .replace(/(\d{5})(\d)/, "$1-$2");
  };

  const mascararCEP = (valor: string) => {
    const v = apenasNumeros(valor).slice(0, 8);

    return v.replace(/^(\d{5})(\d)/, "$1-$2");
  };

  const validarCPF = (cpfValor: string) => {
    const cpfLimpo = apenasNumeros(cpfValor);

    if (cpfLimpo.length !== 11) return false;

    if (/^(\d)\1+$/.test(cpfLimpo)) return false;

    let soma = 0;

    for (let i = 0; i < 9; i++) {
      soma += parseInt(cpfLimpo.charAt(i)) * (10 - i);
    }

    let resto = (soma * 10) % 11;

    if (resto === 10) resto = 0;

    if (resto !== parseInt(cpfLimpo.charAt(9))) {
      return false;
    }

    soma = 0;

    for (let i = 0; i < 10; i++) {
      soma += parseInt(cpfLimpo.charAt(i)) * (11 - i);
    }

    resto = (soma * 10) % 11;

    if (resto === 10) resto = 0;

    return resto === parseInt(cpfLimpo.charAt(10));
  };

  const limparForm = () => {
    setNome("");
    setCpf("");
    setRg("");
    setCelular("");
    setTelefone("");
    setEmail("");
    setDataNascimento("");
    setSexo("");
    setEstadoCivil("");
    setProfissao("");
    setConvenio("");
    setNumeroConvenio("");
    setCep("");
    setEndereco("");
    setNumero("");
    setBairro("");
    setCidade("");
    setEstado("");
    setObservacoes("");
    setEditando(null);
  };

  const preencherEdicao = (p: Paciente) => {
    setEditando(p);

    setNome(p.nome ?? "");
    setCpf(p.cpf ?? "");
    setRg(p.rg ?? "");
    setCelular(p.celular ?? "");
    setTelefone(p.telefone ?? "");
    setEmail(p.email ?? "");
    setDataNascimento(p.data_nascimento ?? "");
    setSexo(p.sexo ?? "");
    setEstadoCivil(p.estado_civil ?? "");
    setProfissao(p.profissao ?? "");
    setConvenio(p.convenio ?? "");
    setNumeroConvenio(p.numero_convenio ?? "");
    setCep(p.cep ?? "");
    setEndereco(p.endereco ?? "");
    setNumero(p.numero ?? "");
    setBairro(p.bairro ?? "");
    setCidade(p.cidade ?? "");
    setEstado(p.estado ?? "");
    setObservacoes(p.observacoes ?? "");

    setAba("cadastro");

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  const salvar = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!nome.trim()) {
      alert("Informe o nome do paciente.");
      return;
    }

    if (!validarCPF(cpf)) {
      alert("CPF inválido.");
      return;
    }

    setSalvando(true);

    try {
      if (editando) {
        await dbExecute(
          `
            UPDATE pacientes SET
              nome=?,
              cpf=?,
              rg=?,
              celular=?,
              telefone=?,
              email=?,
              data_nascimento=?,
              sexo=?,
              estado_civil=?,
              profissao=?,
              convenio=?,
              numero_convenio=?,
              cep=?,
              endereco=?,
              numero=?,
              bairro=?,
              cidade=?,
              estado=?,
              observacoes=?
            WHERE id=?
          `,
          [
            nome,
            cpf,
            rg,
            celular,
            telefone,
            email,
            dataNascimento,
            sexo,
            estadoCivil,
            profissao,
            convenio,
            numeroConvenio,
            cep,
            endereco,
            numero,
            bairro,
            cidade,
            estado,
            observacoes,
            String(editando.id),
          ]
        );
      } else {
        await dbExecute(
          `
            INSERT INTO pacientes (
              nome,
              cpf,
              rg,
              celular,
              telefone,
              email,
              data_nascimento,
              sexo,
              estado_civil,
              profissao,
              convenio,
              numero_convenio,
              cep,
              endereco,
              numero,
              bairro,
              cidade,
              estado,
              observacoes
            )
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
          `,
          [
            nome,
            cpf,
            rg,
            celular,
            telefone,
            email,
            dataNascimento,
            sexo,
            estadoCivil,
            profissao,
            convenio,
            numeroConvenio,
            cep,
            endereco,
            numero,
            bairro,
            cidade,
            estado,
            observacoes,
          ]
        );
      }

      limparForm();
      await carregar();

      alert(
        editando
          ? "Paciente atualizado com sucesso."
          : "Paciente cadastrado com sucesso."
      );
    } catch (e) {
      alert("Erro ao salvar: " + e);
    } finally {
      setSalvando(false);
    }
  };

  const deletar = async (id: number, nomePaciente: string) => {
    if (
      !confirm(
        `Excluir o paciente "${nomePaciente}"?\n\nEsta ação não pode ser desfeita.`
      )
    ) {
      return;
    }

    try {
      await dbExecute("DELETE FROM pacientes WHERE id = ?", [String(id)]);
      carregar();
    } catch (e: any) {
      if (String(e).includes("FOREIGN KEY constraint failed")) {
        alert(
          "Não é possível excluir este paciente, pois ele possui consultas ou prontuários registrados."
        );
      } else {
        alert("Erro ao excluir: " + e);
      }
    }
  };

  const filtrados = useMemo(() => {
    return pacientes.filter((p) => {
      const termo = busca.toLowerCase();

      return (
        p.nome?.toLowerCase().includes(termo) ||
        p.cpf?.includes(busca) ||
        p.celular?.includes(busca) ||
        p.email?.toLowerCase().includes(termo)
      );
    });
  }, [pacientes, busca]);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "1rem",
      }}
    >
      <div
        style={{
          display: "flex",
          gap: "0.5rem",
        }}
      >
        <button
          onClick={() => setAba("cadastro")}
          style={{
            padding: "0.55rem 1rem",
            borderRadius: "8px",
            border: "1px solid var(--border)",
            background:
              aba === "cadastro"
                ? "var(--btn-primary)"
                : "transparent",
            color:
              aba === "cadastro"
                ? "white"
                : "var(--text-muted)",
            fontSize: "13px",
            fontWeight: 600,
            cursor: "pointer",
          }}
        >
          Cadastro
        </button>

        <button
          onClick={() => setAba("visualizar")}
          style={{
            padding: "0.55rem 1rem",
            borderRadius: "8px",
            border: "1px solid var(--border)",
            background:
              aba === "visualizar"
                ? "var(--btn-primary)"
                : "transparent",
            color:
              aba === "visualizar"
                ? "white"
                : "var(--text-muted)",
            fontSize: "13px",
            fontWeight: 600,
            cursor: "pointer",
          }}
        >
          Visualizar Pacientes
        </button>
      </div>

      {aba === "cadastro" && (
        <div
          style={{
            background: "var(--bg-panel)",
            borderRadius: "12px",
            padding: "1.2rem",
            border: "1px solid var(--border)",
            boxShadow: "var(--shadow-sm)",
          }}
        >
          <h3
            style={{
              margin: "0 0 1rem",
              fontSize: "14px",
              fontWeight: 700,
              color: "var(--text-main)",
            }}
          >
            {editando
              ? `Editar Paciente — ${editando.nome}`
              : "Novo Paciente"}
          </h3>

          <form
            onSubmit={salvar}
            style={{
              display: "flex",
              flexDirection: "column",
              gap: "1rem",
            }}
          >
            <div>
              <h4 style={sectionTitleStyle}>Dados Pessoais</h4>

              <div
                style={{
                  display: "grid",
                  gridTemplateColumns:
                    "repeat(auto-fit, minmax(180px, 1fr))",
                  gap: "0.75rem",
                }}
              >
                <div>
                  <label style={labelStyle}>Nome Completo *</label>

                  <input
                    value={nome}
                    onChange={(e) => setNome(e.target.value)}
                    required
                    style={inputStyle}
                  />
                </div>

                <div>
                  <label style={labelStyle}>CPF *</label>

                  <input
                    value={cpf}
                    onChange={(e) =>
                      setCpf(mascararCPF(e.target.value))
                    }
                    maxLength={14}
                    required
                    style={inputStyle}
                  />
                </div>

                <div>
                  <label style={labelStyle}>RG</label>

                  <input
                    value={rg}
                    onChange={(e) => setRg(e.target.value)}
                    style={inputStyle}
                  />
                </div>

                <div>
                  <label style={labelStyle}>Nascimento</label>

                  <input
                    type="date"
                    value={dataNascimento}
                    onChange={(e) =>
                      setDataNascimento(e.target.value)
                    }
                    style={inputStyle}
                  />
                </div>

                <div>
                  <label style={labelStyle}>Sexo</label>

                  <select
                    value={sexo}
                    onChange={(e) => setSexo(e.target.value)}
                    style={inputStyle}
                  >
                    <option value="">Selecione...</option>
                    <option value="Masculino">Masculino</option>
                    <option value="Feminino">Feminino</option>
                  </select>
                </div>

                <div>
                  <label style={labelStyle}>Estado Civil</label>

                  <select
                    value={estadoCivil}
                    onChange={(e) =>
                      setEstadoCivil(e.target.value)
                    }
                    style={inputStyle}
                  >
                    <option value="">Selecione...</option>
                    <option value="Solteiro(a)">
                      Solteiro(a)
                    </option>
                    <option value="Casado(a)">
                      Casado(a)
                    </option>
                    <option value="Divorciado(a)">
                      Divorciado(a)
                    </option>
                    <option value="Viúvo(a)">Viúvo(a)</option>
                  </select>
                </div>

                <div>
                  <label style={labelStyle}>Profissão</label>

                  <input
                    value={profissao}
                    onChange={(e) =>
                      setProfissao(e.target.value)
                    }
                    style={inputStyle}
                  />
                </div>
              </div>
            </div>

            <div>
              <h4 style={sectionTitleStyle}>Contato</h4>

              <div
                style={{
                  display: "grid",
                  gridTemplateColumns:
                    "repeat(auto-fit, minmax(180px, 1fr))",
                  gap: "0.75rem",
                }}
              >
                <div>
                  <label style={labelStyle}>Celular</label>

                  <input
                    value={celular}
                    onChange={(e) =>
                      setCelular(
                        mascararTelefone(e.target.value)
                      )
                    }
                    maxLength={15}
                    style={inputStyle}
                  />
                </div>

                <div>
                  <label style={labelStyle}>Telefone</label>

                  <input
                    value={telefone}
                    onChange={(e) =>
                      setTelefone(
                        mascararTelefone(e.target.value)
                      )
                    }
                    maxLength={15}
                    style={inputStyle}
                  />
                </div>

                <div>
                  <label style={labelStyle}>E-mail</label>

                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    style={inputStyle}
                  />
                </div>
              </div>
            </div>

            <div>
              <h4 style={sectionTitleStyle}>Endereço</h4>

              <div
                style={{
                  display: "grid",
                  gridTemplateColumns:
                    "repeat(auto-fit, minmax(180px, 1fr))",
                  gap: "0.75rem",
                }}
              >
                <div>
                  <label style={labelStyle}>CEP</label>

                  <input
                    value={cep}
                    onChange={(e) =>
                      setCep(mascararCEP(e.target.value))
                    }
                    maxLength={9}
                    style={inputStyle}
                  />
                </div>

                <div style={{ gridColumn: "span 2" }}>
                  <label style={labelStyle}>Endereço</label>

                  <input
                    value={endereco}
                    onChange={(e) =>
                      setEndereco(e.target.value)
                    }
                    style={inputStyle}
                  />
                </div>

                <div>
                  <label style={labelStyle}>Número</label>

                  <input
                    value={numero}
                    onChange={(e) => setNumero(e.target.value)}
                    style={inputStyle}
                  />
                </div>

                <div>
                  <label style={labelStyle}>Bairro</label>

                  <input
                    value={bairro}
                    onChange={(e) => setBairro(e.target.value)}
                    style={inputStyle}
                  />
                </div>

                <div>
                  <label style={labelStyle}>Cidade</label>

                  <input
                    value={cidade}
                    onChange={(e) => setCidade(e.target.value)}
                    style={inputStyle}
                  />
                </div>

                <div>
                  <label style={labelStyle}>Estado</label>

                  <input
                    value={estado}
                    onChange={(e) => setEstado(e.target.value)}
                    maxLength={2}
                    style={inputStyle}
                  />
                </div>
              </div>
            </div>

            <div>
              <h4 style={sectionTitleStyle}>Convênio</h4>

              <div
                style={{
                  display: "grid",
                  gridTemplateColumns:
                    "repeat(auto-fit, minmax(180px, 1fr))",
                  gap: "0.75rem",
                }}
              >
                <div>
                  <label style={labelStyle}>Convênio</label>

                  <input
                    value={convenio}
                    onChange={(e) =>
                      setConvenio(e.target.value)
                    }
                    style={inputStyle}
                  />
                </div>

                <div>
                  <label style={labelStyle}>
                    Número da Carteira
                  </label>

                  <input
                    value={numeroConvenio}
                    onChange={(e) =>
                      setNumeroConvenio(e.target.value)
                    }
                    style={inputStyle}
                  />
                </div>
              </div>
            </div>

            <div>
              <h4 style={sectionTitleStyle}>Observações</h4>

              <textarea
                value={observacoes}
                onChange={(e) =>
                  setObservacoes(e.target.value)
                }
                style={textareaStyle}
              />
            </div>

            <div
              style={{
                display: "flex",
                gap: "0.75rem",
              }}
            >
              <button
                type="submit"
                disabled={salvando}
                style={{
                  padding: "0.65rem 1.4rem",
                  background: "var(--btn-success)",
                  color: "white",
                  border: "none",
                  borderRadius: "8px",
                  fontSize: "13px",
                  fontWeight: 600,
                  cursor: "pointer",
                }}
              >
                {salvando
                  ? "Salvando..."
                  : editando
                  ? "Salvar Alterações"
                  : "Cadastrar Paciente"}
              </button>

              {editando && (
                <button
                  type="button"
                  onClick={limparForm}
                  style={{
                    padding: "0.65rem 1.2rem",
                    background: "transparent",
                    color: "var(--text-muted)",
                    border: "1px solid var(--border)",
                    borderRadius: "8px",
                    fontSize: "13px",
                    cursor: "pointer",
                  }}
                >
                  Cancelar
                </button>
              )}
            </div>
          </form>
        </div>
      )}

      {aba === "visualizar" && (
        <div
          style={{
            background: "var(--bg-panel)",
            borderRadius: "12px",
            border: "1px solid var(--border)",
            boxShadow: "var(--shadow-sm)",
            overflow: "hidden",
          }}
        >
          <div
            style={{
              padding: "1rem",
              borderBottom: "1px solid var(--border)",
              display: "flex",
              gap: "1rem",
              alignItems: "center",
            }}
          >
            <input
              value={busca}
              onChange={(e) => setBusca(e.target.value)}
              placeholder="Buscar paciente..."
              style={{
                ...inputStyle,
                maxWidth: "320px",
              }}
            />

            <span
              style={{
                marginLeft: "auto",
                fontSize: "12px",
                color: "var(--text-muted)",
              }}
            >
              {filtrados.length} paciente
              {filtrados.length !== 1 ? "s" : ""}
            </span>
          </div>

          <div style={{ overflowX: "auto" }}>
            <table>
              <thead>
                <tr
                  style={{
                    background: "var(--bg-subtle)",
                  }}
                >
                  {[
                    "ID",
                    "Nome",
                    "CPF",
                    "Celular",
                    "E-mail",
                    "Cidade",
                    "Ações",
                  ].map((h) => (
                    <th
                      key={h}
                      style={{
                        padding: "0.75rem 1rem",
                        textAlign: "left",
                        whiteSpace: "nowrap",
                        fontSize: "12px",
                      }}
                    >
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>

              <tbody>
                {filtrados.map((p) => (
                  <tr
                    key={p.id}
                    style={{
                      borderTop: "1px solid var(--border)",
                    }}
                  >
                    <td
                      style={{
                        padding: "0.75rem 1rem",
                        fontSize: "12px",
                        color: "var(--text-muted)",
                      }}
                    >
                      {p.id}
                    </td>

                    <td
                      style={{
                        padding: "0.75rem 1rem",
                        fontSize: "13px",
                        fontWeight: 600,
                      }}
                    >
                      {p.nome}
                    </td>

                    <td
                      style={{
                        padding: "0.75rem 1rem",
                        fontSize: "12px",
                        color: "var(--text-muted)",
                      }}
                    >
                      {p.cpf}
                    </td>

                    <td
                      style={{
                        padding: "0.75rem 1rem",
                        fontSize: "12px",
                        color: "var(--text-muted)",
                      }}
                    >
                      {p.celular || "—"}
                    </td>

                    <td
                      style={{
                        padding: "0.75rem 1rem",
                        fontSize: "12px",
                        color: "var(--text-muted)",
                      }}
                    >
                      {p.email || "—"}
                    </td>

                    <td
                      style={{
                        padding: "0.75rem 1rem",
                        fontSize: "12px",
                        color: "var(--text-muted)",
                      }}
                    >
                      {p.cidade || "—"}
                    </td>

                    <td
                      style={{
                        padding: "0.75rem 1rem",
                      }}
                    >
                      <div
                        style={{
                          display: "flex",
                          gap: "0.5rem",
                        }}
                      >
                        <button
                          onClick={() => preencherEdicao(p)}
                          style={{
                            background:
                              "rgba(37,99,235,0.1)",
                            color: "var(--btn-primary)",
                            border: "none",
                            padding: "0.35rem 0.8rem",
                            borderRadius: "6px",
                            fontSize: "12px",
                            fontWeight: 600,
                            cursor: "pointer",
                          }}
                        >
                          Editar
                        </button>

                        <button
                          onClick={() =>
                            deletar(p.id, p.nome)
                          }
                          style={{
                            background:
                              "rgba(220,38,38,0.1)",
                            color: "var(--btn-danger)",
                            border: "none",
                            padding: "0.35rem 0.8rem",
                            borderRadius: "6px",
                            fontSize: "12px",
                            fontWeight: 600,
                            cursor: "pointer",
                          }}
                        >
                          Excluir
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}

                {filtrados.length === 0 && (
                  <tr>
                    <td
                      colSpan={7}
                      style={{
                        padding: "2rem",
                        textAlign: "center",
                        color: "var(--text-muted)",
                        fontSize: "13px",
                      }}
                    >
                      Nenhum paciente encontrado.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}