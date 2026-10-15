# Sienge MCP Server

MCP (Model Context Protocol) Server para integração com a API do Sienge.

Este servidor expõe ferramentas para interagir com os seguintes módulos do Sienge:
- **Credores**: Gestão de credores, informações bancárias e PIX
- **Empresas**: Gestão de empresas
- **Contratos**: Contratos de suprimentos, anexos e aditivos
- **Medições**: Medições de contratos de suprimentos
- **Empreendimentos**: Empreendimentos/obras e agrupamentos
- **Títulos a Pagar**: Gestão de títulos, parcelas e informações de pagamento
- **Contas a Receber**: Gestão de títulos a receber e parcelas
- **Planos Financeiros**: Gestão de categorias de pagamento
- **Contas-Correntes**: Consulta de contas bancárias
- **Centro de Custos**: Gestão de centros de custo
- **Estoque de Insumos**: Gestão de estoque e reservas
- **Nota Fiscal de Compra**: Gestão de notas fiscais de compra
- **Cotações de Preços**: Gestão de cotações e negociações
- **Solicitações de Compra**: Gestão de solicitações de compra
- **Pedidos de Compra**: Gestão de pedidos de compra, autorização e reprovação

**Total de 111 ferramentas disponíveis**

## Requisitos

- Python 3.10 ou superior
- Credenciais de acesso à API do Sienge (subdomínio, usuário e senha)

## Instalação

1. Clone ou baixe este repositório

2. Crie um ambiente virtual:
```bash
python -m venv venv
```

3. Ative o ambiente virtual:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -e .
```

## Configuração

1. Copie o arquivo de exemplo de variáveis de ambiente:
```bash
cp .env.example .env
```

2. Edite o arquivo `.env` com suas credenciais do Sienge:
```env
SIENGE_SUBDOMAIN=seu-subdominio
SIENGE_USERNAME=seu-usuario
SIENGE_PASSWORD=sua-senha
```

3. Configure o servidor MCP no seu cliente MCP (ex: Claude Desktop):

Adicione a seguinte configuração ao arquivo de configuração do MCP:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**Mac**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "sienge": {
      "command": "python",
      "args": [
        "-m",
        "sienge_mcp.server"
      ],
      "env": {
        "SIENGE_SUBDOMAIN": "seu-subdominio",
        "SIENGE_USERNAME": "seu-usuario",
        "SIENGE_PASSWORD": "sua-senha"
      }
    }
  }
}
```

Ou, se preferir usar variáveis de ambiente do sistema:

```json
{
  "mcpServers": {
    "sienge": {
      "command": "python",
      "args": [
        "-m",
        "sienge_mcp.server"
      ],
      "env": {
        "SIENGE_SUBDOMAIN": "${SIENGE_SUBDOMAIN}",
        "SIENGE_USERNAME": "${SIENGE_USERNAME}",
        "SIENGE_PASSWORD": "${SIENGE_PASSWORD}"
      }
    }
  }
}
```

## Ferramentas Disponíveis

### Credores

- `get_creditors`: Busca credores com filtros (CPF, CNPJ, nome)
- `get_creditor`: Busca um credor específico por ID
- `insert_creditor`: Insere um novo credor
- `update_creditor`: Atualiza informações de um credor
- `get_bank_informations`: Busca informações bancárias do credor
- `insert_bank_informations`: Insere informações bancárias
- `update_bank_informations`: Atualiza informações bancárias
- `get_pix_informations`: Busca informações PIX do credor
- `insert_pix_information`: Insere informações PIX
- `update_pix_information`: Atualiza informações PIX
- `update_creditor_phone`: Atualiza telefone do credor
- `update_creditor_contact`: Atualiza contato do credor
- `update_creditor_procurator`: Atualiza procurador do credor
- `update_creditor_agents`: Atualiza lista de representantes

### Empresas

- `get_companies`: Lista empresas com paginação
- `get_company`: Busca uma empresa específica por ID

### Contratos

- `get_supply_contract`: Consulta um contrato específico
- `get_supply_contracts_all`: Lista contratos com filtros e paginação
- `get_supply_contract_attachment`: Retorna anexo do contrato
- `get_supply_contract_attachments_all`: Lista anexos do contrato
- `get_supply_contract_buildings`: Consulta obras do contrato
- `get_supply_contract_addenda`: Consulta aditivos de obras
- `get_addendum_items`: Consulta itens de aditivo
- `authorize_supply_contract`: Autoriza um contrato
- `disapprove_supply_contract`: Reprova um contrato

### Medições

- `get_measurement`: Consulta uma medição específica
- `list_measurements`: Lista medições com filtros
- `post_measurement`: Cria uma nova medição
- `get_measurement_attachment`: Download de anexo de medição
- `list_measurement_attachments`: Lista anexos de medições
- `authorize_measurement`: Autoriza uma medição
- `get_measurement_clearing`: Retorna liberação de medição

### Empreendimentos

- `get_enterprises`: Lista empreendimentos com filtros
- `get_enterprise`: Busca um empreendimento específico
- `get_enterprise_groupings`: Busca agrupamentos de unidades

## Uso

Após configurar o servidor MCP, as ferramentas estarão disponíveis no seu cliente MCP (ex: Claude Desktop). Você pode usá-las para:

1. Consultar dados do Sienge
2. Criar e atualizar registros
3. Autorizar contratos e medições
4. Gerenciar credores e suas informações

## Exemplos

### Buscar todos os credores
```
get_creditors(limit=50)
```

### Buscar credor por CPF
```
get_creditors(cpf="12345678900")
```

### Buscar empresa específica
```
get_company(company_id=123)
```

### Listar contratos por período
```
get_supply_contracts_all(
    contract_start_date="2024-01-01",
    contract_end_date="2024-12-31",
    limit=100
)
```

### Autorizar um contrato
```
authorize_supply_contract(
    document_id=1,
    contract_number=100,
    observation={"text": "Contrato aprovado"}
)
```

## Estrutura do Projeto

```
sienge-mcp-server/
├── sienge_mcp/
│   ├── __init__.py
│   ├── client.py          # Cliente HTTP com autenticação
│   ├── creditors.py       # Módulo de Credores
│   ├── companies.py       # Módulo de Empresas
│   ├── contracts.py       # Módulo de Contratos
│   ├── measurements.py    # Módulo de Medições
│   ├── enterprises.py     # Módulo de Empreendimentos
│   └── server.py          # Servidor MCP principal
├── pyproject.toml         # Configuração do projeto
├── .env.example          # Exemplo de variáveis de ambiente
├── .env                   # Suas credenciais (não commitar)
└── README.md             # Este arquivo
```

## Segurança

- Nunca commitar o arquivo `.env` com suas credenciais
- Use variáveis de ambiente para armazenar credenciais sensíveis
- O arquivo `.env.example` serve como template, não contém dados reais

## Troubleshooting

### Erro: "Missing Sienge credentials"
Verifique se as variáveis de ambiente `SIENGE_SUBDOMAIN`, `SIENGE_USERNAME` e `SIENGE_PASSWORD` estão configuradas corretamente.

### Erro de autenticação
Verifique se suas credenciais do Sienge estão corretas e se você tem permissão para acessar a API.

### Timeout nas requisições
O cliente HTTP está configurado com timeout de 30 segundos. Se necessário, ajuste no arquivo `client.py`.

## Licença

Este projeto é fornecido como está para integração com a API do Sienge.
