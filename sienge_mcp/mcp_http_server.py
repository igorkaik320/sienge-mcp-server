"""MCP HTTP Server with full tool registration for Sienge API"""
import os
import json
import logging
import asyncio
import inspect
import hmac
import time
import functools
from typing import Any, Dict, List, Optional, Callable
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse
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
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("sienge_mcp")

# API Key for authentication
API_KEY = os.getenv("MCP_API_KEY", "your-secret-api-key-change-this")
READ_ONLY = os.getenv("READ_ONLY", "false").lower() == "true"


# Tool storage
class ToolStorage:
    """Storage for MCP tools"""
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}
    
    def add_tool(self, name: str, func: Callable, description: str, parameters: Dict[str, Any], is_write: bool = False):
        """Add a tool to storage"""
        self.tools[name] = {
            "name": name,
            "description": description,
            "inputSchema": parameters,
            "function": func,
            "is_write": is_write
        }
    
    def get_tool(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a tool by name"""
        return self.tools.get(name)
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List all tools"""
        return [
            {
                "name": tool["name"],
                "description": tool["description"],
                "inputSchema": tool["inputSchema"]
            }
            for tool in self.tools.values()
        ]


tool_storage = ToolStorage()


# Mock MCP class to collect tools
class MockMCP:
    """Mock MCP class to collect tool registrations"""
    def __init__(self):
        self.tools = []
    
    def tool(self, name: str = None):
        """Decorator to register tools"""
        def decorator(func):
            tool_name = name or func.__name__
            self.tools.append((tool_name, func))
            return func
        return decorator


# Extract parameters from function signature
def extract_parameters(func: Callable) -> Dict[str, Any]:
    """Extract JSON Schema parameters from function signature"""
    sig = inspect.signature(func)
    parameters = {
        "type": "object",
        "properties": {},
        "required": []
    }
    
    for param_name, param in sig.parameters.items():
        if param_name in ['self', 'mcp', 'client']:
            continue
        
        param_type = param.annotation if param.annotation != inspect.Parameter.empty else "string"
        default = param.default if param.default != inspect.Parameter.empty else None
        
        # Map Python types to JSON Schema types
        type_mapping = {
            str: "string",
            int: "integer",
            float: "number",
            bool: "boolean",
            list: "array",
            dict: "object"
        }
        
        json_type = type_mapping.get(param_type, "string")
        
        prop_def = {"type": json_type}
        
        if default is not None:
            prop_def["default"] = default
        else:
            parameters["required"].append(param_name)
        
        parameters["properties"][param_name] = prop_def
    
    return parameters


# Detect if function is a write operation
def is_write_operation(func_name: str) -> bool:
    """Detect if a function is a write operation based on name"""
    write_prefixes = ['insert', 'update', 'delete', 'remove', 'authorize', 'disapprove', 'patch', 'put', 'post']
    return any(func_name.startswith(prefix) for prefix in write_prefixes)


# Register all tools
def register_all_tools():
    """Register all Sienge tools from all modules"""
    mock_mcp = MockMCP()
    
    # Register tools from each module
    register_creditor_tools(mock_mcp, sienge_client)
    register_company_tools(mock_mcp, sienge_client)
    register_contract_tools(mock_mcp, sienge_client)
    register_measurement_tools(mock_mcp, sienge_client)
    register_enterprise_tools(mock_mcp, sienge_client)
    register_bill_tools(mock_mcp, sienge_client)
    register_accounts_receivable_tools(mock_mcp, sienge_client)
    register_payment_categories_tools(mock_mcp, sienge_client)
    register_checking_accounts_tools(mock_mcp, sienge_client)
    register_cost_centers_tools(mock_mcp, sienge_client)
    register_stock_inventories_tools(mock_mcp, sienge_client)
    register_purchase_invoices_tools(mock_mcp, sienge_client)
    register_purchase_quotations_tools(mock_mcp, sienge_client)
    register_purchase_requests_tools(mock_mcp, sienge_client)
    register_purchase_orders_tools(mock_mcp, sienge_client)
    
    # Extract tools from mock MCP
    for tool_name, func in mock_mcp.tools:
        is_write = is_write_operation(tool_name)
        
        # Skip write operations in READ_ONLY mode
        if READ_ONLY and is_write:
            logger.info(f"Skipping write tool in READ_ONLY mode: {tool_name}")
            continue
        
        description = func.__doc__ or f"Tool: {tool_name}"
        parameters = extract_parameters(func)
        tool_storage.add_tool(tool_name, func, description, parameters, is_write)
    
    logger.info(f"Registered {len(tool_storage.tools)} tools (READ_ONLY={READ_ONLY})")


# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan"""
    # Startup
    logger.info("Starting MCP HTTP Server")
    register_all_tools()
    logger.info(f"MCP HTTP Server ready with {len(tool_storage.tools)} tools")
    
    yield
    
    # Shutdown
    logger.info("Shutting down MCP HTTP Server")
    if sienge_client:
        sienge_client.close()


# Initialize FastAPI with lifespan
app = FastAPI(
    title="Sienge MCP HTTP Server",
    description="MCP Server via HTTP for Sienge API integration",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def verify_api_key(
    authorization: Optional[str] = Header(None),
    x_api_key: Optional[str] = Header(None),
    api_key_query: Optional[str] = None
) -> None:
    """Verify API key for authentication (accepts Bearer header, X-API-Key header, or query parameter)"""
    key = None
    
    # Try Authorization: Bearer <key>
    if authorization and authorization.startswith("Bearer "):
        key = authorization[7:]
    # Try X-API-Key header
    elif x_api_key:
        key = x_api_key
    # Try query parameter
    elif api_key_query:
        key = api_key_query
    
    if not key:
        raise HTTPException(status_code=401, detail="API key required")
    
    # Use constant-time comparison to prevent timing attacks
    if not hmac.compare_digest(key.encode(), API_KEY.encode()):
        raise HTTPException(status_code=401, detail="Invalid API key")


@app.get("/")
async def root():
    """Root endpoint with info"""
    return {
        "name": "Sienge MCP HTTP Server",
        "version": "1.0.0",
        "status": "healthy",
        "endpoints": {
            "health": "/health",
            "mcp": "/mcp",
            "sse": "/sse",
            "tools": "/tools"
        },
        "tools_count": len(tool_storage.tools),
        "read_only": READ_ONLY
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "sienge_client": "connected" if sienge_client else "disconnected",
        "tools_count": len(tool_storage.tools),
        "read_only": READ_ONLY
    }


@app.get("/tools")
async def list_tools_endpoint(
    authorization: Optional[str] = Header(None),
    x_api_key: Optional[str] = Header(None),
    api_key: Optional[str] = None
):
    """List all available tools"""
    verify_api_key(authorization, x_api_key, api_key)
    return {
        "tools": tool_storage.list_tools()
    }


@app.post("/mcp")
async def mcp_endpoint(
    request: Dict[str, Any],
    authorization: Optional[str] = Header(None),
    x_api_key: Optional[str] = Header(None),
    api_key: Optional[str] = None
):
    """Main MCP endpoint for JSON-RPC 2.0"""
    verify_api_key(authorization, x_api_key, api_key)
    
    jsonrpc = request.get("jsonrpc", "2.0")
    request_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})
    
    if sienge_client is None:
        return {
            "jsonrpc": jsonrpc,
            "id": request_id,
            "error": {
                "code": -32603,
                "message": "Sienge client not initialized"
            }
        }
    
    try:
        if method == "initialize":
            return {
                "jsonrpc": jsonrpc,
                "id": request_id,
                "result": {
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
            }
        
        elif method == "tools/list":
            return {
                "jsonrpc": jsonrpc,
                "id": request_id,
                "result": {
                    "tools": tool_storage.list_tools()
                }
            }
        
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if not tool_name:
                return {
                    "jsonrpc": jsonrpc,
                    "id": request_id,
                    "error": {
                        "code": -32602,
                        "message": "Tool name is required"
                    }
                }
            
            tool = tool_storage.get_tool(tool_name)
            if not tool:
                return {
                    "jsonrpc": jsonrpc,
                    "id": request_id,
                    "error": {
                        "code": -32602,
                        "message": f"Tool not found: {tool_name}"
                    }
                }
            
            # Check if write operation in READ_ONLY mode
            if READ_ONLY and tool.get("is_write", False):
                return {
                    "jsonrpc": jsonrpc,
                    "id": request_id,
                    "error": {
                        "code": -32603,
                        "message": f"Tool {tool_name} is blocked in READ_ONLY mode"
                    }
                }
            
            # Log tool call
            start = time.perf_counter()
            try:
                result = tool["function"](**arguments)
                duration_ms = (time.perf_counter() - start) * 1000
                # Sanitize arguments for logging
                safe_args = {k: "***" if any(x in k.lower() for x in ['password', 'senha', 'key']) else v for k, v in arguments.items()}
                logger.info("tool=%s ok ms=%d args=%s", tool_name, duration_ms, safe_args)
                
                return {
                    "jsonrpc": jsonrpc,
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, ensure_ascii=False, indent=2)
                            }
                        ]
                    }
                }
            except Exception as e:
                duration_ms = (time.perf_counter() - start) * 1000
                safe_args = {k: "***" if any(x in k.lower() for x in ['password', 'senha', 'key']) else v for k, v in arguments.items()}
                logger.exception("tool=%s error ms=%d args=%s", tool_name, duration_ms, safe_args)
                return {
                    "jsonrpc": jsonrpc,
                    "id": request_id,
                    "error": {
                        "code": -32603,
                        "message": f"Error calling tool: {str(e)}"
                    }
                }
        
        else:
            return {
                "jsonrpc": jsonrpc,
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }
    
    except Exception as e:
        logger.error(f"Error processing MCP request: {e}")
        return {
            "jsonrpc": jsonrpc,
            "id": request_id,
            "error": {
                "code": -32603,
                "message": str(e)
            }
        }


@app.get("/sse")
async def sse_endpoint(
    request: Request,
    authorization: Optional[str] = Header(None),
    x_api_key: Optional[str] = Header(None),
    api_key: Optional[str] = None
):
    """SSE endpoint for streaming MCP messages"""
    verify_api_key(authorization, x_api_key, api_key)
    
    async def event_generator():
        """Generate SSE events"""
        try:
            # Send initialized notification
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
    port = int(os.getenv("PORT", 10000))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting MCP HTTP Server on {host}:{port} (READ_ONLY={READ_ONLY})")
    uvicorn.run(app, host=host, port=port, access_log=False)
