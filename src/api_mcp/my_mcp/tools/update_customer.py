from mcp.server.mcpserver import MCPServer

from api_mcp.application.customer_service import CustomerService
from api_mcp.domain.customer import CreateCustomerResult, Customer


def register_update_customer_tool(server: MCPServer, service: CustomerService):
    @server.tool()
    async def update_customer(name: str, phone: str, id: str) -> CreateCustomerResult:
        """Update an existing customer's name and phone number by their ID.

        Args:
            name: The customer's full name.
            phone: The customer's contact phone number.
            id: The unique identifier (_id) of the customer to be updated.
        """
        try:
            new_customer = Customer(name=name, phone=phone, _id=id)
            new_customer_result = await service.update_customer(new_customer)
            if new_customer_result is None:
                raise RuntimeError(f"Customer {id} not found")
            return new_customer_result
        except Exception as error:
            raise RuntimeError(f"Failed to update customer: {error}")
