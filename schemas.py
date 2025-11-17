from pydantic import BaseModel, Field
from typing import Optional, List

# Each model corresponds to a MongoDB collection with the class name lowercased

class Product(BaseModel):
    id: Optional[str] = Field(default=None, description="Document ID")
    name: str
    description: str
    price: float
    currency: str = "AED"
    images: List[str] = []
    tags: List[str] = []
    in_stock: bool = True
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class Message(BaseModel):
    id: Optional[str] = Field(default=None)
    name: str
    email: str
    subject: str
    message: str
    created_at: Optional[str] = None

