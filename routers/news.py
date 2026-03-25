# @Time : 2026/3/22 0022 18:27
# @Author : HaoJun Chen
# @APP : PyCharm

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud import news
from config.db_conf import get_db

# 创建 APIRouter 实例
# prefix 路由前缀
# tags  分组（标签）
router = APIRouter(prefix="/api/news", tags=["news"])

@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    # 先获取数据库里面的新闻分类数据 -> 先定义模型 -> 封装查询数据的方法
    categories = await news.get_categories(db, skip, limit)
    return {
        "status": 200,
        "message": "获取新闻分类成功",
        "data": categories
    }