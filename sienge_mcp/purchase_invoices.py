"""Nota Fiscal de Compra (Purchase Invoices) module for Sienge MCP"""
from typing import Optional
from mcp.server.fastmcp import FastMCP
from .client import SiengeClient


def register_purchase_invoices_tools(mcp: FastMCP, client: SiengeClient):
    """Register purchase invoices tools"""

    @mcp.tool()
    def get_purchase_invoice(sequential_number: int) -> dict:
        """Consulta nota fiscal de compra.

        Args:
            sequential_number: Número sequencial da nota fiscal

        Returns:
            Dados da nota fiscal de compra
        """
        return client.get(f"/purchase-invoices/{sequential_number}")

    @mcp.tool()
    def get_purchase_invoice_items(sequential_number: int) -> dict:
        """Retorna os itens da nota fiscal de compra.

        Args:
            sequential_number: Número sequencial da nota fiscal

        Returns:
            Lista de itens da nota fiscal
        """
        return client.get(f"/purchase-invoices/{sequential_number}/items")

    @mcp.tool()
    def get_purchase_invoice_item_appropriations(
        sequential_number: int,
        item_number: int,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Consulta apropriações de obra do item da nota fiscal.

        Args:
            sequential_number: Número sequencial da nota fiscal
            item_number: Número do item da nota fiscal
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Lista de apropriações de obra do item
        """
        params = {"limit": limit, "offset": offset}
        return client.get(f"/purchase-invoices/{sequential_number}/items/{item_number}/buildings-appropriations", params=params)

    @mcp.tool()
    def get_purchase_invoices(
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        company_id: Optional[int] = None,
        supplier_id: Optional[int] = None,
        document_id: Optional[str] = None,
        series: Optional[str] = None,
        number: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Lista notas fiscais de compra.

        Args:
            start_date: Data de início (formato: yyyy-MM-dd)
            end_date: Data de fim (formato: yyyy-MM-dd)
            company_id: Código da empresa
            supplier_id: Código do fornecedor
            document_id: ID do documento
            series: Série da nota fiscal
            number: Número da nota fiscal
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Lista paginada de notas fiscais de compra
        """
        params = {"limit": limit, "offset": offset}
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        if company_id:
            params["companyId"] = company_id
        if supplier_id:
            params["supplierId"] = supplier_id
        if document_id:
            params["documentId"] = document_id
        if series:
            params["series"] = series
        if number:
            params["number"] = number

        return client.get("/purchase-invoices", params=params)

    @mcp.tool()
    def post_purchase_invoice(invoice_data: dict) -> dict:
        """Cadastra uma nota fiscal de compra.

        Args:
            invoice_data: Dados da nota fiscal de compra a ser inserida

        Returns:
            Informações principais da nota fiscal inserida
        """
        return client.post("/purchase-invoices", json=invoice_data)

    @mcp.tool()
    def post_purchase_invoice_items_from_orders(sequential_number: int, items_data: dict) -> dict:
        """Insere itens em uma nota fiscal a partir de entregas de pedidos de compra.

        Args:
            sequential_number: Número sequencial da nota fiscal
            items_data: Dados dos itens da nota fiscal a serem inseridos

        Returns:
            Confirmação da inserção dos itens
        """
        return client.post(f"/purchase-invoices/{sequential_number}/items/purchase-orders/delivery-schedules", json=items_data)

    @mcp.tool()
    def get_purchase_invoices_deliveries_attended(
        bill_id: Optional[int] = None,
        sequential_number: Optional[int] = None,
        purchase_order_id: Optional[int] = None,
        invoice_item_number: Optional[int] = None,
        purchase_order_item_number: Optional[int] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Lista das entregas atendidas entre pedido de compra e nota fiscal.

        Args:
            bill_id: ID do título da nota fiscal
            sequential_number: Número sequencial da nota fiscal
            purchase_order_id: ID do pedido de compra
            invoice_item_number: Número do item da nota fiscal
            purchase_order_item_number: Número do item do pedido de compra
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Lista de entregas atendidas
        """
        params = {"limit": limit, "offset": offset}
        if bill_id:
            params["billId"] = bill_id
        if sequential_number:
            params["sequentialNumber"] = sequential_number
        if purchase_order_id:
            params["purchaseOrderId"] = purchase_order_id
        if invoice_item_number:
            params["invoiceItemNumber"] = invoice_item_number
        if purchase_order_item_number:
            params["purchaseOrderItemNumber"] = purchase_order_item_number

        return client.get("/purchase-invoices/deliveries-attended", params=params)
