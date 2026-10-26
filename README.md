# Customers MCP Server

Servidor MCP (Model Context Protocol) para gerenciamento de clientes.
Encapsula a API REST de clientes exposta por um repositório separado,
oferecendo ferramentas, prompts e recursos via stdio.

## Repositórios relacionados

- **API REST (Node.js/Fastify/MongoDB):** https://github.com/Brunospo/legacy-node-api
  - Endpoints base: `http://localhost:9999/v1` (configurável).
  - **Suba a API antes de iniciar este servidor MCP.**

## Arquitetura

```
src/api_mcp/
├── domain/           # Modelos de dados (Customer)
├── application/      # Serviços de aplicação (CustomerService)
├── infrastructure/   # Clientes HTTP (CustomerHTTPClient)
├── my_mcp/           # Servidor MCP
│   ├── server.py     # Configuração do servidor (BASE_URL)
│   ├── tools/        # list/create/get/update/delete_customer
│   ├── resources/    # api_info
│   └── prompts/      # find/update/delete_customer prompts
└── main.py           # Entry point
```

> Testes automatizados em `src/tests/`.

## Pré-requisitos

- Python 3.13+ e [uv](https://docs.astral.sh/uv/)
- API REST rodando (repositório acima): Node.js 20+, Docker (MongoDB)
- Porta 9999 disponível (ou ajuste `BASE_URL`)

## Instalação

```bash
uv sync
uv sync --group dev   # desenvolvimento (pytest, mcp[cli])
```

## Configuração

- `BASE_URL` em `src/api_mcp/my_mcp/server.py` (padrão: `http://localhost:9999/v1`).
- Para apontar para outra instância da API, altere essa constante e reinicie o MCP.

## Subindo a API (repositório separado)

```bash
git clone https://github.com/Brunospo/legacy-node-api
cd legacy-node-api
docker compose up -d mongodb
npm ci
npm start   # API em http://localhost:9999
```

## Executando o MCP

```bash
.venv/bin/python src/api_mcp/main.py
# ou
uv run python src/api_mcp/main.py
```

O servidor roda via stdio (standard input/output).

## Ferramentas Disponíveis

| Tool | Descrição |
|------|-----------|
| `list_customers` | Lista todos os clientes da API |
| `create_customer` | Cria um novo cliente (name, phone) |
| `get_customer` | Busca cliente via query (`_id`, `name`, `phone`; case-insensitive, parcial) |
| `update_customer` | Atualiza nome e telefone por ID |
| `delete_customer` | Remove cliente por ID |

## Prompts Disponíveis

| Prompt | Descrição |
|--------|-----------|
| `find_customer_prompt` | Monta consulta por `_id`, nome ou telefone |
| `update_customer_prompt` | Orienta atualização por ID |
| `delete_customer_prompt` | Orienta remoção por ID |

## Recursos Disponíveis

| Resource URI | Descrição |
|--------------|-----------|
| `customers://api-info` | Descreve a API REST encapsulada |

## Testes

```bash
uv run pytest
```

## Troubleshooting

- "Connection refused"/timeout: confirme que a API está rodando em 9999 e o MongoDB up (`docker compose up -d mongodb`).
- Porta em uso: ajuste a porta na API e atualize `BASE_URL`.
- MCP corrompendo stdio: mensagens de startup vão para stderr (já tratado).
- Campos vazios na busca: ignorados; nome/telefone comparados case-insensitively.

## Licença

MIT
" path="/home/brunospo/Documentos/eng_ia_modulo_3/mcp_api/customers_mcp/README.md