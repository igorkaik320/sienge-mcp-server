"""Pedidos de Compra (Purchase Orders) module for Sienge MCP"""
from typing import Optional
from mcp.server.fastmcp import FastMCP
from .client import SiengeClient


def register_purchase_orders_tools(mcp: FastMCP, client: SiengeClient):
    """Register purchase orders tools"""

    @mcp.tool()
    def get_purchase_orders(
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
    ) -> dict:
        """Consulta pedidos de compra.

        Args:
            start_date: Data de início da busca (formato: yyyy-MM-dd)
            end_date: Data de fim da busca (formato: yyyy-MM-dd)
            status: Situação do pedido (PENDING, PARTIALLY_DELIVERED, FULLY_DELIVERED, CANCELED)
            authorized: Filtrar por autorização (true/false)
            supplier_id: ID do fornecedor
            building_id: Código da obra
            buyer_id: ID do comprador
            status_approval: Código da situação de aprovação
            consistency: Status da situação de consistência (IN_INCLUSION, CONSISTENT, INCONSISTENT)
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Lista de pedidos de compra
        """
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

    @mcp.tool()
    def get_purchase_order(purchase_order_id: int) -> dict:
        """Consulta pedido de compra específico.

        Args:
            purchase_order_id: ID do pedido de compra

        Returns:
            Detalhes do pedido de compra
        """
        return client.get(f"/purchase-orders/{purchase_order_id}")

    @mcp.tool()
    def get_purchase_order_items(
        purchase_order_id: int,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Consulta itens do pedido de compra.

        Args:
            purchase_order_id: ID do pedido de compra
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Lista de itens do pedido
        """
        params = {"limit": limit, "offset": offset}
        return client.get(f"/purchase-orders/{purchase_order_id}/items", params=params)

    @mcp.tool()
    def get_purchase_order_item(
        purchase_order_id: int,
        item_number: int,
    ) -> dict:
        """Consulta item específico do pedido de compra.

        Args:
            purchase_order_id: ID do pedido de compra
            item_number: Número do item

        Returns:
            Detalhes do item
        """
        return client.get(f"/purchase-orders/{purchase_order_id}/items/{item_number}")

    @mcp.tool()
    def get_purchase_order_item_purchase_requests(
        purchase_order_id: int,
        item_number: int,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Itens de Solicitação atendidas.

        Args:
            purchase_order_id: ID do pedido de compra
            item_number: Número do item
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Lista de solicitações de compra vinculadas ao item
        """
        params = {"limit": limit, "offset": offset}
        return client.get(f"/purchase-orders/{purchase_order_id}/items/{item_number}/purchase-requests", params=params)

    @mcp.tool()
    def get_purchase_order_item_delivery_schedules(
        purchase_order_id: int,
        item_number: int,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Consulta previsões de entregas do item do pedido.

        Args:
            purchase_order_id: ID do pedido de compra
            item_number: Número do item
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Lista de previsões de entrega
        """
        params = {"limit": limit, "offset": offset}
        return client.get(f"/purchase-orders/{purchase_order_id}/items/{item_number}/delivery-schedules", params=params)

    @mcp.tool()
    def get_purchase_order_item_building_appropriations(
        purchase_order_id: int,
        item_number: int,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Consulta apropriações de obra do item do pedido.

        Args:
            purchase_order_id: ID do pedido de compra
            item_number: Número do item
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Lista de apropriações de obra
        """
        params = {"limit": limit, "offset": offset}
        return client.get(f"/purchase-orders/{purchase_order_id}/items/{item_number}/buildings-appropriations", params=params)

    @mcp.tool()
    def get_purchase_order_totalization(
        purchase_order_id: int,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Consultar a totalização do pedido de compra.

        Args:
            purchase_order_id: ID do pedido de compra
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Totalização do pedido
        """
        params = {"limit": limit, "offset": offset}
        return client.get(f"/purchase-orders/{purchase_order_id}/totalization", params=params)

    @mcp.tool()
    def get_purchase_order_direct_billing(
        purchase_order_id: int,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Consultar o faturamento direto simples do pedido.

        Args:
            purchase_order_id: ID do pedido de compra
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Faturamento direto do pedido
        """
        params = {"limit": limit, "offset": offset}
        return client.get(f"/purchase-orders/{purchase_order_id}/direct-billing", params=params)

    @mcp.tool()
    def authorize_purchase_order(purchase_order_id: int, observation: Optional[dict] = None) -> dict:
        """Autoriza pedido de compra que está aguardando autorização.

        Args:
            purchase_order_id: ID do pedido de compra
            observation: Observação do pedido (opcional)

        Returns:
            Confirmação da autorização
        """
        if observation:
            return client.patch(f"/purchase-orders/{purchase_order_id}/authorize", json=observation)
        return client.client.put(f"/purchase-orders/{purchase_order_id}/authorize")

    @mcp.tool()
    def disapprove_purchase_order(purchase_order_id: int, observation: Optional[dict] = None) -> dict:
        """Reprova pedido de compra que está aguardando autorização.

        Args:
            purchase_order_id: ID do pedido de compra
            observation: Observação do pedido (opcional)

        Returns:
            Confirmação da reprovação
        """
        if observation:
            return client.patch(f"/purchase-orders/{purchase_order_id}/disapprove", json=observation)
        return client.client.put(f"/purchase-orders/{purchase_order_id}/disapprove")

    @mcp.tool()
    def get_purchase_order_attachments(
        purchase_order_id: int,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Retorna lista de anexos do pedido de compra.

        Args:
            purchase_order_id: ID do pedido de compra
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Lista de anexos
        """
        params = {"limit": limit, "offset": offset}
        return client.get(f"/purchase-orders/{purchase_order_id}/attachments", params=params)

    @mcp.tool()
    def get_purchase_order_attachment(purchase_order_id: int, attachment_number: int) -> dict:
        """Download de anexo do pedido de compra.

        Args:
            purchase_order_id: ID do pedido de compra
            attachment_number: Número do anexo

        Returns:
            Arquivo do anexo
        """
        return client.get(f"/purchase-orders/{purchase_order_id}/attachments/{attachment_number}")

    @mcp.tool()
    def get_supplier_evaluation_criteria(purchase_order_id: int) -> dict:
        """Lista de critérios de avaliação do fornecedor.

        Args:
            purchase_order_id: ID do pedido de compra

        Returns:
            Lista de critérios de avaliação
        """
        return client.get(f"/purchase-orders/{purchase_order_id}/supplier-evaluation-criteria")

    @mcp.tool()
    def post_purchase_order_evaluation(purchase_order_id: int, evaluation_data: dict) -> dict:
        """Cadastra uma avaliação do fornecedor no pedido.

        Args:
            purchase_order_id: ID do pedido de compra
            evaluation_data: Dados da avaliação

        Returns:
            Confirmação do cadastro
        """
        return client.post(f"/purchase-orders/{purchase_order_id}/evaluation", json=evaluation_data)

    @mcp.tool()
    def put_purchase_order_evaluation(purchase_order_id: int, evaluation_data: dict) -> dict:
        """Atualiza a avaliação do fornecedor no pedido.

        Args:
            purchase_order_id: ID do pedido de compra
            evaluation_data: Dados da avaliação

        Returns:
            Confirmação da atualização
        """
        return client.client.put(f"/purchase-orders/{purchase_order_id}/evaluation", json=evaluation_data)

    @mcp.tool()
    def get_purchase_order_analysis_pdf(
        purchase_order_id: int,
        print_purchase_order_authorization_observations_flag: bool = False,
        print_list_of_purchase_orders_with_same_appropriate_items: bool = False,
        print_only_purchase_invoices_with_outstanding_installments: bool = False,
        print_detailed_amounts_from_purchase_invoices: bool = False,
        print_appropriation_quantity: bool = False,
    ) -> dict:
        """Gera o relatório de Análise do Pedido de Compra em PDF.

        Args:
            purchase_order_id: ID do pedido de compra
            print_purchase_order_authorization_observations_flag: Imprimir observações de autorização
            print_list_of_purchase_orders_with_same_appropriate_items: Imprimir pedidos com mesmos itens
            print_only_purchase_invoices_with_outstanding_installments: Imprimir apenas NFs com parcelas em aberto
            print_detailed_amounts_from_purchase_invoices: Imprimir quantidades detalhadas das NFs
            print_appropriation_quantity: Imprimir quantidades de apropriações

        Returns:
            Arquivo PDF do relatório
        """
        params = {
            "printPurchaseOrderAuthorizationObservationsFlag": print_purchase_order_authorization_observations_flag,
            "printListOfPurchaseOrdersWithSameAppropriateItems": print_list_of_purchase_orders_with_same_appropriate_items,
            "printOnlyPurchaseInvoicesWithOutstandingInstallments": print_only_purchase_invoices_with_outstanding_installments,
            "printDetailedAmountsFromPurchaseInvoices": print_detailed_amounts_from_purchase_invoices,
            "printAppropriationQuantity": print_appropriation_quantity,
        }
        return client.get(f"/purchase-orders/{purchase_order_id}/analysis/pdf", params=params)
