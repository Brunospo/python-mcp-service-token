import pytest
from api_mcp.my_mcp.server import server
from mcp.client.client import Client


@pytest.fixture
async def mcp_session():

    async with Client(server) as client:
        yield client


@pytest.mark.anyio
async def testar_delete_customer_prompt(mcp_session):
    """Testar o prompt de deletar cliente"""
    result = await mcp_session.get_prompt(
        name="delete_customer_prompt",
        arguments={"customer_id": "123456"},
    )

    assert (
        result.messages[0].content.text
        == "Please delete the customer using the `delete_customer` tool with the following details:\n- Customer ID: 123456"
    )
