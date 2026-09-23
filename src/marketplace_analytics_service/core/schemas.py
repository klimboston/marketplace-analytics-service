from pydantic import BaseModel, ConfigDict, Field


class ProductRead(BaseModel):
    id: int
    name: str
    price: float
    rating: float
    reviews_count: int
    article: str

    model_config = ConfigDict(from_attributes=True)


class MarketPlaceCreate(BaseModel):
    name: str = Field(max_length=60, description="Marketplace name")
    slug: str = Field(min_length=2, max_length=20)
    is_active: bool


class MarketPlaceRead(MarketPlaceCreate):
    id: int


class MarketPlaceWithProductsRead(MarketPlaceCreate):
    id: int
    products: list[ProductRead]

    model_config = ConfigDict(from_attributes=True)


class StartParsingSchema(BaseModel):
    marketplace_id: int
    query_search: str = Field(min_length=2, max_length=100)
