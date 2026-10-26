from api_mcp.domain.customer import Customer, CustomerQuery, is_present
from api_mcp.infrastructure.customer_http_client import CustomerHTTPClient


class CustomerService:
    def __init__(self, base_url: str, service_token: str) -> None:
        self._client = CustomerHTTPClient(base_url, service_token)

    async def list_customers(self):
        return await self._client.list_customers()

    async def create_customer(self, customer: Customer):
        return await self._client.create_customer(customer)

    async def find_customer(self, query: CustomerQuery):
        if is_present(query._id):
            return await self._client.get_customer_by_id(query._id)

        filters = query.filters
        if not filters:
            return None

        customers = await self._client.list_customers()

        for customer in customers:
            match = True
            for key, value in filters.items():
                customer_value = getattr(customer, key, "")

                if (
                    str(value).strip().lower()
                    not in str(customer_value).strip().lower()
                ):
                    match = False
                    break

            if match:
                return customer

        return None

    async def update_customer(self, customer: Customer):
        return await self._client.update_customer(customer)

    async def delete_customer(self, customer_id: str):
        return await self._client.delete_customer(customer_id)
