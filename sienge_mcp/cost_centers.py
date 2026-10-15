"""Centro de Custos (Cost Centers) module for Sienge MCP"""
from mcp.server.fastmcp import FastMCP
from .client import SiengeClient


def register_cost_centers_tools(mcp: FastMCP, client: SiengeClient):
    """Register cost centers tools"""

    @mcp.tool()
    def get_all_cost_centers(
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Busca todos os centros de custo.

        Args:
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Lista de centros de custo
        """
        params = {"limit": limit, "offset": offset}
        return client.get("/cost-centers", params=params)

    @mcp.tool()
    def get_cost_center(cost_center_id: int) -> dict:
        """Busca centro de custo específico.

        Args:
            cost_center_id: Código do centro de custo

        Returns:
            Detalhes do centro de custo
        """
        return client.get(f"/cost-centers/{cost_center_id}")

    @mcp.tool()
    def get_cost_center_available(cost_center_id: int) -> dict:
        """Busca centro de custo com contas correntes disponíveis.

        Args:
            cost_center_id: Código do centro de custo

        Returns:
            Centro de custo com contas disponíveis
        """
        return client.get(f"/cost-centers/{cost_center_id}/available")

    @mcp.tool()
    def get_immediate_register_settings(cost_center_id: int) -> dict:
        """Busca configurações de registro ATO no centro de custo.

        Args:
            cost_center_id: Código do centro de custo

        Returns:
            Configurações de registro ATO
        """
        params = {"costCenterId": cost_center_id}
        return client.get("/cost-centers/immediate-register-settings", params=params)
