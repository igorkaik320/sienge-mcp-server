"""MCP HTTP Server for Sienge API integration"""
import os
import json
import logging
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel
import uvicorn
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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Sienge MCP HTTP Server",
    description="MCP Server via HTTP for Sienge API integration",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key for authentication
API_KEY = os.getenv("MCP_API_KEY", "your-secret-api-key-change-this")

# Initialize Sienge client
try:
    sienge_client = SiengeClient()
    logger.info("Sienge client initialized successfully")
except ValueError as e:
    logger.error(f"Failed to initialize Sienge client: {e}")
    sienge_client = None


def verify_api_key(api_key: Optional[str] = Header(None)) -> None:
    """Verify API key for authentication"""
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


# Tool registry
tools_registry: Dict[str, Any] = {}


def register_tool(name: str, func: Any, description: str, parameters: Dict[str, Any]):
    """Register a tool in the registry"""
    tools_registry[name] = {
        "name": name,
        "description": description,
        "inputSchema": parameters,
        "function": func
    }


# Register all tools
def register_all_tools():
    """Register all Sienge tools for MCP"""
    # We'll use a custom registration to extract tool info
    pass


# MCP Protocol Implementation
class MCPRequest(BaseModel):
    """MCP JSON-RPC request"""
    jsonrpc: str = "2.0"
    id: Optional[str] = None
    method: str
    params: Optional[Dict[str, Any]] = None


class MCPResponse(BaseModel):
    """MCP JSON-RPC response"""
    jsonrpc: str = "2.0"
    id: Optional[str] = None
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "sienge_client": "connected" if sienge_client else "disconnected"
    }


@app.post("/mcp")
async def mcp_endpoint(request: MCPRequest, x_api_key: Optional[str] = Header(None)):
    """Main MCP endpoint for JSON-RPC 2.0"""
    verify_api_key(x_api_key)
    
    if sienge_client is None:
        return MCPResponse(
            id=request.id,
            error={
                "code": -32603,
                "message": "Sienge client not initialized"
            }
        )
    
    try:
        if request.method == "initialize":
            # Initialize connection
            return MCPResponse(
                id=request.id,
                result={
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {
                            "listChanged": True
                        }
                    },
                    "serverInfo": {
                        "name": "sienge-mcp-server",
                        "version": "1.0.0"
                    }
                }
            )
        
        elif request.method == "tools/list":
            # List all available tools
            tools = []
            # Here we would dynamically list all tools from the registry
            # For now, returning a placeholder
            return MCPResponse(
                id=request.id,
                result={
                    "tools": [
                        {
                            "name": "get_bills",
                            "description": "Busca títulos no Sienge com filtros",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "start_date": {"type": "string"},
                                    "end_date": {"type": "string"}
                                },
                                "required": ["start_date", "end_date"]
                            }
                        }
                    ]
                }
            )
        
        elif request.method == "tools/call":
            # Call a specific tool
            tool_name = request.params.get("name") if request.params else None
            arguments = request.params.get("arguments", {}) if request.params else {}
            
            if not tool_name:
                return MCPResponse(
                    id=request.id,
                    error={
                        "code": -32602,
                        "message": "Tool name is required"
                    }
                )
            
            # Here we would call the actual tool function
            # For now, returning a placeholder
            return MCPResponse(
                id=request.id,
                result={
                    "content": [
                        {
                            "type": "text",
                            "text": f"Tool {tool_name} called with args: {arguments}"
                        }
                    ]
                }
            )
        
        else:
            return MCPResponse(
                id=request.id,
                error={
                    "code": -32601,
                    "message": f"Method not found: {request.method}"
                }
            )
    
    except Exception as e:
        logger.error(f"Error processing MCP request: {e}")
        return MCPResponse(
            id=request.id,
            error={
                "code": -32603,
                "message": str(e)
            }
        )


@app.get("/sse")
async def sse_endpoint(request: Request, x_api_key: Optional[str] = Header(None)):
    """SSE endpoint for streaming MCP messages"""
    verify_api_key(x_api_key)
    
    async def event_generator():
        """Generate SSE events"""
        try:
            # Send initialization message
            yield {
                "event": "message",
                "data": json.dumps({
                    "jsonrpc": "2.0",
                    "method": "notifications/initialized",
                    "params": {}
                })
            }
            
            # Keep connection alive
            while True:
                if await request.is_disconnected():
                    break
                yield {
                    "event": "ping",
                    "data": "keepalive"
                }
                await asyncio.sleep(30)
        
        except Exception as e:
            logger.error(f"SSE error: {e}")
    
    return EventSourceResponse(event_generator())


if __name__ == "__main__":
    import asyncio
    
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting MCP HTTP Server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
