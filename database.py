import os
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "appdb")

logger = logging.getLogger("database")
logging.basicConfig(level=logging.INFO)

_client: Optional[AsyncIOMotorClient] = None
db: Optional[AsyncIOMotorDatabase] = None

async def get_db() -> AsyncIOMotorDatabase:
    global _client, db
    if db is None:
        _client = AsyncIOMotorClient(DATABASE_URL)
        db = _client[DATABASE_NAME]
        logger.info("Connected to MongoDB at %s/%s", DATABASE_URL, DATABASE_NAME)
    return db

async def create_document(collection_name: str, data: Dict[str, Any]) -> str:
    database = await get_db()
    now = datetime.utcnow().isoformat()
    data["created_at"] = data.get("created_at", now)
    data["updated_at"] = data.get("updated_at", now)
    result = await database[collection_name].insert_one(data)
    return str(result.inserted_id)

async def get_documents(collection_name: str, filter_dict: Dict[str, Any] | None = None, limit: int = 50) -> List[Dict[str, Any]]:
    database = await get_db()
    cursor = database[collection_name].find(filter_dict or {}).limit(limit)
    items: List[Dict[str, Any]] = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        items.append(doc)
    return items
