# @Time : 2026/3/25 0025 22:29
# @Author : HaoJun Chen
# @APP : PyCharm

from models.news import Category
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select

async def get_categories(db:AsyncSession, skip: int = 0, limit: int = 100):
    stmt = Select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()