"""Solicitações de Compra (Purchase Requests) module for Sienge MCP"""
from typing import Optional
from mcp.server.fastmcp import FastMCP
from .client import SiengeClient


def register_purchase_requests_tools(mcp: FastMCP, client: SiengeClient):
    """Register purchase requests tools"""

    @mcp.tool()
    def get_purchase_request(purchase_request_id: int) -> dict:
        """Consulta solicitação de compra.

        Args:
            purchase_request_id: Código da solicitação de compra

        Returns:
            Dados da solicitação de compra
        """
        return client.get(f"/purchase-requests/{purchase_request_id}")

    @mcp.tool()
    def authorize_purchase_request(purchase_request_id: int) -> dict:
        """Autoriza todos os itens de uma solicitação.

        Args:
            purchase_request_id: Código da solicitação de compra

        Returns:
            Confirmação da autorização
        """
        return client.patch(f"/purchase-requests/{purchase_request_id}/authorize")

    @mcp.tool()
    def disapprove_purchase_request(purchase_request_id: int) -> dict:
        """Reprova todos os itens de uma solicitação.

        Args:
            purchase_request_id: Código da solicitação de compra

        Returns:
            Confirmação da reprovação
        """
        return client.patch(f"/purchase-requests/{purchase_request_id}/disapproval")

    @mcp.tool()
    def post_purchase_request(request_data: dict) -> dict:
        """Cria uma solicitação de compra para uma obra já existente.

        Args:
            request_data: Dados da solicitação de compra

        Returns:
            Confirmação da criação
        """
        return client.post("/purchase-requests", json=request_data)

    @mcp.tool()
    def get_purchase_request_items(
        purchase_request_id: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        building_id: Optional[int] = None,
        requester_user: Optional[str] = None,
        authorized: Optional[bool] = None,
        disapproved: Optional[bool] = None,
        purchase_request_consistency: Optional[str] = None,
        purchase_request_status: Optional[str] = None,
        with_open_quantity: Optional[bool] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Consulta itens de solicitação de compra.

        Args:
            purchase_request_id: ID da solicitação de compra
            start_date: Data de início (formato: yyyy-MM-dd)
            end_date: Data de fim (formato: yyyy-MM-dd)
            building_id: Código da obra
            requester_user: ID do solicitante
            authorized: Filtrar por autorização
            disapproved: Filtrar por reprovação
            purchase_request_consistency: Status da consistência (IN_INCLUSION, CONSISTENT, INCONSISTENT)
            purchase_request_status: Status da solicitação (PENDING, PARTIALLY_ATTENDED, FULLY_ATTENDED, CANCELED)
            with_open_quantity: Filtrar por saldo em aberto
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Lista de itens de solicitação de compra
        """
        params = {"limit": limit, "offset": offset}
        if purchase_request_id:
            params["purchaseRequestId"] = purchase_request_id
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        if building_id:
            params["buildingId"] = building_id
        if requester_user:
            params["requesterUser"] = requester_user
        if authorized is not None:
            params["authorized"] = authorized
        if disapproved is not None:
            params["disapproved"] = disapproved
        if purchase_request_consistency:
            params["purchaseRequestConsistency"] = purchase_request_consistency
        if purchase_request_status:
            params["purchaseRequestStatus"] = purchase_request_status
        if with_open_quantity is not None:
            params["withOpenQuantity"] = with_open_quantity

        return client.get("/purchase-requests/all/items", params=params)

    @mcp.tool()
    def get_purchase_request_item_appropriations(
        purchase_request_id: int,
        purchase_request_item_number: int,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Consulta apropriações de um item da solicitação.

        Args:
            purchase_request_id: ID da solicitação de compra
            purchase_request_item_number: Número do item
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Lista de apropriações do item
        """
        params = {"limit": limit, "offset": offset}
        return client.get(f"/purchase-requests/{purchase_request_id}/items/{purchase_request_item_number}/buildings-appropriations", params=params)

    @mcp.tool()
    def get_purchase_request_item_deliveries(
        purchase_request_id: int,
        purchase_request_item_number: int,
    ) -> dict:
        """Consulta entregas de um item da solicitação.

        Args:
            purchase_request_id: ID da solicitação de compra
            purchase_request_item_number: Número do item

        Returns:
            Lista de entregas do item
        """
        return client.get(f"/purchase-requests/{purchase_request_id}/items/{purchase_request_item_number}/delivery-requirements")

    @mcp.tool()
    def post_purchase_request_items(purchase_request_id: int, items_data: list) -> dict:
        """Cria itens para uma solicitação de compra existente.

        Args:
            purchase_request_id: ID da solicitação de compra
            items_data: Lista de itens a serem cadastrados

        Returns:
            Confirmação da criação dos itens
        """
        return client.post(f"/purchase-requests/{purchase_request_id}/items", json=items_data)

    @mcp.tool()
    def authorize_purchase_request_items(purchase_request_id: int, items_data: dict) -> dict:
        """Autoriza itens específicos de uma solicitação.

        Args:
            purchase_request_id: ID da solicitação de compra
            items_data: Lista de itens para autorização

        Returns:
            Confirmação da autorização
        """
        return client.patch(f"/purchase-requests/{purchase_request_id}/items/authorize", json=items_data)

    @mcp.tool()
    def authorize_purchase_request_item(purchase_request_id: int, purchase_request_item_number: int) -> dict:
        """Autoriza um item específico de uma solicitação.

        Args:
            purchase_request_id: ID da solicitação de compra
            purchase_request_item_number: Número do item

        Returns:
            Confirmação da autorização
        """
        return client.patch(f"/purchase-requests/{purchase_request_id}/items/{purchase_request_item_number}/authorize")
