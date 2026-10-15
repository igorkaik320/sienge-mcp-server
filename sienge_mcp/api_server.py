"""FastAPI REST API Server for Sienge integration"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from pydantic import BaseModel
from .client import SiengeClient
import os

app = FastAPI(
    title="Sienge API Server",
    description="REST API para integração com Sienge",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize client
client = SiengeClient()

# Pydantic models for request bodies
class ObservationDTO(BaseModel):
    """Model for observations"""
    text: Optional[str] = None

# ==================== BILLS (Títulos a Pagar) ====================

@app.get("/api/bills")
async def get_bills(
    start_date: str,
    end_date: str,
    debtor_id: Optional[int] = None,
    creditor_id: Optional[int] = None,
    cost_center_id: Optional[int] = None,
    documents_identification_id: Optional[str] = None,
    document_number: Optional[str] = None,
    status: Optional[str] = None,
    origin_id: Optional[int] = None,
    limit: int = 100,
    offset: int = 0,
):
    """Busca títulos no Sienge"""
    params = {
        "startDate": start_date,
        "endDate": end_date,
        "limit": limit,
        "offset": offset,
    }
    if debtor_id:
        params["debtorId"] = debtor_id
    if creditor_id:
        params["creditorId"] = creditor_id
    if cost_center_id:
        params["costCenterId"] = cost_center_id
    if documents_identification_id:
        params["documentsIdentificationId"] = documents_identification_id
    if document_number:
        params["documentNumber"] = document_number
    if status:
        params["status"] = status
    if origin_id:
        params["originId"] = origin_id
    return client.get("/bills", params=params)

@app.post("/api/bills")
async def insert_bill(bill_data: dict):
    """Insere um novo título"""
    return client.post("/bills", json=bill_data)

@app.get("/api/bills/{bill_id}")
async def get_bill(bill_id: int):
    """Busca detalhes de um título"""
    return client.get(f"/bills/{bill_id}")

@app.patch("/api/bills/{bill_id}")
async def update_bill(bill_id: int, bill_data: dict):
    """Atualiza um título"""
    return client.patch(f"/bills/{bill_id}", json=bill_data)

@app.get("/api/bills/by-change-date")
async def get_bills_by_change_date(
    start_date: str,
    end_date: str,
    debtor_id: Optional[int] = None,
    creditor_id: Optional[int] = None,
    cost_center_id: Optional[int] = None,
    documents_identification_id: Optional[str] = None,
    document_number: Optional[str] = None,
    status: Optional[str] = None,
    origin_id: Optional[int] = None,
    limit: int = 100,
    offset: int = 0,
):
    """Busca títulos por data de alteração"""
    params = {
        "startDate": start_date,
        "endDate": end_date,
        "limit": limit,
        "offset": offset,
    }
    if debtor_id:
        params["debtorId"] = debtor_id
    if creditor_id:
        params["creditorId"] = creditor_id
    if cost_center_id:
        params["costCenterId"] = cost_center_id
    if documents_identification_id:
        params["documentsIdentificationId"] = documents_identification_id
    if document_number:
        params["documentNumber"] = document_number
    if status:
        params["status"] = status
    if origin_id:
        params["originId"] = origin_id
    return client.get("/bills/by-change-date", params=params)

@app.get("/api/bills/{bill_id}/installments")
async def get_bill_installments(bill_id: int, limit: int = 100, offset: int = 0):
    """Lista parcelas de um título"""
    params = {"limit": limit, "offset": offset}
    return client.get(f"/bills/{bill_id}/installments", params=params)

# ==================== ACCOUNTS RECEIVABLE (Contas a Receber) ====================

@app.get("/api/accounts-receivable/receivable-bills")
async def find_receivable_bills(
    customer_id: int,
    company_id: Optional[int] = None,
    cost_center_id: Optional[int] = None,
    paid_off: bool = False,
    limit: int = 100,
    offset: int = 0,
):
    """Busca títulos a receber"""
    params = {
        "customerId": customer_id,
        "paidOff": paid_off,
        "limit": limit,
        "offset": offset,
    }
    if company_id:
        params["companyId"] = company_id
    if cost_center_id:
        params["costCenterId"] = cost_center_id
    return client.get("/accounts-receivable/receivable-bills", params=params)

@app.get("/api/accounts-receivable/receivable-bills/{receivable_bill_id}")
async def find_receivable_bill_by_id(receivable_bill_id: int):
    """Busca título a receber por ID"""
    return client.get(f"/accounts-receivable/receivable-bills/{receivable_bill_id}")

@app.get("/api/accounts-receivable/receivable-bills/{receivable_bill_id}/installments")
async def find_receivable_installments(
    receivable_bill_id: int,
    carrier_id_in: Optional[int] = None,
    limit: int = 100,
    offset: int = 0,
):
    """Busca parcelas do título"""
    params = {"limit": limit, "offset": offset}
    if carrier_id_in:
        params["carrierIdIn"] = carrier_id_in
    return client.get(f"/accounts-receivable/receivable-bills/{receivable_bill_id}/installments", params=params)

# ==================== PAYMENT CATEGORIES (Planos Financeiros) ====================

@app.get("/api/payment-categories")
async def get_all_payment_categories():
    """Busca todos os planos financeiros"""
    return client.get("/payment-categories")

@app.get("/api/payment-categories/{payment_categories_id}")
async def get_payment_category(payment_categories_id: int):
    """Busca plano financeiro por código"""
    return client.get(f"/payment-categories/{payment_categories_id}")

# ==================== CHECKING ACCOUNTS (Contas-Correntes) ====================

@app.get("/api/checking-accounts")
async def get_checking_accounts(
    company_id: Optional[int] = None,
    account_number: Optional[str] = None,
    account_status: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
):
    """Busca contas-correntes"""
    params = {"limit": limit, "offset": offset}
    if company_id:
        params["companyId"] = company_id
    if account_number:
        params["accountNumber"] = account_number
    if account_status:
        params["accountStatus"] = account_status
    return client.get("/checking-accounts", params=params)

# ==================== COST CENTERS (Centro de Custos) ====================

@app.get("/api/cost-centers")
async def get_all_cost_centers(limit: int = 100, offset: int = 0):
    """Busca todos os centros de custo"""
    params = {"limit": limit, "offset": offset}
    return client.get("/cost-centers", params=params)

@app.get("/api/cost-centers/{cost_center_id}")
async def get_cost_center(cost_center_id: int):
    """Busca centro de custo específico"""
    return client.get(f"/cost-centers/{cost_center_id}")

@app.get("/api/cost-centers/{cost_center_id}/available")
async def get_cost_center_available(cost_center_id: int):
    """Busca centro de custo com contas disponíveis"""
    return client.get(f"/cost-centers/{cost_center_id}/available")

# ==================== STOCK INVENTORIES (Estoque de Insumos) ====================

@app.get("/api/stock-inventories/{cost_center_id}/items")
async def get_stock_inventory_items(
    cost_center_id: int,
    limit: int = 100,
    offset: int = 0,
):
    """Retorna insumos no estoque"""
    params = {"limit": limit, "offset": offset}
    return client.get(f"/stock-inventories/{cost_center_id}/items", params=params)

# ==================== PURCHASE INVOICES (Nota Fiscal de Compra) ====================

@app.get("/api/purchase-invoices/{sequential_number}")
async def get_purchase_invoice(sequential_number: int):
    """Consulta nota fiscal de compra"""
    return client.get(f"/purchase-invoices/{sequential_number}")

@app.get("/api/purchase-invoices/{sequential_number}/items")
async def get_purchase_invoice_items(sequential_number: int):
    """Retorna itens da nota fiscal"""
    return client.get(f"/purchase-invoices/{sequential_number}/items")

# ==================== PURCHASE QUOTATIONS (Cotações de Preços) ====================

@app.post("/api/purchase-quotations")
async def post_purchase_quotation(quotation_data: dict):
    """Cria cotação de preço"""
    return client.post("/purchase-quotations", json=quotation_data)

@app.get("/api/purchase-quotations/all/negotiations")
async def get_purchase_quotations_negotiations(
    quotation_number: Optional[int] = None,
    supplier_id: Optional[int] = None,
    buyer_id: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
):
    """Lista cotações com negociações"""
    params = {"limit": limit, "offset": offset}
    if quotation_number:
        params["quotationNumber"] = quotation_number
    if supplier_id:
        params["supplierId"] = supplier_id
    if buyer_id:
        params["buyerId"] = buyer_id
    if start_date:
        params["startDate"] = start_date
    if end_date:
        params["endDate"] = end_date
    return client.get("/purchase-quotations/all/negotiations", params=params)

# ==================== PURCHASE REQUESTS (Solicitações de Compra) ====================

@app.get("/api/purchase-requests/{purchase_request_id}")
async def get_purchase_request(purchase_request_id: int):
    """Consulta solicitação de compra"""
    return client.get(f"/purchase-requests/{purchase_request_id}")

@app.patch("/api/purchase-requests/{purchase_request_id}/authorize")
async def authorize_purchase_request(purchase_request_id: int):
    """Autoriza solicitação de compra"""
    return client.patch(f"/purchase-requests/{purchase_request_id}/authorize")

@app.patch("/api/purchase-requests/{purchase_request_id}/disapproval")
async def disapprove_purchase_request(purchase_request_id: int):
    """Reprova solicitação de compra"""
    return client.patch(f"/purchase-requests/{purchase_request_id}/disapproval")

# ==================== PURCHASE ORDERS (Pedidos de Compra) ====================

@app.get("/api/purchase-orders")
async def get_purchase_orders(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    status: Optional[str] = None,
    authorized: Optional[bool] = None,
    supplier_id: Optional[int] = None,
    building_id: Optional[int] = None,
    buyer_id: Optional[str] = None,
    status_approval: Optional[str] = None,
    consistency: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
):
    """Consulta pedidos de compra"""
    params = {"limit": limit, "offset": offset}
    if start_date:
        params["startDate"] = start_date
    if end_date:
        params["endDate"] = end_date
    if status:
        params["status"] = status
    if authorized is not None:
        params["authorized"] = authorized
    if supplier_id:
        params["supplierId"] = supplier_id
    if building_id:
        params["buildingId"] = building_id
    if buyer_id:
        params["buyerId"] = buyer_id
    if status_approval:
        params["statusApproval"] = status_approval
    if consistency:
        params["consistency"] = consistency
    return client.get("/purchase-orders", params=params)

# ==================== HEALTH CHECK ====================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Sienge API Server",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
