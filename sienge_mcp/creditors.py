"""Credores (Creditors) module for Sienge MCP"""
from typing import Optional, List
from mcp.server.fastmcp import FastMCP
from .client import SiengeClient


def register_creditor_tools(mcp: FastMCP, client: SiengeClient):
    """Register creditor-related tools"""

    @mcp.tool()
    def get_creditors(
        cpf: Optional[str] = None,
        cnpj: Optional[List[str]] = None,
        creditor: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Busca credores no Sienge.

        Args:
            cpf: CPF do credor sem máscara, somente números
            cnpj: Lista de CNPJs do credor sem máscara, somente números
            creditor: Nome do credor, nome fantasia ou código do credor
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Lista de credores encontrados com metadados de paginação
        """
        params = {"limit": limit, "offset": offset}
        if cpf:
            params["cpf"] = cpf
        if cnpj:
            params["cnpj"] = cnpj
        if creditor:
            params["creditor"] = creditor

        return client.get("/creditors", params=params)

    @mcp.tool()
    def get_creditor(creditor_id: int) -> dict:
        """Busca um credor específico por ID.

        Args:
            creditor_id: Código do credor

        Returns:
            Detalhes do credor
        """
        return client.get(f"/creditors/{creditor_id}")

    @mcp.tool()
    def insert_creditor(creditor_data: dict) -> dict:
        """Insere um novo credor no Sienge.

        Args:
            creditor_data: Objeto com dados do credor para criação

        Returns:
            Confirmação da inserção
        """
        return client.post("/creditors", json=creditor_data)

    @mcp.tool()
    def update_creditor(creditor_id: int, creditor_data: dict) -> dict:
        """Atualiza informações de um credor.

        Args:
            creditor_id: Código do credor a ser atualizado
            creditor_data: Objeto com dados para atualização (não precisa enviar todos os campos)

        Returns:
            Confirmação da atualização
        """
        return client.patch(f"/creditors/{creditor_id}", json=creditor_data)

    @mcp.tool()
    def get_bank_informations(
        creditor_id: int,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Busca as informações bancárias do credor.

        Args:
            creditor_id: Código do credor
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Lista de informações bancárias do credor
        """
        params = {"limit": limit, "offset": offset}
        return client.get(f"/creditors/{creditor_id}/bank-informations", params=params)

    @mcp.tool()
    def insert_bank_informations(creditor_id: int, bank_data: dict) -> dict:
        """Insere informações bancárias do credor.

        Args:
            creditor_id: Código do credor
            bank_data: Lista de objetos para criação das informações bancárias

        Returns:
            Confirmação da inserção
        """
        return client.post(f"/creditors/{creditor_id}/bank-informations", json=bank_data)

    @mcp.tool()
    def update_bank_informations(
        creditor_id: int,
        bank_information_id: int,
        bank_data: dict,
    ) -> dict:
        """Atualiza informações bancárias do credor.

        Args:
            creditor_id: Código do credor
            bank_information_id: Código da informação bancária
            bank_data: Objeto para alteração das informações bancárias

        Returns:
            Confirmação da atualização
        """
        return client.patch(
            f"/creditors/{creditor_id}/bank-informations/{bank_information_id}",
            json=bank_data,
        )

    @mcp.tool()
    def get_pix_informations(
        creditor_id: int,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Busca as informações de PIX do credor.

        Args:
            creditor_id: Código do credor
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Lista de informações PIX do credor
        """
        params = {"limit": limit, "offset": offset}
        return client.get(f"/creditors/{creditor_id}/pix-informations", params=params)

    @mcp.tool()
    def insert_pix_information(creditor_id: int, pix_data: dict) -> dict:
        """Insere informações de PIX do credor.

        Args:
            creditor_id: Código do credor
            pix_data: Objeto para criação de informação de PIX

        Returns:
            Confirmação da inserção
        """
        return client.post(f"/creditors/{creditor_id}/pix-informations", json=pix_data)

    @mcp.tool()
    def update_pix_information(
        creditor_id: int,
        pix_information_id: int,
        pix_data: dict,
    ) -> dict:
        """Atualiza informações de PIX do credor.

        Args:
            creditor_id: Código do credor
            pix_information_id: Código da informação de PIX
            pix_data: Objeto para alteração de informação de PIX

        Returns:
            Confirmação da atualização
        """
        return client.patch(
            f"/creditors/{creditor_id}/pix-informations/{pix_information_id}",
            json=pix_data,
        )

    @mcp.tool()
    def update_creditor_phone(
        creditor_id: int,
        phone_id: int,
        phone_data: dict,
    ) -> dict:
        """Atualiza informações de um telefone do credor.

        Args:
            creditor_id: Código do credor
            phone_id: Código do telefone
            phone_data: Objeto para atualização do telefone

        Returns:
            Confirmação da atualização
        """
        return client.patch(f"/creditors/{creditor_id}/phone/{phone_id}", json=phone_data)

    @mcp.tool()
    def update_creditor_contact(
        creditor_id: int,
        contact_id: int,
        contact_data: dict,
    ) -> dict:
        """Atualiza informações de um contato do credor.

        Args:
            creditor_id: Código do credor
            contact_id: Código do contato
            contact_data: Objeto para atualização do contato

        Returns:
            Confirmação da atualização
        """
        return client.patch(f"/creditors/{creditor_id}/contact/{contact_id}", json=contact_data)

    @mcp.tool()
    def update_creditor_procurator(
        creditor_id: int,
        procurator_id: int,
        procurator_data: dict,
    ) -> dict:
        """Atualiza informações de um procurador do credor.

        Args:
            creditor_id: Código do credor
            procurator_id: Código do procurador
            procurator_data: Objeto de atualização do procurador

        Returns:
            Confirmação da atualização
        """
        return client.patch(
            f"/creditors/{creditor_id}/procurator/{procurator_id}",
            json=procurator_data,
        )

    @mcp.tool()
    def update_creditor_agents(creditor_id: int, agents: List[dict]) -> dict:
        """Atualiza a lista de representantes do credor.

        Args:
            creditor_id: Código do credor
            agents: Lista completa de representantes (enviar todos ao atualizar)

        Returns:
            Confirmação da atualização
        """
        # Note: Sienge API uses PUT for this endpoint
        response = client.client.put(f"/creditors/{creditor_id}/agents", json=agents)
        response.raise_for_status()
        return {"status": "success"}
