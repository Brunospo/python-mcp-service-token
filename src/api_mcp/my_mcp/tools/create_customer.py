from typing import Any

from mcp.server.mcpserver import MCPServer

from api_mcp.application.customer_service import CustomerService
from api_mcp.domain.customer import Customer


def register_create_customer_tool(server: MCPServer, service: CustomerService):
    @server.tool(name="create_customer", description="Create a new customer")
    async def create_customer(name: str, phone: str) -> dict[str, Any]:
        """Create a new customer with the provided name and phone number.

        Args:
            name: The customer's full name.
            phone: The customer's contact phone number.
        """
        try:
            new_customer = Customer(name, phone)
            result = await service.create_customer(new_customer)

            message = getattr(result, "message", None) or ""

            return {
                "content": [{"type": "text", "text": message}],
                "structured_content": result,
            }
        except Exception as err:
            error_message = f"Failed to create customer. Error: {err!s}"
            return {
                "content": [{"type": "text", "text": error_message}],
                "structured_content": {"isError": True, "message": error_message},
            }
