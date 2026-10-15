# Guia de Hospedagem Online - Sienge API Server

Criei uma versão REST API do servidor que pode ser hospedada online! Esta versão usa FastAPI e pode ser implantada em vários serviços de nuvem.

## 🚀 Opções de Hospedagem

### Opção 1: Render (Mais Simples - Gratuito)

**Render** é uma plataforma gratuita e fácil de usar para hospedar APIs.

#### Passo a Passo:

1. **Crie uma conta no Render**: https://render.com

2. **Crie um repositório Git** com seu código (GitHub, GitLab, etc.)

3. **Suba seu código para o repositório**:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/seu-usuario/sienge-api.git
git push -u origin main
```

4. **No Render, crie um novo Web Service**:
   - Clique em "New" → "Web Service"
   - Conecte seu repositório
   - O Render detectará automaticamente o arquivo `render.yaml`
   - Configure as variáveis de ambiente:
     - `SIENGE_SUBDOMAIN`: ccontrol
     - `SIENGE_USERNAME`: cctcontrol-api
     - `SIENGE_PASSWORD`: QnMXmZbF24LWZujTrOJo6GVgAg3EPxeU

5. **Deploy!** O Render vai criar e deployar automaticamente

6. **Após o deploy**, você terá uma URL como: `https://sienge-api-server.onrender.com`

#### Usar a API:

```bash
# Listar empresas
curl https://sienge-api-server.onrender.com/api/companies

# Buscar credores
curl https://sienge-api-server.onrender.com/api/creditors

# Health check
curl https://sienge-api-server.onrender.com/health
```

---

### Opção 2: Railway (Alternativa Gratuita)

**Railway** é outra opção gratuita popular.

#### Passo a Passo:

1. **Crie uma conta no Railway**: https://railway.app

2. **Crie um novo projeto** e conecte seu repositório Git

3. **Adicione variáveis de ambiente**:
   - `SIENGE_SUBDOMAIN`: ccontrol
   - `SIENGE_USERNAME`: cctcontrol-api
   - `SIENGE_PASSWORD`: QnMXmZbF24LWZujTrOJo6GVgAg3EPxeU

4. **Deploy** e Railway vai criar a URL automaticamente

---

### Opção 3: VPS Próprio (DigitalOcean, AWS, etc.)

Se você quiser mais controle, pode usar um VPS.

#### Usando Docker:

1. **Copie o arquivo .env para o servidor**:
```bash
scp .env usuario@seu-servidor:/app/
```

2. **No servidor, execute**:
```bash
docker-compose up -d
```

3. **Configure um proxy reverso** (nginx) para HTTPS

---

## 🧪 Testar Localmente

Antes de hospedar online, você pode testar localmente:

### Iniciar o servidor:

```bash
cd C:\Users\USER\Documents\projet
venv\Scripts\python.exe -m sienge_mcp.api_server
```

Ou usando o comando instalado:
```bash
venv\Scripts\sienge-api
```

### Testar endpoints:

```bash
# Health check
curl http://localhost:8000/health

# Listar empresas
curl http://localhost:8000/api/companies

# Buscar credores
curl http://localhost:8000/api/creditors

# Listar contratos
curl "http://localhost:8000/api/supply-contracts/all?contract_start_date=2024-01-01&contract_end_date=2024-12-31"
```

### Documentação Interativa:

Abra no navegador: http://localhost:8000/docs

O FastAPI fornece uma documentação interativa automática (Swagger UI) onde você pode testar todos os endpoints!

---

## 📋 Endpoints Disponíveis

### Credores
- `GET /api/creditors` - Listar credores
- `GET /api/creditors/{id}` - Buscar credor
- `POST /api/creditors` - Criar credor
- `PATCH /api/creditors/{id}` - Atualizar credor
- `GET /api/creditors/{id}/bank-informations` - Listar informações bancárias
- `POST /api/creditors/{id}/bank-informations` - Criar informações bancárias
- `PATCH /api/creditors/{id}/bank-informations/{bank_id}` - Atualizar informações bancárias
- `GET /api/creditors/{id}/pix-informations` - Listar informações PIX
- `POST /api/creditors/{id}/pix-informations` - Criar informações PIX
- `PATCH /api/creditors/{id}/pix-informations/{pix_id}` - Atualizar informações PIX

### Empresas
- `GET /api/companies` - Listar empresas
- `GET /api/companies/{id}` - Buscar empresa

### Contratos
- `GET /api/supply-contracts` - Buscar contrato específico
- `GET /api/supply-contracts/all` - Listar contratos com filtros
- `GET /api/supply-contracts/attachments` - Buscar anexo
- `GET /api/supply-contracts/attachments/all` - Listar anexos
- `GET /api/supply-contracts/buildings` - Listar obras do contrato
- `PATCH /api/supply-contracts/authorize` - Autorizar contrato
- `PATCH /api/supply-contracts/disapprove` - Reprovar contrato

### Medições
- `GET /api/supply-contracts/measurements` - Buscar medição específica
- `GET /api/supply-contracts/measurements/all` - Listar medições
- `POST /api/supply-contracts/measurements` - Criar medição
- `PATCH /api/supply-contracts/measurements/authorize` - Autorizar medição

### Empreendimentos
- `GET /api/enterprises` - Listar empreendimentos
- `GET /api/enterprises/{id}` - Buscar empreendimento
- `GET /api/enterprises/{id}/groupings` - Buscar agrupamentos

### Health
- `GET /health` - Health check

---

## 🔒 Segurança

### Importante:

1. **Variáveis de ambiente**: Nunca commit credenciais no código. Use variáveis de ambiente na plataforma de hospedagem.

2. **HTTPS**: Em produção, sempre use HTTPS. Render e Railway fornecem HTTPS automático.

3. **Rate limiting**: Para produção, considere adicionar rate limiting para proteger sua API.

4. **Autenticação**: Se necessário, adicione autenticação (API keys, JWT, etc.) para proteger seus endpoints.

### Adicionar autenticação básica (opcional):

Se você quiser proteger sua API com autenticação, pode adicionar middleware no FastAPI. Me avise se precisar disso!

---

## 📦 Arquivos Adicionais Criados

- `sienge_mcp/api_server.py` - Servidor FastAPI REST
- `Dockerfile` - Configuração Docker
- `docker-compose.yml` - Configuração Docker Compose
- `render.yaml` - Configuração para Render

---

## 💡 Recursos Extras

### Documentação Automática

Ao iniciar o servidor, acesse:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### CORS

O servidor já está configurado com CORS habilitado para permitir chamadas de qualquer origem. Em produção, você pode restringir isso.

---

## 🎯 Recomendação

Para começar, recomendo usar **Render** por ser:
- Gratuito
- Fácil de configurar
- HTTPS automático
- Detecta automaticamente o arquivo `render.yaml`
- Bom para APIs REST

Após testar e validar, você pode migrar para serviços mais robustos se necessário.
