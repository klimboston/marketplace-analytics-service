import json

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlmodel import select

from src.marketplace_analytics_service.core.database import redis_client
from src.marketplace_analytics_service.core.dependencies import SessionDep
from src.marketplace_analytics_service.core.models import MarketPlace
from src.marketplace_analytics_service.core.schemas import (
    MarketPlaceCreate,
    MarketPlaceRead,
    MarketPlaceWithProductsRead,
    StartParsingSchema,
)
from src.marketplace_analytics_service.tasks import parcing

router = APIRouter(prefix="/market", tags=["market"])


@router.post("/", response_model=MarketPlaceRead, status_code=status.HTTP_201_CREATED)
async def add_market(market: MarketPlaceCreate, db: SessionDep):
    market_db = MarketPlace(**market.model_dump())
    db.add(market_db)
    try:
        await db.commit()
        await db.refresh(market_db)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="bad request"
        )

    return market_db


@router.post("/parse", status_code=status.HTTP_200_OK)
async def parse(product: StartParsingSchema, db: SessionDep):
    parcing.delay(product.marketplace_id, product.query_search)
    return {"status": "parsing started"}


@router.get("/", response_model=list[MarketPlaceWithProductsRead])
async def get_marketplates(db: SessionDep):

    cached_payload = await redis_client.get("marketplaces_list")
    if cached_payload:
        return json.loads(cached_payload)

    statement = (
        select(MarketPlace)
        .offset(0)
        .limit(100)
        .options(selectinload(MarketPlace.products))
    )

    marketplates = (await db.execute(statement)).scalars().all()

    payload_to_cache = [
        MarketPlaceWithProductsRead.model_validate(marketplace).model_dump()
        for marketplace in marketplates
    ]
    await redis_client.set("marketplaces_list", json.dumps(payload_to_cache), ex=60)

    return marketplates
