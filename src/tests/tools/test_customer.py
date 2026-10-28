import json
import os
import sys

import httpx2
import pytest
from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client
from rich import print

API_URL = os.getenv("CUSTOMERS_API_URL", "http://localhost:9999/v1")


@pytest.fixture
async def service_token():
    """Fixture assíncrona que busca o token de serviço antes dos testes."""
    async with httpx2.AsyncClient() as client:
        response = await client.post(
            f"{API_URL}/auth/service-token",
            json={
                "username": "erickwendel",
                "password": "123123",
                "adminSuperSecret": "AM I THE BOSS?",
            },
            headers={"Content-Type": "application/json"},
        )

        if not response.is_success:
            raise RuntimeError(f"Failed to get service token: {response.status_code}")

        data = response.json()
        return data["serviceToken"]


@pytest.fixture
async def mcp_session(service_token):
    env = {**os.environ, "SERVICE_TOKEN": service_token}

    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "api_mcp.main"],
        env=env,
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield session


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

    assert response_data["structured_content"]["message"] == "user Wendel created!"


@pytest.mark.anyio
async def test_get_customer_by_name(mcp_session):
    """Testar a tool de obter cliente por nome"""

    result = await mcp_session.call_tool(
        "get_customer", arguments={"query": {"name": "Wen"}}
    )

    assert "_id" in result.structured_content["structured_content"]["customer"]


@pytest.mark.anyio
async def test_get_customer_is_case_insensitive(mcp_session):
    """Testar a tool de obter cliente com nome em caixa diferente (case-insensitive)"""

    result = await mcp_session.call_tool(
        "get_customer", arguments={"query": {"name": "WENDEL"}}
    )

    assert "_id" in result.structured_content["structured_content"]["customer"]


@pytest.mark.anyio
async def test_get_customer_ignores_empty_fields(mcp_session):
    """Testar a tool de obter cliente ignorando campos vazios"""

    result = await mcp_session.call_tool(
        "get_customer",
        arguments={"query": {"_id": "", "name": "wendel", "phone": ""}},
    )

    assert "_id" in result.structured_content["structured_content"]["customer"]


@pytest.mark.anyio
async def test_update_customer(mcp_session):
    """Testar a tool de atualizar cliente"""

    create_result = await mcp_session.call_tool(
        "create_customer", arguments={"name": "Jhon", "phone": "977-000-727"}
    )

    customer_id = create_result.structured_content["structured_content"]["id"]

    update_result = await mcp_session.call_tool(
        "update_customer",
        arguments={"name": "Brian", "phone": "40028922", "id": customer_id},
    )

    assert (
        f"User {customer_id} updated!"
        == update_result.structured_content["structured_content"]["message"]
    )


@pytest.mark.anyio
async def test_delete_customer(mcp_session):
    """Testar a tool de deletar cliente"""

    create_result = await mcp_session.call_tool(
        "create_customer", arguments={"name": "Jhon", "phone": "977-000-727"}
    )

    customer_id = create_result.structured_content["structured_content"]["id"]

    deleted_result = await mcp_session.call_tool(
        "delete_customer", arguments={"customer_id": customer_id}
    )

    assert (
        f"User {customer_id} deleted!"
        == deleted_result.structured_content["structured_content"]["message"]
    )


@pytest.mark.anyio
async def test_rate_limit(mcp_session):
    """Testar se o rate limit é atingido e tratado corretamente após várias requisições."""

    rate_limit_alcancado = False
    total_requisicoes = 0
    max_tentativas = 100

    for _ in range(max_tentativas):
        total_requisicoes += 1
        list_result = await mcp_session.call_tool("list_customers", arguments={})

        # Acessa com segurança o isError no dicionário aninhado
        sc = list_result.structured_content or {}
        inner_sc = sc.get("structured_content", {})
        is_error = inner_sc.get("isError", False)

        if is_error:
            rate_limit_alcancado = True

            # Validações extras para garantir que a mensagem de erro está correta
            mensagem = inner_sc.get("message", "")
            assert "Rate limit exceeded" in mensagem, (
                f"Unexpected error message: {mensagem}"
            )

            break

    # Asserções finais do teste
    assert rate_limit_alcancado, (
        f"O rate limit não foi atingido após {max_tentativas} requisições."
    )
    print(f"Rate limit atingido com sucesso após {total_requisicoes} requisições.")
