"""Contas-Correntes (Checking Accounts) module for Sienge MCP"""
from typing import Optional
from mcp.server.fastmcp import FastMCP
from .client import SiengeClient


def register_checking_accounts_tools(mcp: FastMCP, client: SiengeClient):
    """Register checking accounts tools"""

    @mcp.tool()
    def get_checking_accounts(
        company_id: Optional[int] = None,
        account_number: Optional[str] = None,
        account_status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Busca contas-correntes.

        Args:
            company_id: Código da empresa (opcional)
            account_number: Número da conta-corrente (opcional)
            account_status: Status da conta (ENABLED, DISABLED, ALL)
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Lista de contas-correntes
        """
        params = {"limit": limit, "offset": offset}
        if company_id:
            params["companyId"] = company_id
        if account_number:
            params["accountNumber"] = account_number
        if account_status:
            params["accountStatus"] = account_status

        return client.get("/checking-accounts", params=params)
