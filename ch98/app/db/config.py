from motor.motor_asyncio import AsyncIOMotorClient 
from beanie import init_beanie
from decouple import config
from app.account.model import User

DB_URL = config("DATABASE_URL")

async def init_db():
    client = AsyncIOMotorClient(DB_URL)
    await init_beanie(database=client.get_default_database(), document_models=[User])
    