from mcp.server.mcpserver import MCPServer


def register_update_customer_prompt(server: MCPServer):
    @server.prompt(
        name="update_customer_prompt",
        description="Prompt to update an existing customer's name and phone number by their ID",
    )
    def update_customer_prompt(id: str, name: str, phone: str) -> str:
        return (
            f"Please update the customer using the `update_customer` tool with the following details:\n"
            f"- Customer ID: {id}\n"
            f"- New Name: {name}\n"
            f"- New Phone: {phone}"
        )
