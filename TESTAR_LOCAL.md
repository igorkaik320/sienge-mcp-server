# Testar API Localmente

## Iniciar o Servidor

### Opção 1: Usando o módulo Python
```bash
cd C:\Users\USER\Documents\projet
venv\Scripts\python.exe -m sienge_mcp.api_server
```

### Opção 2: Usando o comando instalado
```bash
cd C:\Users\USER\Documents\projet
venv\Scripts\sienge-api
```

O servidor iniciará em: http://localhost:8000

## Testar Endpoints

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. Listar Empresas
```bash
curl http://localhost:8000/api/companies
```

### 3. Listar Credores
```bash
curl http://localhost:8000/api/creditors
```

### 4. Buscar Empresa Específica
```bash
curl http://localhost:8000/api/companies/1
```

### 5. Listar Contratos por Período
```bash
curl "http://localhost:8000/api/supply-contracts/all?contract_start_date=2024-01-01&contract_end_date=2024-12-31"
```

## Documentação Interativa

Abra no navegador:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Na documentação interativa, você pode:
- Ver todos os endpoints
- Testar cada endpoint diretamente no navegador
- Ver os parâmetros necessários
- Ver exemplos de requisições e respostas

## Parar o Servidor

Pressione `CTRL+C` no terminal onde o servidor está rodando.
