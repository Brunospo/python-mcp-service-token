# interfaces/mcp/get_customer_tool.py
from mcp.server.mcpserver import MCPServer

from api_mcp.application.customer_service import CustomerService
from api_mcp.domain.customer import Customer, CustomerQuery


def register_get_customer_tool(server: MCPServer, service: CustomerService) -> None:

    @server.tool(
        name="get_customer",
        description="Find a customer by _id, name, or phone number",
    )
    async def get_customer(query: CustomerQuery) -> dict[str, Customer | None]:
        try:
            customer = await service.find_customer(query)
            return {"customer": customer}
        except Exception as error:
            raise RuntimeError(f"Failed to get customer. Error: {error}") from error
