"""Títulos do Contas a Pagar (Bills) module for Sienge MCP"""
from typing import Optional
from mcp.server.fastmcp import FastMCP
from .client import SiengeClient


def register_bill_tools(mcp: FastMCP, client: SiengeClient):
    """Register bill-related tools"""

    @mcp.tool()
    def get_bills(
        start_date: str,
        end_date: str,
        debtor_id: Optional[int] = None,
        creditor_id: Optional[int] = None,
        cost_center_id: Optional[int] = None,
        documents_identification_id: Optional[str] = None,
        document_number: Optional[str] = None,
        status: Optional[str] = None,
        origin_id: Optional[int] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Busca títulos no Sienge com filtros.

        Args:
            start_date: Data inicial de emissão (formato: yyyy-MM-dd)
            end_date: Data final de emissão (formato: yyyy-MM-dd)
            debtor_id: Código do devedor (opcional)
            creditor_id: Código do credor (opcional)
            cost_center_id: Código do centro de custo (opcional)
            documents_identification_id: Identificação do documento (opcional)
            document_number: Número do documento (opcional)
            status: Status do título (opcional)
            origin_id: ID da origem (opcional)
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Lista de títulos com metadados de paginação
        """
        params = {
            "startDate": start_date,
            "endDate": end_date,
            "limit": limit,
            "offset": offset,
        }
        if debtor_id:
            params["debtorId"] = debtor_id
        if creditor_id:
            params["creditorId"] = creditor_id
        if cost_center_id:
            params["costCenterId"] = cost_center_id
        if documents_identification_id:
            params["documentsIdentificationId"] = documents_identification_id
        if document_number:
            params["documentNumber"] = document_number
        if status:
            params["status"] = status
        if origin_id:
            params["originId"] = origin_id

        return client.get("/bills", params=params)

    @mcp.tool()
    def insert_bill(bill_data: dict) -> dict:
        """Insere um novo título no Sienge.

        Args:
            bill_data: Objeto para criação do título

        Returns:
            Confirmação da inserção
        """
        return client.post("/bills", json=bill_data)

    @mcp.tool()
    def get_bill(bill_id: int) -> dict:
        """Busca detalhes de um título específico.

        Args:
            bill_id: Número do título

        Returns:
            Detalhes do título
        """
        return client.get(f"/bills/{bill_id}")

    @mcp.tool()
    def update_bill(bill_id: int, bill_data: dict) -> dict:
        """Atualiza dados de um título existente.

        Args:
            bill_id: Número do título
            bill_data: Objeto para atualização do título

        Returns:
            Confirmação da atualização
        """
        return client.patch(f"/bills/{bill_id}", json=bill_data)

    @mcp.tool()
    def get_bills_by_change_date(
        start_date: str,
        end_date: str,
        debtor_id: Optional[int] = None,
        creditor_id: Optional[int] = None,
        cost_center_id: Optional[int] = None,
        documents_identification_id: Optional[str] = None,
        document_number: Optional[str] = None,
        status: Optional[str] = None,
        origin_id: Optional[int] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Busca títulos por data de alteração.

        Args:
            start_date: Data inicial de alteração (formato: yyyy-MM-dd)
            end_date: Data final de alteração (formato: yyyy-MM-dd)
            debtor_id: Código do devedor (opcional)
            creditor_id: Código do credor (opcional)
            cost_center_id: Código do centro de custo (opcional)
            documents_identification_id: Identificação do documento (opcional)
            document_number: Número do documento (opcional)
            status: Status do título (opcional)
            origin_id: ID da origem (opcional)
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Lista de títulos alterados no período
        """
        params = {
            "startDate": start_date,
            "endDate": end_date,
            "limit": limit,
            "offset": offset,
        }
        if debtor_id:
            params["debtorId"] = debtor_id
        if creditor_id:
            params["creditorId"] = creditor_id
        if cost_center_id:
            params["costCenterId"] = cost_center_id
        if documents_identification_id:
            params["documentsIdentificationId"] = documents_identification_id
        if document_number:
            params["documentNumber"] = document_number
        if status:
            params["status"] = status
        if origin_id:
            params["originId"] = origin_id

        return client.get("/bills/by-change-date", params=params)

    @mcp.tool()
    def insert_electronic_invoice_bill(invoice_data: dict) -> dict:
        """Insere título baseado em nota fiscal eletrônica.

        Args:
            invoice_data: Dados da nota fiscal eletrônica

        Returns:
            Confirmação da inserção
        """
        return client.post("/eletronic-invoice-bills", json=invoice_data)

    @mcp.tool()
    def get_bill_installments(
        bill_id: int,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Lista parcelas de um título específico.

        Args:
            bill_id: Número do título
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Lista de parcelas do título
        """
        params = {"limit": limit, "offset": offset}
        return client.get(f"/bills/{bill_id}/installments", params=params)

    @mcp.tool()
    def update_installments(bill_id: int, installments_data: dict) -> dict:
        """Atualiza parcelas do título em massa.

        Args:
            bill_id: Número do título
            installments_data: Objeto com campos para atualização das parcelas

        Returns:
            Confirmação da atualização
        """
        return client.patch(f"/bills/{bill_id}/installments", json=installments_data)

    @mcp.tool()
    def update_installment(bill_id: int, installment_id: int, installment_data: dict) -> dict:
        """Atualiza parcela específica do título.

        Args:
            bill_id: Número do título
            installment_id: Número da parcela
            installment_data: Objeto com campos para atualização da parcela

        Returns:
            Confirmação da atualização
        """
        return client.patch(f"/bills/{bill_id}/installments/{installment_id}", json=installment_data)

    @mcp.tool()
    def get_bank_transfer(bill_id: int, installment_id: int) -> dict:
        """Busca pagamento por transferência bancária.

        Args:
            bill_id: Número do título
            installment_id: Número da parcela

        Returns:
            Informações de transferência bancária
        """
        return client.get(f"/bills/{bill_id}/installments/{installment_id}/payment-information/bank-transfer")

    @mcp.tool()
    def insert_bank_transfer(bill_id: int, installment_id: int, transfer_data: dict) -> dict:
        """Insere pagamento por transferência bancária.

        Args:
            bill_id: Número do título
            installment_id: Número da parcela
            transfer_data: Dados da transferência bancária

        Returns:
            Confirmação da inserção
        """
        return client.patch(f"/bills/{bill_id}/installments/{installment_id}/payment-information/bank-transfer", json=transfer_data)

    @mcp.tool()
    def get_boleto_bancario(bill_id: int, installment_id: int) -> dict:
        """Busca pagamento por boleto bancário.

        Args:
            bill_id: Número do título
            installment_id: Número da parcela

        Returns:
            Informações de boleto bancário
        """
        return client.get(f"/bills/{bill_id}/installments/{installment_id}/payment-information/boleto-bancario")

    @mcp.tool()
    def insert_boleto_bancario(bill_id: int, installment_id: int, boleto_data: dict) -> dict:
        """Insere pagamento por boleto bancário.

        Args:
            bill_id: Número do título
            installment_id: Número da parcela
            boleto_data: Dados do boleto bancário

        Returns:
            Confirmação da inserção
        """
        return client.patch(f"/bills/{bill_id}/installments/{installment_id}/payment-information/boleto-bancario", json=boleto_data)

    @mcp.tool()
    def get_boleto_concessionaria(bill_id: int, installment_id: int) -> dict:
        """Busca pagamento por boleto concessionária.

        Args:
            bill_id: Número do título
            installment_id: Número da parcela

        Returns:
            Informações de boleto concessionária
        """
        return client.get(f"/bills/{bill_id}/installments/{installment_id}/payment-information/boleto-concessionaria")

    @mcp.tool()
    def insert_boleto_concessionaria(bill_id: int, installment_id: int, boleto_data: dict) -> dict:
        """Insere pagamento por boleto concessionária.

        Args:
            bill_id: Número do título
            installment_id: Número da parcela
            boleto_data: Dados do boleto concessionária

        Returns:
            Confirmação da inserção
        """
        return client.patch(f"/bills/{bill_id}/installments/{installment_id}/payment-information/boleto-concessionaria", json=boleto_data)

    @mcp.tool()
    def get_boleto_tax(bill_id: int, installment_id: int) -> dict:
        """Busca pagamento de tributos com código de barras.

        Args:
            bill_id: Número do título
            installment_id: Número da parcela

        Returns:
            Informações de tributos com código de barras
        """
        return client.get(f"/bills/{bill_id}/installments/{installment_id}/payment-information/boleto-tax")

    @mcp.tool()
    def insert_boleto_tax(bill_id: int, installment_id: int, boleto_data: dict) -> dict:
        """Insere pagamento de tributos com código de barras.

        Args:
            bill_id: Número do título
            installment_id: Número da parcela
            boleto_data: Dados do boleto de tributos

        Returns:
            Confirmação da inserção
        """
        return client.patch(f"/bills/{bill_id}/installments/{installment_id}/payment-information/boleto-tax", json=boleto_data)

    @mcp.tool()
    def get_dda(bill_id: int, installment_id: int) -> dict:
        """Busca pagamento por DDA.

        Args:
            bill_id: Número do título
            installment_id: Número da parcela

        Returns:
            Informações de DDA
        """
        return client.get(f"/bills/{bill_id}/installments/{installment_id}/payment-information/dda")

    @mcp.tool()
    def insert_dda(bill_id: int, installment_id: int, dda_data: dict) -> dict:
        """Insere pagamento por DDA.

        Args:
            bill_id: Número do título
            installment_id: Número da parcela
            dda_data: Dados do DDA

        Returns:
            Confirmação da inserção
        """
        return client.patch(f"/bills/{bill_id}/installments/{installment_id}/payment-information/dda", json=dda_data)
