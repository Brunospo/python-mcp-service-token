import asyncio
import os
import sys

from api_mcp.my_mcp.server import server


async def main() -> None:
    service_token = os.getenv("SERVICE_TOKEN", "")

    if not service_token:
        print("[error]: SERVICE_TOKEN env var is required", file=sys.stderr)
        sys.exit(1)

    print("Customers MCP Server running on stdio", file=sys.stderr)

    server.run(transport="stdio")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as error:
        print(f"Fatal error in main(): {error}", file=sys.stderr)
        sys.exit(1)
