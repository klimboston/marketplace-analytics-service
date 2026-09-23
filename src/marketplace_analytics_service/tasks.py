import asyncio
import random

from src.marketplace_analytics_service.core.celery_app import celery_app
from src.marketplace_analytics_service.core.database import sessionmaker
from src.marketplace_analytics_service.core.models import Product


async def parse(marketplace_id: int, query_search: str):
    base_products = [
        f" Смартфон {query_search} Pro",
        f" Чехол для {query_search}",
        f" Кабель {query_search} Fast Charge",
    ]
    


    async with sessionmaker() as db:
        products_list = []
        for i in range(5):
            await asyncio.sleep(1)
            product = Product(
                marketplace_id=marketplace_id,
                name=f"Товар {query_search}",
                price=random.randint(1000, 100000),
                rating=random.uniform(1, 5),
                reviews_count=random.randint(5, 50),
                article=random.randint(10000000, 99999999),
            )
            products_list.append(product)
        db.add_all(products_list)
        await db.commit()


@celery_app.task
def parcing(marketplace_id: int, query_search: str) -> None:
    print("Начинается парсинг данных")
    asyncio.run(parse(marketplace_id, query_search))
    print("Парсинг завершен")
