"""Planos Financeiros (Payment Categories) module for Sienge MCP"""
from mcp.server.fastmcp import FastMCP
from .client import SiengeClient


def register_payment_categories_tools(mcp: FastMCP, client: SiengeClient):
    """Register payment categories tools"""

    @mcp.tool()
    def get_all_payment_categories() -> dict:
        """Busca todos os planos financeiros no Sienge.

        Returns:
            Lista completa de planos financeiros
        """
        return client.get("/payment-categories")

    @mcp.tool()
    def get_payment_category(payment_categories_id: int) -> dict:
        """Busca plano financeiro pelo código.

        Args:
            payment_categories_id: Código do plano financeiro (sem pontuação)

        Returns:
            Detalhes do plano financeiro
        """
        return client.get(f"/payment-categories/{payment_categories_id}")
