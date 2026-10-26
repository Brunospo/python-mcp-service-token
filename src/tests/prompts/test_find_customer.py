import pytest
from api_mcp.my_mcp.server import server
from mcp.client.client import Client


@pytest.fixture
async def mcp_session():

    async with Client(server) as client:
        yield client


@pytest.mark.anyio
async def testar_find_customer_prompt(mcp_session):
    """Testar o prompt de buscar cliente"""
    result = await mcp_session.get_prompt(
        name="find_customer_prompt",
        arguments={"name": "Wendel"},
    )

    assert (
        result.messages[0].content.text
        == """Please find the customer matching the following query using the get_customer or list_customers tool.\nQuery: {"name": "Wendel"}"""
    )


@pytest.mark.anyio
async def testar_find_customer_prompt_com_campos_vazios(mcp_session):
    """Campos vazios (_id/phone) devem ser ignorados ao montar o query do prompt"""

    result = await mcp_session.get_prompt(
        name="find_customer_prompt",
        arguments={"name": "wendel", "id": "", "phone": ""},
    )

    assert (
        result.messages[0].content.text
        == """Please find the customer matching the following query using the get_customer or list_customers tool.\nQuery: {"name": "wendel"}"""
    )
