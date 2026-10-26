import json

from mcp.server.mcpserver import MCPServer

from api_mcp.domain.customer import CustomerQuery


def register_find_customer_prompt(server: MCPServer):
    @server.prompt(
        name="find_customer_prompt",
        description="Prompt to search a customer using any combination of _id, name or phone",
    )
    def find_customer_prompt(
        name: str | None = None,
        phone: str | None = None,
        id: str | None = None,
    ) -> str:
        query = CustomerQuery(_id=id, name=name, phone=phone)
        query_json = json.dumps(query.to_dict())

        return f"Please find the customer matching the following query using the get_customer or list_customers tool.\nQuery: {query_json}"
