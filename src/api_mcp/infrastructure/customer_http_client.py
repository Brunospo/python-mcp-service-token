from dataclasses import asdict

import httpx2

from api_mcp.domain.customer import CreateCustomerResult, Customer
from api_mcp.domain.errors import ForbiddenError, RateLimitError, UnauthorizedError


class CustomerHTTPClient:
    def __init__(self, base_url: str, service_token: str) -> None:
        self._base_url = base_url
        self._auth_headers = {"Authorization": f"Bearer {service_token}"}

    async def _assert_ok(self, response: httpx2.Response) -> None:
        if response.status_code == 401:
            raise UnauthorizedError()
        if response.status_code == 403:
            raise ForbiddenError()
        if response.status_code == 429:
            raise RateLimitError()
        if response.is_error:
            raise Exception(
                f"HTTP {response.status_code} - {response.reason_phrase} - {response.text}"
            )

    async def list_customers(self) -> list[Customer]:
        async with httpx2.AsyncClient(base_url=self._base_url) as client:
            response = await client.get("/customers", headers=self._auth_headers)
            await self._assert_ok(response)
            data = response.json()

            return [
                Customer(_id=item["_id"], name=item["name"], phone=item["phone"])
                for item in data
            ]

    async def get_customer_by_id(self, id: str) -> Customer | None:
        async with httpx2.AsyncClient(base_url=self._base_url) as client:
            response = await client.get(f"/customers/{id}", headers=self._auth_headers)
            if response.status_code in (404, 400):
                return None

            await self._assert_ok(response)
            data = response.json()

            return Customer(_id=data["_id"], name=data["name"], phone=data["phone"])

    async def create_customer(self, customer: Customer) -> CreateCustomerResult:
        payload = asdict(customer)
        payload.pop("_id", None)

        async with httpx2.AsyncClient(base_url=self._base_url) as client:
            response = await client.post(
                "/customers",
                json=payload,
                headers={"Content-Type": "application/json", **self._auth_headers},
            )
            await self._assert_ok(response)
            data_res = response.json()

            return CreateCustomerResult(message=data_res["message"], id=data_res["id"])

    async def update_customer(self, customer: Customer) -> CreateCustomerResult:
        payload = asdict(customer)
        payload.pop("_id", None)

        async with httpx2.AsyncClient(base_url=self._base_url) as client:
            response = await client.put(
                f"/customers/{customer._id}",
                json=payload,
                headers={"Content-Type": "application/json", **self._auth_headers},
            )
            await self._assert_ok(response)
            data_res = response.json()

            return CreateCustomerResult(message=data_res["message"], id=data_res["id"])

    async def delete_customer(self, customer_id: str) -> CreateCustomerResult:
        async with httpx2.AsyncClient(base_url=self._base_url) as client:
            response = await client.delete(
                f"/customers/{customer_id}", headers=self._auth_headers
            )
            await self._assert_ok(response)
            data_res = response.json()

            return CreateCustomerResult(message=data_res["message"], id=data_res["id"])
