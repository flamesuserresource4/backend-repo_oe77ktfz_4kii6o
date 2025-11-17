from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from database import get_db, create_document, get_documents
from schemas import Product, Message

app = FastAPI(title="Medical Apparel Store API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "API is running", "backend": "FastAPI"}


@app.get("/test")
async def test_db():
    try:
        database = await get_db()
        collections = await database.list_collection_names()
        return {
            "backend": "FastAPI",
            "database": "MongoDB",
            "database_url": "hidden",
            "database_name": database.name,
            "connection_status": "connected",
            "collections": collections,
        }
    except Exception as e:
        return {"backend": "FastAPI", "database": "MongoDB", "connection_status": f"error: {e}"}


# Products endpoints
@app.get("/products", response_model=List[Product])
async def list_products(tag: str | None = None):
    filter_dict = {"tags": {"$in": [tag]}} if tag else {}
    items = await get_documents("product", filter_dict, limit=100)
    return [Product(**item) for item in items]


class CreateProduct(BaseModel):
    name: str
    description: str
    price: float
    currency: str = "AED"
    images: List[str] = []
    tags: List[str] = []
    in_stock: bool = True


@app.post("/products", status_code=201)
async def create_product(payload: CreateProduct):
    try:
        new_id = await create_document("product", payload.model_dump())
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Contact messages
class CreateMessage(BaseModel):
    name: str
    email: str
    subject: str
    message: str


@app.post("/contact", status_code=201)
async def create_message(payload: CreateMessage):
    try:
        new_id = await create_document("message", payload.model_dump())
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
