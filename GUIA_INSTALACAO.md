# Guia de Instalação Completo - Sienge MCP Server

## Passo 1: Instalação das Dependências

As dependências já foram instaladas com sucesso no ambiente virtual em:
`C:\Users\USER\Documents\projet\venv\`

## Passo 2: Configuração das Credenciais

As credenciais já foram configuradas no arquivo `.env`:
- Subdomínio: cctcontrol
- Usuário: cctcontrol-api
- Senha: QnMXmZbF24LWZujTrOJo6GVgAg3EPxeU

## Passo 3: Configurar no Claude Desktop (ou outro cliente MCP)

### Windows

1. Abra o arquivo de configuração do Claude Desktop:
   `%APPDATA%\Claude\claude_desktop_config.json`

2. Adicione a seguinte configuração:

```json
{
  "mcpServers": {
    "sienge": {
      "command": "C:\\Users\\USER\\Documents\\projet\\venv\\Scripts\\python.exe",
      "args": [
        "-m",
        "sienge_mcp.server"
      ],
      "env": {
        "SIENGE_SUBDOMAIN": "cctcontrol",
        "SIENGE_USERNAME": "cctcontrol-api",
        "SIENGE_PASSWORD": "QnMXmZbF24LWZujTrOJo6GVgAg3EPxeU"
      }
    }
  }
}
```

**IMPORTANTE**: Se você já tiver outros servidores MCP configurados, você precisa mesclar a configuração. Por exemplo, se seu arquivo já tiver algo, adicione apenas a parte `"sienge"` dentro de `"mcpServers"`.

Exemplo de arquivo completo:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\Users\\USER\\Documents"
      ]
    },
    "sienge": {
      "command": "C:\\Users\\USER\\Documents\\projet\\venv\\Scripts\\python.exe",
      "args": [
        "-m",
        "sienge_mcp.server"
      ],
      "env": {
        "SIENGE_SUBDOMAIN": "cctcontrol",
        "SIENGE_USERNAME": "cctcontrol-api",
        "SIENGE_PASSWORD": "QnMXmZbF24LWZujTrOJo6GVgAg3EPxeU"
      }
    }
  }
}
```

3. Salve o arquivo

4. Reinicie o Claude Desktop

## Passo 4: Verificar se está funcionando

Após reiniciar o Claude Desktop, você pode verificar se o servidor MCP está funcionando:

1. Abra o Claude Desktop
2. Clique no ícone de configurações (engrenagem)
3. Na seção "MCP Servers", você deve ver "sienge" listado
4. O status deve aparecer como "Connected" ou similar

## Passo 5: Usar as Ferramentas

Agora você pode usar as ferramentas do Sienge diretamente no Claude Desktop. Alguns exemplos:

### Buscar empresas
```
Use a ferramenta get_companies para listar as empresas disponíveis no Sienge.
```

### Buscar credores
```
Use a ferramenta get_creditors para buscar credores com filtros.
```

### Listar contratos
```
Use a ferramenta get_supply_contracts_all para listar contratos por período.
```

## Solução de Problemas

### Servidor não aparece no Claude Desktop

1. Verifique se o caminho do Python está correto:
   `C:\Users\USER\Documents\projet\venv\Scripts\python.exe`

2. Verifique se o arquivo de configuração JSON está válido (use um validador JSON online)

3. Verifique se o Claude Desktop foi reiniciado

### Erro de conexão

1. Verifique suas credenciais do Sienge
2. Verifique se o subdomínio está correto
3. Verifique se você tem permissão para acessar a API

### Erro de autenticação

1. Verifique se o usuário e senha estão corretos
2. Verifique se o usuário tem permissão para acessar a API REST do Sienge

## Arquivos do Projeto

- `sienge_mcp/client.py` - Cliente HTTP com autenticação
- `sienge_mcp/creditors.py` - Ferramentas de Credores
- `sienge_mcp/companies.py` - Ferramentas de Empresas
- `sienge_mcp/contracts.py` - Ferramentas de Contratos
- `sienge_mcp/measurements.py` - Ferramentas de Medições
- `sienge_mcp/enterprises.py` - Ferramentas de Empreendimentos
- `sienge_mcp/server.py` - Servidor MCP principal
- `.env` - Credenciais (não compartilhar este arquivo)
- `sienge-mcp-config.json` - Configuração exemplo para MCP

## Teste Manual

Para testar se o servidor MCP está funcionando manualmente:

```bash
cd C:\Users\USER\Documents\projet
venv\Scripts\python.exe -m sienge_mcp.server
```

Isso iniciará o servidor MCP em modo manual para verificação.
