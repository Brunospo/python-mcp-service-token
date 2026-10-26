import json

import pytest
from api_mcp.my_mcp.server import server
from mcp.client.client import Client


@pytest.fixture
async def mcp_session():

    async with Client(server) as client:
        yield client


@pytest.mark.anyio
async def test_list_all_customers(mcp_session):
    """Testar a tool de listar todos os clientes"""
    result = await mcp_session.call_tool("list_customers", arguments={})
    assert isinstance(result.content, list)


@pytest.mark.anyio
async def test_create_customer(mcp_session):
    """Testar a tool de cadastrar clientes"""
    result = await mcp_session.call_tool(
        "create_customer", arguments={"name": "Wendel", "phone": "999-000-777"}
    )

    response_data = json.loads(result.content[0].text)

    assert response_data["message"] == "user Wendel created!"


@pytest.mark.anyio
async def test_get_customer_by_name(mcp_session):
    """Testar a tool de obter cliente por nome"""

    result = await mcp_session.call_tool(
        "get_customer", arguments={"query": {"name": "Wen"}}
    )

    assert "_id" in result.structured_content["customer"]


@pytest.mark.anyio
async def test_get_customer_is_case_insensitive(mcp_session):
    """Testar a tool de obter cliente com nome em caixa diferente (case-insensitive)"""

    result = await mcp_session.call_tool(
        "get_customer", arguments={"query": {"name": "WENDEL"}}
    )

    assert "_id" in result.structured_content["customer"]


@pytest.mark.anyio
async def test_get_customer_ignores_empty_fields(mcp_session):
    """Testar a tool de obter cliente ignorando campos vazios"""

    result = await mcp_session.call_tool(
        "get_customer",
        arguments={"query": {"_id": "", "name": "wendel", "phone": ""}},
    )

    assert "_id" in result.structured_content["customer"]


@pytest.mark.anyio
async def test_update_customer(mcp_session):
    """Testar a tool de atualizar cliente"""

    create_result = await mcp_session.call_tool(
        "create_customer", arguments={"name": "Jhon", "phone": "977-000-727"}
    )

    customer_id = create_result.structured_content["id"]

    update_result = await mcp_session.call_tool(
        "update_customer",
        arguments={"name": "Brian", "phone": "40028922", "id": customer_id},
    )

    assert f"User {customer_id} updated!" == update_result.structured_content["message"]


@pytest.mark.anyio
async def test_delete_customer(mcp_session):
    """Testar a tool de deletar cliente"""

    create_result = await mcp_session.call_tool(
        "create_customer", arguments={"name": "Jhon", "phone": "977-000-727"}
    )

    customer_id = create_result.structured_content["id"]

    deleted_result = await mcp_session.call_tool(
        "delete_customer", arguments={"customer_id": customer_id}
    )

    assert (
        f"User {customer_id} deleted!" == deleted_result.structured_content["message"]
    )
