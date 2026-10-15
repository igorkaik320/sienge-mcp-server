"""Cotações de Preços (Purchase Quotations) module for Sienge MCP"""
from typing import Optional
from mcp.server.fastmcp import FastMCP
from .client import SiengeClient


def register_purchase_quotations_tools(mcp: FastMCP, client: SiengeClient):
    """Register purchase quotations tools"""

    @mcp.tool()
    def post_purchase_quotation(quotation_data: dict) -> dict:
        """Cria uma cotação de preço.

        Args:
            quotation_data: Dados da cotação de preço

        Returns:
            Confirmação da criação
        """
        return client.post("/purchase-quotations", json=quotation_data)

    @mcp.tool()
    def get_purchase_quotations_negotiations(
        quotation_number: Optional[int] = None,
        supplier_id: Optional[int] = None,
        buyer_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        authorized: Optional[bool] = None,
        status: Optional[str] = None,
        consistency: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Lista cotações com negociações.

        Args:
            quotation_number: Código da cotação (opcional)
            supplier_id: Código do fornecedor (opcional)
            buyer_id: Código do comprador (opcional)
            start_date: Data de início (formato: yyyy-MM-dd)
            end_date: Data de fim (formato: yyyy-MM-dd)
            authorized: Filtro para negociações autorizadas ou não
            status: Status da cotação (NEGOTIATION_IN_PROGRESS, NEGOTIATION_CLOSED, ACQUISITION_FORWARDED, SENT_FOR_SERVICE)
            consistency: Status da consistência (IN_INCLUSION, CONSISTENT, INCONSISTENT)
            limit: Quantidade máxima de resultados (default: 100, max: 200)
            offset: Deslocamento para paginação (default: 0)

        Returns:
            Lista de cotações com negociações
        """
        params = {"limit": limit, "offset": offset}
        if quotation_number:
            params["quotationNumber"] = quotation_number
        if supplier_id:
            params["supplierId"] = supplier_id
        if buyer_id:
            params["buyerId"] = buyer_id
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        if authorized is not None:
            params["authorized"] = authorized
        if status:
            params["status"] = status
        if consistency:
            params["consistency"] = consistency

        return client.get("/purchase-quotations/all/negotiations", params=params)

    @mcp.tool()
    def post_purchase_quotation_item(purchase_quotation_id: int, item_data: dict) -> dict:
        """Adiciona itens à cotação.

        Args:
            purchase_quotation_id: ID da cotação de preço
            item_data: Dados do item a ser adicionado

        Returns:
            Confirmação da criação do item
        """
        return client.post(f"/purchase-quotations/{purchase_quotation_id}/items", json=item_data)

    @mcp.tool()
    def post_purchase_quotation_item_from_request(purchase_quotation_id: int, request_data: dict) -> dict:
        """Adiciona itens de solicitação à cotação.

        Args:
            purchase_quotation_id: ID da cotação de preço
            request_data: Dados da entrega da solicitação de compra

        Returns:
            Confirmação da criação do item
        """
        return client.post(f"/purchase-quotations/{purchase_quotation_id}/items/from-purchase-request", json=request_data)

    @mcp.tool()
    def post_purchase_quotation_item_supplier(purchase_quotation_id: int, purchase_quotation_item_number: int, supplier_data: dict) -> dict:
        """Adiciona fornecedores ao item da cotação.

        Args:
            purchase_quotation_id: ID da cotação de preço
            purchase_quotation_item_number: Número do item da cotação
            supplier_data: Dados do fornecedor a ser incluído

        Returns:
            Confirmação da adição do fornecedor
        """
        return client.post(f"/purchase-quotations/{purchase_quotation_id}/items/{purchase_quotation_item_number}/suppliers", json=supplier_data)

    @mcp.tool()
    def post_purchase_quotation_negotiation(purchase_quotation_id: int, supplier_id: int) -> dict:
        """Cria negociação com fornecedor.

        Args:
            purchase_quotation_id: ID da cotação de preço
            supplier_id: ID do fornecedor

        Returns:
            Confirmação da criação da negociação
        """
        return client.post(f"/purchase-quotations/{purchase_quotation_id}/suppliers/{supplier_id}/negotiations")

    @mcp.tool()
    def authorize_purchase_quotation_negotiation(purchase_quotation_id: int, supplier_id: int) -> dict:
        """Autoriza última negociação de cotação para o fornecedor.

        Args:
            purchase_quotation_id: ID da cotação de preço
            supplier_id: ID do fornecedor

        Returns:
            Confirmação da autorização
        """
        return client.patch(f"/purchase-quotations/{purchase_quotation_id}/suppliers/{supplier_id}/negotiations/latest/authorize")

    @mcp.tool()
    def put_purchase_quotation_negotiation(purchase_quotation_id: int, supplier_id: int, negotiation_number: int, negotiation_data: dict) -> dict:
        """Atualiza uma negociação de cotação de um fornecedor.

        Args:
            purchase_quotation_id: ID da cotação de preço
            supplier_id: ID do fornecedor
            negotiation_number: Número da negociação
            negotiation_data: Dados da negociação a ser atualizada

        Returns:
            Confirmação da atualização
        """
        return client.client.put(f"/purchase-quotations/{purchase_quotation_id}/suppliers/{supplier_id}/negotiations/{negotiation_number}", json=negotiation_data)

    @mcp.tool()
    def put_purchase_quotation_negotiation_item(purchase_quotation_id: int, supplier_id: int, negotiation_number: int, quotation_item_number: int, item_data: dict) -> dict:
        """Atualiza item da negociação.

        Args:
            purchase_quotation_id: ID da cotação de preço
            supplier_id: ID do fornecedor
            negotiation_number: Número da negociação
            quotation_item_number: Número do item da cotação
            item_data: Dados do item a ser atualizado

        Returns:
            Confirmação da atualização
        """
        return client.client.put(f"/purchase-quotations/{purchase_quotation_id}/suppliers/{supplier_id}/negotiations/{negotiation_number}/items/{quotation_item_number}", json=item_data)

    @mcp.tool()
    def get_purchase_quotations_comparison_map_pdf(
        purchase_quotation_id: Optional[int] = None,
        supplier_id: Optional[int] = None,
        buyer_id: Optional[str] = None,
        building_id: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        short_print_flag: bool = False,
        print_general_data_flag: bool = True,
        print_number_requests_originated_quotations_flag: bool = False,
        highlight_highest_and_lowest_price_flag: bool = False,
        highlight_chosen_supplier_flag: bool = False,
        display_trading_authorization_history_flag: bool = False,
        display_supplier_group_per_page_flag: bool = False,
        print_quoted_price_flag: bool = False,
        print_internal_observation_flag: bool = False,
        show_the_best_and_last_price_considering_detail_and_brand_flag: bool = False,
    ) -> dict:
        """Gera relatório em PDF do mapa de cotações.

        Args:
            purchase_quotation_id: Código da cotação (opcional)
            supplier_id: Código do fornecedor (opcional)
            buyer_id: Código do comprador (opcional)
            building_id: Código da obra (opcional)
            start_date: Data de início (formato: yyyy-MM-dd)
            end_date: Data de fim (formato: yyyy-MM-dd)
            short_print_flag: Imprime relatório resumido
            print_general_data_flag: Imprime dados gerais
            print_number_requests_originated_quotations_flag: Imprime número das solicitações
            highlight_highest_and_lowest_price_flag: Destaca maior e menor preço
            highlight_chosen_supplier_flag: Destaca fornecedor escolhido
            display_trading_authorization_history_flag: Apresenta histórico de autorização
            display_supplier_group_per_page_flag: Apresenta bloco de fornecedores por página
            print_quoted_price_flag: Imprimir preço orçado
            print_internal_observation_flag: Imprimir observação interna
            show_the_best_and_last_price_considering_detail_and_brand_flag: Apresenta melhor e último preço

        Returns:
            URL do relatório PDF
        """
        params = {
            "shortPrintFlag": short_print_flag,
            "printGeneralDataFlag": print_general_data_flag,
            "printNumberRequestsOriginatedQuotationsFlag": print_number_requests_originated_quotations_flag,
            "highlightHighestAndLowestPriceFlag": highlight_highest_and_lowest_price_flag,
            "highlightChosenSupplierFlag": highlight_chosen_supplier_flag,
            "displayTradingAuthorizationHistoryFlag": display_trading_authorization_history_flag,
            "displaySupplierGroupPerPageFlag": display_supplier_group_per_page_flag,
            "printQuotedPriceFlag": print_quoted_price_flag,
            "printInternalObservationFlag": print_internal_observation_flag,
            "showTheBestAndLastPriceConsideringDetailAndBrandFlag": show_the_best_and_last_price_considering_detail_and_brand_flag,
        }
        if purchase_quotation_id:
            params["purchaseQuotationId"] = purchase_quotation_id
        if supplier_id:
            params["supplierId"] = supplier_id
        if buyer_id:
            params["buyerId"] = buyer_id
        if building_id:
            params["buildingId"] = building_id
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date

        return client.get("/purchase-quotations/comparison-map/pdf", params=params)
