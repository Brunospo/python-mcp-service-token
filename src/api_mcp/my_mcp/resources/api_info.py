from mcp.server.mcpserver import MCPServer


def register_api_resource(server: MCPServer, base_url: str):

    @server.resource(
        uri="customers://api-info",
        description="describes the customers rest API that this MCP server wraps",
    )
    async def api_info() -> str:
        return f"""
Customers API

  Base URL : {base_url}
  Endpoints:
    GET    /customers         — list all customers
    GET    /customers/:id     — get customer by id
    POST   /customers         — create customer  {{ name, phone }}
    PUT    /customers/:id     — update customer  {{ name, phone }}
    DELETE /customers/:id     — delete customer

  Customer shape: {{ _id: string, name: string, phone: string }}
"""
