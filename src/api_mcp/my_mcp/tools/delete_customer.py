from mcp.server.mcpserver import MCPServer

from api_mcp.application.customer_service import CustomerService
from api_mcp.domain.customer import CreateCustomerResult


def register_delete_customer_tool(server: MCPServer, service: CustomerService):
    @server.tool()
    async def delete_customer(customer_id: str) -> CreateCustomerResult:
        """Delete an existing customer their ID.

        Args:
            customer_id: The unique identifier (_id) of the customer to be deleted.
        """
        try:
            deleted_customer_result = await service.delete_customer(customer_id)
            if deleted_customer_result is None:
                raise RuntimeError(f"Customer {customer_id} not found")
            return deleted_customer_result
        except Exception as error:
            raise RuntimeError(f"Failed to delete customer: {error}")
