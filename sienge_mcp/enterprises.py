"""Empreendimentos (Enterprises) module for Sienge MCP"""
from typing import Optional
from mcp.server.fastmcp import FastMCP
from .client import SiengeClient


def register_enterprise_tools(mcp: FastMCP, client: SiengeClient):
    """Register enterprise-related tools"""

    @mcp.tool()
    def get_enterprises(
        company_id: Optional[int] = None,
        type: Optional[int] = None,
        limit: int = 100,
        offset: int = 0,
        receivable_register: Optional[str] = None,
        only_buildings_enabled_for_integration: bool = False,
    ) -> dict:
        """Busca uma lista de empreendimentos conforme filtros.

        Args:
            company_id: Código empresa do centro de custo (opcional)
            type: Tipo de empreendimento (1=Obra e Centro de custo, 2=Obra, 3=Centro de custo, 4=Centro de custo associado a obra)
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)
            receivable_register: Filtro de registro de recebíveis (B3 ou CERC)
            only_buildings_enabled_for_integration: Retornar apenas obras habilitadas para integração orçamentária

        Returns:
            Lista paginada de empreendimentos
        """
        params = {"limit": limit, "offset": offset}
        if company_id:
            params["companyId"] = company_id
        if type:
            params["type"] = type
        if receivable_register:
            params["receivableRegister"] = receivable_register
        if only_buildings_enabled_for_integration:
            params["onlyBuildingsEnabledForIntegration"] = only_buildings_enabled_for_integration

        return client.get("/enterprises", params=params)

    @mcp.tool()
    def get_enterprise(enterprise_id: int) -> dict:
        """Busca um empreendimento específico por ID.

        Args:
            enterprise_id: ID do empreendimento

        Returns:
            Detalhes completos do empreendimento
        """
        return client.get(f"/enterprises/{enterprise_id}")

    @mcp.tool()
    def get_enterprise_groupings(enterprise_id: int) -> dict:
        """Busca valores dos agrupamentos de unidades do empreendimento.

        Args:
            enterprise_id: ID do empreendimento

        Returns:
            Agrupamentos de unidades e seus valores associados
        """
        return client.get(f"/enterprises/{enterprise_id}/groupings")
