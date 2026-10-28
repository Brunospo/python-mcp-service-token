from typing import Any

from mcp.server.mcpserver import MCPServer

from api_mcp.application.customer_service import CustomerService


def register_delete_customer_tool(server: MCPServer, service: CustomerService):
    @server.tool()
    async def delete_customer(customer_id: str) -> dict[str, Any]:
        """Delete an existing customer their ID.

        Args:
            customer_id: The unique identifier (_id) of the customer to be deleted.
        """
        try:
            deleted_customer_result = await service.delete_customer(customer_id)
            message = getattr(deleted_customer_result, "message", None) or ""

            return {
                "content": [{"type": "text", "text": message}],
                "structured_content": deleted_customer_result,
            }
        except Exception as err:
            error_message = f"Failed to delete customer. Error: {err!s}"
            return {
                "content": [{"type": "text", "text": error_message}],
                "structured_content": {"isError": True, "message": error_message},
            }
