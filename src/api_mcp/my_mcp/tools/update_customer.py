from typing import Any

from mcp.server.mcpserver import MCPServer

from api_mcp.application.customer_service import CustomerService
from api_mcp.domain.customer import Customer


def register_update_customer_tool(server: MCPServer, service: CustomerService):
    @server.tool()
    async def update_customer(name: str, phone: str, id: str) -> dict[str, Any]:
        """Update an existing customer's name and phone number by their ID.

        Args:
            name: The customer's full name.
            phone: The customer's contact phone number.
            id: The unique identifier (_id) of the customer to be updated.
        """
        try:
            new_customer = Customer(name=name, phone=phone, _id=id)
            new_customer_result = await service.update_customer(new_customer)
            message = getattr(new_customer_result, "message", None) or ""

            return {
                "content": [{"type": "text", "text": message}],
                "structured_content": new_customer_result,
            }
        except Exception as error:
            message = f"Failed to update customer. Error: {error!s}"
            return {
                "content": [{"type": "text", "text": message}],
                "structured_content": {"isError": True, "message": message},
            }
