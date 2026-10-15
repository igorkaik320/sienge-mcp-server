"""Main MCP Server for Sienge API integration"""
import sys
from mcp.server.fastmcp import FastMCP
from .client import SiengeClient
from .creditors import register_creditor_tools
from .companies import register_company_tools
from .contracts import register_contract_tools
from .measurements import register_measurement_tools
from .enterprises import register_enterprise_tools
from .bills import register_bill_tools
from .accounts_receivable import register_accounts_receivable_tools
from .payment_categories import register_payment_categories_tools
from .checking_accounts import register_checking_accounts_tools
from .cost_centers import register_cost_centers_tools
from .stock_inventories import register_stock_inventories_tools
from .purchase_invoices import register_purchase_invoices_tools
from .purchase_quotations import register_purchase_quotations_tools
from .purchase_requests import register_purchase_requests_tools
from .purchase_orders import register_purchase_orders_tools


def main():
    """Main entry point for the MCP server"""
    # Create MCP server
    mcp = FastMCP("Sienge MCP Server")

    # Initialize Sienge client
    try:
        client = SiengeClient()
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Register all module tools
    register_creditor_tools(mcp, client)
    register_company_tools(mcp, client)
    register_contract_tools(mcp, client)
    register_measurement_tools(mcp, client)
    register_enterprise_tools(mcp, client)
    register_bill_tools(mcp, client)
    register_accounts_receivable_tools(mcp, client)
    register_payment_categories_tools(mcp, client)
    register_checking_accounts_tools(mcp, client)
    register_cost_centers_tools(mcp, client)
    register_stock_inventories_tools(mcp, client)
    register_purchase_invoices_tools(mcp, client)
    register_purchase_quotations_tools(mcp, client)
    register_purchase_requests_tools(mcp, client)
    register_purchase_orders_tools(mcp, client)

    # Run the server
    mcp.run()


if __name__ == "__main__":
    main()
