import os

from mcp.server.mcpserver import MCPServer

from api_mcp.application.customer_service import CustomerService
from api_mcp.my_mcp.prompts.delete_customer import register_delete_customer_prompt
from api_mcp.my_mcp.prompts.find_customer import register_find_customer_prompt
from api_mcp.my_mcp.prompts.update_customer import register_update_customer_prompt
from api_mcp.my_mcp.resources.api_info import register_api_resource
from api_mcp.my_mcp.tools.create_customer import register_create_customer_tool
from api_mcp.my_mcp.tools.delete_customer import register_delete_customer_tool
from api_mcp.my_mcp.tools.get_customer import register_get_customer_tool
from api_mcp.my_mcp.tools.list_customers import register_list_customers_tool
from api_mcp.my_mcp.tools.update_customer import register_update_customer_tool

BASE_URL = "http://localhost:9999/v1"
SERVICE_TOKEN = os.getenv("SERVICE_TOKEN", "")

service = CustomerService(BASE_URL, SERVICE_TOKEN)

server = MCPServer("customers MCP", version="0.0.1")

register_list_customers_tool(server, service)
register_create_customer_tool(server, service)
register_get_customer_tool(server, service)
register_update_customer_tool(server, service)
register_delete_customer_tool(server, service)

register_find_customer_prompt(server)
register_update_customer_prompt(server)
register_delete_customer_prompt(server)

register_api_resource(server, BASE_URL)
