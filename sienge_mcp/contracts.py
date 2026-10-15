"""Contratos de Suprimentos (Supply Contracts) module for Sienge MCP"""
from typing import Optional
from mcp.server.fastmcp import FastMCP
from .client import SiengeClient


def register_contract_tools(mcp: FastMCP, client: SiengeClient):
    """Register contract-related tools"""

    @mcp.tool()
    def get_supply_contract(
        document_id: int,
        contract_number: int,
    ) -> dict:
        """Consulta um contrato específico.

        Args:
            document_id: ID do documento
            contract_number: Número do contrato

        Returns:
            Dados do contrato
        """
        params = {"documentId": document_id, "contractNumber": contract_number}
        return client.get("/supply-contracts", params=params)

    @mcp.tool()
    def get_supply_contracts_all(
        contract_start_date: str,
        contract_end_date: str,
        company_id: Optional[int] = None,
        building_id: Optional[int] = None,
        limit: int = 100,
        offset: int = 0,
        status_approval: Optional[str] = None,
        authorization: Optional[str] = None,
        consistency: Optional[str] = None,
    ) -> dict:
        """Consulta lista de contratos com filtros.

        Args:
            contract_start_date: Data inicial do contrato (formato: yyyy-MM-dd)
            contract_end_date: Data final do contrato (formato: yyyy-MM-dd)
            company_id: Código da empresa (opcional)
            building_id: Código da obra (opcional)
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)
            status_approval: Código da situação de aprovação (opcional)
            authorization: Status de autorização (opcional)
            consistency: Status da situação de consistência (opcional)

        Returns:
            Lista paginada de contratos
        """
        params = {
            "contractStartDate": contract_start_date,
            "contractEndDate": contract_end_date,
            "limit": limit,
            "offset": offset,
        }
        if company_id:
            params["companyId"] = company_id
        if building_id:
            params["buildingId"] = building_id
        if status_approval:
            params["statusApproval"] = status_approval
        if authorization:
            params["authorization"] = authorization
        if consistency:
            params["consistency"] = consistency

        return client.get("/supply-contracts/all", params=params)

    @mcp.tool()
    def get_supply_contract_attachment(
        document_id: int,
        contract_number: int,
        attachment_number: int,
    ) -> dict:
        """Retorna o anexo do contrato.

        Args:
            document_id: ID do documento
            contract_number: Número do contrato
            attachment_number: Número do anexo

        Returns:
            Arquivo de anexo do contrato
        """
        params = {
            "documentId": document_id,
            "contractNumber": contract_number,
            "contractAttachmentNumber": attachment_number,
        }
        return client.get("/supply-contracts/attachments", params=params)

    @mcp.tool()
    def get_supply_contract_attachments_all(
        document_id: int,
        contract_number: int,
    ) -> dict:
        """Lista anexos do contrato.

        Args:
            document_id: ID do documento
            contract_number: Número do contrato

        Returns:
            Lista paginada de anexos do contrato
        """
        params = {"documentId": document_id, "contractNumber": contract_number}
        return client.get("/supply-contracts/attachments/all", params=params)

    @mcp.tool()
    def get_supply_contract_buildings(
        document_id: int,
        contract_number: int,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Consulta obras do contrato com unidades construtivas.

        Args:
            document_id: ID do documento
            contract_number: Número do contrato
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Lista de obras do contrato com unidades construtivas
        """
        params = {
            "documentId": document_id,
            "contractNumber": contract_number,
            "limit": limit,
            "offset": offset,
        }
        return client.get("/supply-contracts/buildings", params=params)

    @mcp.tool()
    def get_supply_contract_addenda(
        document_id: Optional[int] = None,
        contract_number: Optional[int] = None,
        building_id: Optional[int] = None,
        addendum_number: Optional[int] = None,
        addendum_start_date: Optional[str] = None,
        addendum_end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Consulta aditivos de obras do contrato.

        Args:
            document_id: ID do documento (opcional)
            contract_number: Número do contrato (opcional)
            building_id: Código da obra (opcional)
            addendum_number: Número do aditivo (opcional)
            addendum_start_date: Data inicial do aditivo (formato: yyyy-MM-dd)
            addendum_end_date: Data final do aditivo (formato: yyyy-MM-dd)
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Lista paginada de aditivos de obras do contrato
        """
        params = {"limit": limit, "offset": offset}
        if document_id:
            params["documentId"] = document_id
        if contract_number:
            params["contractNumber"] = contract_number
        if building_id:
            params["buildingId"] = building_id
        if addendum_number:
            params["addendumNumber"] = addendum_number
        if addendum_start_date:
            params["addendumStartDate"] = addendum_start_date
        if addendum_end_date:
            params["addendumEndDate"] = addendum_end_date

        return client.get("/supply-contracts/addenda", params=params)

    @mcp.tool()
    def get_addendum_items(
        document_id: int,
        contract_number: int,
        building_id: int,
        addendum_number: int,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Consulta itens de aditivo da obra do contrato.

        Args:
            document_id: ID do documento
            contract_number: Número do contrato
            building_id: Código da obra
            addendum_number: Número do aditivo
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Lista de itens do aditivo específico de uma obra do contrato
        """
        params = {
            "documentId": document_id,
            "contractNumber": contract_number,
            "buildingId": building_id,
            "addendumNumber": addendum_number,
            "limit": limit,
            "offset": offset,
        }
        return client.get("/supply-contracts/addenda/items", params=params)

    @mcp.tool()
    def authorize_supply_contract(
        document_id: int,
        contract_number: int,
        observation: Optional[dict] = None,
    ) -> dict:
        """Autoriza um contrato que está aguardando autorização.

        Args:
            document_id: ID do documento
            contract_number: Número do contrato
            observation: Observação relacionada à autorização (opcional)

        Returns:
            Confirmação da autorização
        """
        params = {"documentId": document_id, "contractNumber": contract_number}
        return client.patch("/supply-contracts/authorize", params=params, json=observation)

    @mcp.tool()
    def disapprove_supply_contract(
        document_id: int,
        contract_number: int,
        observation: Optional[dict] = None,
    ) -> dict:
        """Reprova um contrato que está aguardando autorização.

        Args:
            document_id: ID do documento
            contract_number: Número do contrato
            observation: Observação relacionada à reprovação (opcional)

        Returns:
            Confirmação da reprovação
        """
        params = {"documentId": document_id, "contractNumber": contract_number}
        return client.patch("/supply-contracts/disapprove", params=params, json=observation)
