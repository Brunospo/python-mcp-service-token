from mcp.server.mcpserver import MCPServer

from api_mcp.application.customer_service import CustomerService
from api_mcp.domain.customer import Customer


def register_list_customers_tool(server: MCPServer, service: CustomerService):
    """Registra a ferramenta de listar clientes no servidor MCP."""

    @server.tool(name="list_customers", description="List all customers")
    async def list_customers() -> list[Customer]:
        """Array of all customers"""
        try:
            customers = await service.list_customers()

            return customers
        except Exception as error:
            raise RuntimeError(f"Failed to list customers. Error: {error}")
