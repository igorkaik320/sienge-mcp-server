"""Empresas (Companies) module for Sienge MCP"""
from typing import Optional
from mcp.server.fastmcp import FastMCP
from .client import SiengeClient


def register_company_tools(mcp: FastMCP, client: SiengeClient):
    """Register company-related tools"""

    @mcp.tool()
    def get_companies(
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Busca uma lista de empresas ordenadas pelo código ID.

        Args:
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Lista de empresas com metadados de paginação
        """
        params = {"limit": limit, "offset": offset}
        return client.get("/companies", params=params)

    @mcp.tool()
    def get_company(company_id: int) -> dict:
        """Busca uma empresa específica por ID.

        Args:
            company_id: Código da empresa

        Returns:
            Detalhes da empresa (id, name, tradeName, cnpj)
        """
        return client.get(f"/companies/{company_id}")
