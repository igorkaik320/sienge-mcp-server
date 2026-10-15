"""Estoque de Insumos (Stock Inventories) module for Sienge MCP"""
from typing import Optional
from mcp.server.fastmcp import FastMCP
from .client import SiengeClient


def register_stock_inventories_tools(mcp: FastMCP, client: SiengeClient):
    """Register stock inventories tools"""

    @mcp.tool()
    def get_stock_inventory_items(
        cost_center_id: int,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Retorna os insumos no estoque do centro de custo.

        Args:
            cost_center_id: Código do centro de custo
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Lista de insumos em estoque
        """
        params = {"limit": limit, "offset": offset}
        return client.get(f"/stock-inventories/{cost_center_id}/items", params=params)

    @mcp.tool()
    def get_stock_building_appropriation(
        cost_center_id: int,
        resource_id: int,
        detail_id: Optional[int] = None,
        trademark_id: Optional[int] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Busca apropriações de obra do insumo em estoque.

        Args:
            cost_center_id: Código do centro de custo
            resource_id: Código do insumo em estoque
            detail_id: Código do detalhe do insumo (opcional)
            trademark_id: Código da marca do insumo (opcional)
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Apropriações de obra do insumo
        """
        params = {"limit": limit, "offset": offset}
        if detail_id:
            params["detailId"] = detail_id
        if trademark_id:
            params["trademarkId"] = trademark_id

        return client.get(f"/stock-inventories/{cost_center_id}/items/{resource_id}/building-appropriation", params=params)

    @mcp.tool()
    def get_stock_reservations(
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Busca as reservas consistentes de forma paginada.

        Args:
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Lista de reservas de estoque
        """
        params = {"limit": limit, "offset": offset}
        return client.get("/stock-reservations", params=params)
