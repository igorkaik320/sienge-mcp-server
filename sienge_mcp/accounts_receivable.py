"""Títulos do Contas a Receber (Accounts Receivable) module for Sienge MCP"""
from typing import Optional, List
from mcp.server.fastmcp import FastMCP
from .client import SiengeClient


def register_accounts_receivable_tools(mcp: FastMCP, client: SiengeClient):
    """Register accounts receivable tools"""

    @mcp.tool()
    def find_receivable_bills(
        customer_id: int,
        company_id: Optional[int] = None,
        cost_center_id: Optional[int] = None,
        paid_off: bool = False,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Busca títulos a receber do cliente.

        Args:
            customer_id: Código do cliente (obrigatório)
            company_id: Código da empresa (opcional)
            cost_center_id: Código do centro de custo (opcional)
            paid_off: Filtrar apenas títulos quitados (default: false)
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Lista de títulos a receber
        """
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

    @mcp.tool()
    def find_receivable_bill_by_id(receivable_bill_id: int) -> dict:
        """Busca título a receber pelo número.

        Args:
            receivable_bill_id: Número do título

        Returns:
            Detalhes do título a receber
        """
        return client.get(f"/accounts-receivable/receivable-bills/{receivable_bill_id}")

    @mcp.tool()
    def find_receivable_installments(
        receivable_bill_id: int,
        carrier_id_in: Optional[int] = None,
        carrier_id_not_in: Optional[List[int]] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Busca parcelas do título a receber.

        Args:
            receivable_bill_id: Número do título
            carrier_id_in: IDs dos portadores para incluir (opcional)
            carrier_id_not_in: IDs dos portadores para excluir (opcional)
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Lista de parcelas do título
        """
        params = {"limit": limit, "offset": offset}
        if carrier_id_in:
            params["carrierIdIn"] = carrier_id_in
        if carrier_id_not_in:
            params["carrierIdNotIn"] = carrier_id_not_in

        return client.get(f"/accounts-receivable/receivable-bills/{receivable_bill_id}/installments", params=params)

    @mcp.tool()
    def change_due_date(receivable_bill_id: int, installment_id: int, new_due_date: str) -> dict:
        """Altera vencimento da parcela e status da cobrança para Em Aberto.

        Args:
            receivable_bill_id: Número do título
            installment_id: Número da parcela
            new_due_date: Nova data de vencimento (formato: yyyy-MM-dd)

        Returns:
            Confirmação da alteração
        """
        data = {"newDueDate": new_due_date}
        return client.patch(f"/accounts-receivable/receivable-bills/{receivable_bill_id}/installments/{installment_id}/change-due-date", json=data)

    @mcp.tool()
    def get_receivable_budget_categories(
        receivable_bill_id: int,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Busca apropriações financeiras do título.

        Args:
            receivable_bill_id: Número do título
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Lista de apropriações financeiras
        """
        params = {"limit": limit, "offset": offset}
        return client.get(f"/accounts-receivable/{receivable_bill_id}/budget-categories", params=params)
