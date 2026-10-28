import json
from typing import Any

from mcp.server.mcpserver import MCPServer

from api_mcp.application.customer_service import CustomerService
from api_mcp.domain.customer import CustomerQuery


def register_get_customer_tool(server: MCPServer, service: CustomerService) -> None:

    @server.tool(
        name="get_customer",
        description="Find a customer by _id, name, or phone number",
    )
    async def get_customer(query: CustomerQuery) -> dict[str, Any | None]:
        """Find a customer by _id, name, or phone number.

        Args:
            query: Object containing search criteria (id, name, or phone)
        """
        try:
            customer = await service.find_customer(query)

            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(customer, default=str, indent=2),
                    }
                ],
                "structured_content": {"customer": customer},
            }
        except Exception as error:
            message = f"Failed to find customer. Error: {error!s}"
            return {
                "content": [{"type": "text", "text": message}],
                "structured_content": {"isError": True, "message": message},
            }
