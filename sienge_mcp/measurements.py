"""Medições de Contratos de Suprimentos (Measurements) module for Sienge MCP"""
from typing import Optional
from mcp.server.fastmcp import FastMCP
from .client import SiengeClient


def register_measurement_tools(mcp: FastMCP, client: SiengeClient):
    """Register measurement-related tools"""

    @mcp.tool()
    def get_measurement(
        document_id: int,
        contract_number: int,
        building_id: int,
        measurement_number: int,
    ) -> dict:
        """Consulta uma medição específica.

        Args:
            document_id: ID do documento
            contract_number: Número do contrato
            building_id: Código da obra
            measurement_number: Número da medição

        Returns:
            Dados da medição
        """
        params = {
            "documentId": document_id,
            "contractNumber": contract_number,
            "buildingId": building_id,
            "measurementNumber": measurement_number,
        }
        return client.get("/supply-contracts/measurements", params=params)

    @mcp.tool()
    def list_measurements(
        document_id: Optional[int] = None,
        contract_number: Optional[int] = None,
        building_id: Optional[int] = None,
        measurement_number: Optional[int] = None,
        contract_supplier_id: Optional[int] = None,
        contract_customer_id: Optional[int] = None,
        measurement_date: Optional[str] = None,
        measurement_start_date: Optional[str] = None,
        measurement_end_date: Optional[str] = None,
        status_approval: Optional[str] = None,
        authorization: Optional[str] = None,
        consistency: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Lista medições de contratos conforme filtros.

        Args:
            document_id: ID do documento (opcional)
            contract_number: Número do contrato (opcional)
            building_id: Código da obra (opcional)
            measurement_number: Número da medição (opcional)
            contract_supplier_id: ID do fornecedor do contrato (opcional)
            contract_customer_id: ID do cliente do contrato (opcional)
            measurement_date: Data da medição (formato: yyyy-MM-dd)
            measurement_start_date: Data inicial da medição (formato: yyyy-MM-dd)
            measurement_end_date: Data final da medição (formato: yyyy-MM-dd)
            status_approval: Código da situação de aprovação (D=Disapproved, A=Approved)
            authorization: Status de autorização (T=Todos, S=Reprovados, A=Aprovados, N=Aguardando)
            consistency: Status da situação de consistência (T=Todos, S=Consistente, N=Inconsistente, I=Inclusão)
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Lista paginada de medições
        """
        params = {"limit": limit, "offset": offset}
        if document_id:
            params["documentId"] = document_id
        if contract_number:
            params["contractNumber"] = contract_number
        if building_id:
            params["buildingId"] = building_id
        if measurement_number:
            params["measurementNumber"] = measurement_number
        if contract_supplier_id:
            params["contractSupplierId"] = contract_supplier_id
        if contract_customer_id:
            params["contractCustomerId"] = contract_customer_id
        if measurement_date:
            params["measurementDate"] = measurement_date
        if measurement_start_date:
            params["measurementStartDate"] = measurement_start_date
        if measurement_end_date:
            params["measurementEndDate"] = measurement_end_date
        if status_approval:
            params["statusApproval"] = status_approval
        if authorization:
            params["authorization"] = authorization
        if consistency:
            params["consistency"] = consistency

        return client.get("/supply-contracts/measurements/all", params=params)

    @mcp.tool()
    def post_measurement(
        document_id: int,
        contract_number: int,
        building_id: int,
        measurement_data: dict,
    ) -> dict:
        """Cria uma nova medição para o contrato e obra informados.

        Args:
            document_id: ID do documento
            contract_number: Número do contrato
            building_id: Código da obra
            measurement_data: Informações da medição a ser cadastrada

        Returns:
            Confirmação da criação da medição
        """
        params = {
            "documentId": document_id,
            "contractNumber": contract_number,
            "buildingId": building_id,
        }
        return client.post("/supply-contracts/measurements", params=params, json=measurement_data)

    @mcp.tool()
    def get_measurement_attachment(
        document_id: int,
        contract_number: int,
        building_id: int,
        measurement_number: int,
        attachment_number: int,
    ) -> dict:
        """Download de anexo de medição de contrato.

        Args:
            document_id: ID do documento
            contract_number: Número do contrato
            building_id: Código da obra
            measurement_number: Número da medição
            attachment_number: Número do anexo

        Returns:
            Arquivo de anexo da medição
        """
        params = {
            "documentId": document_id,
            "contractNumber": contract_number,
            "buildingId": building_id,
            "measurementNumber": measurement_number,
            "attachmentNumber": attachment_number,
        }
        return client.get("/supply-contracts/measurements/attachments", params=params)

    @mcp.tool()
    def list_measurement_attachments(
        measurement_start_date: str,
        measurement_end_date: str,
        document_id: Optional[int] = None,
        contract_number: Optional[int] = None,
        building_id: Optional[int] = None,
        measurement_number: Optional[int] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Lista anexos de medições de contrato conforme período.

        Args:
            measurement_start_date: Data inicial (formato: yyyy-MM-dd)
            measurement_end_date: Data final (formato: yyyy-MM-dd)
            document_id: ID do documento (opcional)
            contract_number: Número do contrato (opcional)
            building_id: Código da obra (opcional)
            measurement_number: Número da medição (opcional)
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Lista paginada de anexos de medições
        """
        params = {
            "measurementStartDate": measurement_start_date,
            "measurementEndDate": measurement_end_date,
            "limit": limit,
            "offset": offset,
        }
        if document_id:
            params["documentId"] = document_id
        if contract_number:
            params["contractNumber"] = contract_number
        if building_id:
            params["buildingId"] = building_id
        if measurement_number:
            params["measurementNumber"] = measurement_number

        return client.get("/supply-contracts/measurements/attachments/all", params=params)

    @mcp.tool()
    def authorize_measurement(
        document_id: int,
        contract_number: int,
        building_id: int,
        measurement_number: int,
        observation: Optional[dict] = None,
    ) -> dict:
        """Autoriza uma medição que está aguardando autorização.

        Args:
            document_id: ID do documento
            contract_number: Número do contrato
            building_id: Código da obra
            measurement_number: Número da medição
            observation: Observação sobre a autorização (opcional)

        Returns:
            Confirmação da autorização
        """
        params = {
            "documentId": document_id,
            "contractNumber": contract_number,
            "buildingId": building_id,
            "measurementNumber": measurement_number,
        }
        return client.patch("/supply-contracts/measurements/authorize", params=params, json=observation)

    @mcp.tool()
    def get_measurement_clearing(
        document_id: int,
        contract_number: int,
        building_id: int,
        measurement_number: int,
    ) -> dict:
        """Retorna a liberação de uma medição.

        Args:
            document_id: ID do documento
            contract_number: Número do contrato
            building_id: Código da obra
            measurement_number: Número da medição

        Returns:
            Informações de liberação da medição
        """
        params = {
            "documentId": document_id,
            "contractNumber": contract_number,
            "buildingId": building_id,
            "measurementNumber": measurement_number,
        }
        return client.get("/supply-contracts/measurements/clearing", params=params)
