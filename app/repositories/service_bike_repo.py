from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.services_bike import ServiceBike
from app.schemas.service_bike import ServiceBikeCreate, ServiceBikeUpdate

class ServiceBikeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, service_bike_id: int) -> ServiceBike | None:
        return await self.session.get(ServiceBike, service_bike_id)

    async def list(self) -> list[ServiceBike]:
        res = await self.session.execute(select(ServiceBike))
        return list(res.scalars().all())

    async def create(self, data: ServiceBikeCreate) -> ServiceBike:
        obj = ServiceBike(**data.model_dump())
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, service_bike_id: int, data: ServiceBikeUpdate) -> ServiceBike | None:
        obj = await self.session.get(ServiceBike, service_bike_id)
        if not obj:
            return None
        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(obj, k, v)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, service_bike_id: int) -> None:
        obj = await self.session.get(ServiceBike, service_bike_id)
        if obj:
            await self.session.delete(obj)
            await self.session.commit()
