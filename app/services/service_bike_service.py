from app.repositories.service_bike_repo import ServiceBikeRepository
from app.schemas.service_bike import ServiceBikeCreate, ServiceBikeUpdate
from app.db.models.services_bike import ServiceBike

class ServiceBikeService:
    def __init__(self, repo: ServiceBikeRepository):
        self.repo = repo

    async def get_by_id(self, service_bike_id: int) -> ServiceBike | None:
        return await self.repo.get_by_id(service_bike_id)

    async def list(self) -> list[ServiceBike]:
        return await self.repo.list()

    async def create(self, data: ServiceBikeCreate) -> ServiceBike:
        return await self.repo.create(data)

    async def update(self, service_bike_id: int, data: ServiceBikeUpdate) -> ServiceBike | None:
        return await self.repo.update(service_bike_id, data)

    async def delete(self, service_bike_id: int) -> None:
        return await self.repo.delete(service_bike_id)
