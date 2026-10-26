from mcp.server.mcpserver import MCPServer


def register_delete_customer_prompt(server: MCPServer):
    @server.prompt(
        name="delete_customer_prompt",
        description="Prompt to delete an existing customer by their ID",
    )
    def delete_customer_prompt(customer_id: str) -> str:
        return (
            f"Please delete the customer using the `delete_customer` tool with the following details:\n"
            f"- Customer ID: {customer_id}"
        )
