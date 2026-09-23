from sqlmodel import Field, Relationship, SQLModel


class MarketPlace(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str = Field(index=True, max_length=60)
    slug: str = Field(index=True, unique=True)
    is_active: bool = Field(default=True)
    products: list["Product"] = Relationship(back_populates="marketplace")


class Product(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    marketplace_id: int = Field(foreign_key="marketplace.id")
    name: str = Field(min_length=2, max_length=200, index=True)
    price: float = Field(gt=0)
    rating: float = Field(ge=1, le=5)
    reviews_count: int = Field(ge=0)
    article: int = Field()

    marketplace: "MarketPlace" = Relationship(back_populates="products")
