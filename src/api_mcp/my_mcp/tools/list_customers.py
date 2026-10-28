import json
from typing import Any

from mcp.server.mcpserver import MCPServer

from api_mcp.application.customer_service import CustomerService


def register_list_customers_tool(server: MCPServer, service: CustomerService):
    """Registra a ferramenta de listar clientes no servidor MCP."""

    @server.tool(name="list_customers", description="List all customers")
    async def list_customers() -> dict[str, Any]:
        """Array of all customers"""
        try:
            customers = await service.list_customers()

            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(customers, default=str, indent=2),
                    }
                ],
                "structured_content": {"customers": customers},
            }
        except Exception as error:
            message = f"Failed to list customers. Error: {error!s}"
            return {
                "content": [{"type": "text", "text": message}],
                "structured_content": {"isError": True, "message": message},
            }
