import pytest
from api_mcp.my_mcp.server import server
from mcp.client.client import Client


@pytest.fixture
async def mcp_session():

    async with Client(server) as client:
        yield client


@pytest.mark.anyio
async def testar_update_customer_prompt(mcp_session):
    """Testar o prompt de atualizar cliente"""
    result = await mcp_session.get_prompt(
        name="update_customer_prompt",
        arguments={"id": "123456", "name": "Wendel", "phone": "8888"},
    )

    assert (
        result.messages[0].content.text
        == "Please update the customer using the `update_customer` tool with the following details:\n- Customer ID: 123456\n- New Name: Wendel\n- New Phone: 8888"
    )
