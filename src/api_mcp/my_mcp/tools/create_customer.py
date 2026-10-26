from mcp.server.mcpserver import MCPServer

from api_mcp.application.customer_service import CustomerService
from api_mcp.domain.customer import CreateCustomerResult, Customer


def register_create_customer_tool(server: MCPServer, service: CustomerService):
    @server.tool()
    async def create_customer(name: str, phone: str) -> CreateCustomerResult:
        """Create a new customer with the provided name and phone number.

        Args:
            name: The customer's full name.
            phone: The customer's contact phone number.
        """
        try:
            new_customer = Customer(name=name, phone=phone)
            new_customer_result = await service.create_customer(new_customer)
            return new_customer_result
        except Exception as error:
            raise RuntimeError(f"Failed to create customer: {error}")
