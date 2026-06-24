from app.utils.db_manager import DBManager


class HotelService:
    def __init__(self, db: DBManager):
        self.db = db

    async def get_by_id(self, id: int):
        return await self.db.hotels.get_by_id(id)
