# Guia do Servidor MCP HTTP para Sienge

## Status: ✅ FUNCIONANDO

O servidor MCP HTTP está online e funcionando em:
- **URL:** https://sienge-mcp-server.onrender.com
- **API Key:** `sienge-mcp-2024-secret-key-xyz123`

## Conexão com Claude Web

### URL do Conector:
```
https://sienge-mcp-server.onrender.com/mcp?api_key=sienge-mcp-2024-secret-key-xyz123
```

### Configuração:
1. Nome: Sienge
2. URL: (acima)
3. Autenticação: Sem login
4. Transporte: HTTP Streamable

## Teste Realizado

✅ **Conexão estabelecida com sucesso**
✅ **Dados reais do Sienge retornados**
- Consulta de títulos: 2 títulos encontrados
- Valor total: R$ 12.750,00
- Dados de 05/10/2026 a 31/10/2026

## Ferramentas Disponíveis

### Total Cadastrado: 113 ferramentas

**Módulos implementados:**
1. Credores (14 ferramentas)
2. Empresas (2 ferramentas)
3. Contratos (9 ferramentas)
4. Medições (7 ferramentas)
5. Empreendimentos (3 ferramentas)
6. Títulos a Pagar (17 ferramentas)
7. Contas a Receber (5 ferramentas)
8. Planos Financeiros (2 ferramentas)
9. Contas-Correntes (1 ferramenta)
10. Centro de Custos (4 ferramentas)
11. Estoque de Insumos (3 ferramentas)
12. Nota Fiscal de Compra (7 ferramentas)
13. Cotações de Preços (10 ferramentas)
14. Solicitações de Compra (9 ferramentas)
15. Pedidos de Compra (15 ferramentas)

### Observação:
O Claude Web pode limitar o número de ferramentas exibidas por sessão. Se precisar de funcionalidades específicas, peça explicitamente ao Claude.

## Exemplos de Uso

### Consultar títulos:
```
Liste os títulos a pagar do mês atual
```

### Consultar fornecedores:
```
Liste os credores/fornecedores cadastrados
```

### Consultar categorias:
```
Liste as categorias de pagamento disponíveis
```

### Pedidos de compra:
```
Liste os pedidos de compra em aberto
```

## Endpoints do Servidor

- **Health:** `/health`
- **MCP JSON-RPC:** `/mcp`
- **SSE:** `/sse`
- **Lista de ferramentas:** `/tools`

## Segurança

- ✅ Autenticação por API key
- ✅ Credenciais do Sienge em variáveis de ambiente
- ✅ Subdomínio correto: cctcontrol

## Limitações

- **Plano gratuito do Render:** Servidor hiberna após 15min de inatividade
- **Primeira requisição:** Pode levar até 30 segundos para "acordar"
- **Claude Web:** Pode limitar ferramentas exibidas por sessão

## Próximos Passos

1. Testar mais funcionalidades
2. Verificar se todas as 113 ferramentas são reconhecidas
3. Otimizar para limitar ferramentas por sessão se necessário

## Backup: Claude Desktop

Para uso completo com todas as 113 ferramentas sem limitações, continue usando o **Claude Desktop** local:
- Caminho: `%APPDATA%\Claude\claude_desktop_config.json`
- Já configurado e funcionando
