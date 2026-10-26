import pytest
from api_mcp.my_mcp.server import server
from mcp.client.client import Client


@pytest.fixture
async def mcp_session():

    async with Client(server) as client:
        yield client


@pytest.mark.anyio
async def test_customers_resource(mcp_session):
    """Testar a listagem de resources no customers://api-info"""
    resource = await mcp_session.list_resources()
    assert resource.resources[0].uri == "customers://api-info"
