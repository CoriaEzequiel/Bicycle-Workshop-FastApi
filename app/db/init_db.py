from sqlalchemy.ext.asyncio import AsyncSession


async def init_db(session: AsyncSession) -> None:
# seed inicial si hace falta
    return