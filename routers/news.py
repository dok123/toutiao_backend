# @Time : 2026/3/22 0022 18:27
# @Author : HaoJun Chen
# @APP : PyCharm

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from crud import news
from config.db_conf import get_db

from crud import news_cache

# 创建 APIRouter 实例
# prefix 路由前缀
# tags  分组（标签）
router = APIRouter(prefix="/api/news", tags=["news"])


@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    # 先获取数据库里面的新闻分类数据 -> 先定义模型 -> 封装查询数据的方法
    categories = await news_cache.get_categories(db, skip, limit)
    print("categories:", categories)
    return {
        "code": 200,
        "message": "获取新闻分类成功",
        "data": categories
    }


@router.get("/list")
async def get_news_list(
        category_id: int = Query(..., alias="categoryId"),  # alias="categoryId" 设置别名
        page: int = 1,
        page_size: int = Query(10, alias="pageSize", le=100),
        db: AsyncSession = Depends(get_db)
):
    # 思路：处理分页逻辑 -》 查询新闻列表 -》计算总量 -》 计算是否还有更多
    offset = (page - 1) * page_size
    news_list = await news.get_news_list(db, category_id, offset, page_size)
    total = await news.get_news_count(db, category_id)
    hsa_more = offset + page_size < total
    return {
        "code": 200,
        "message": "获取新闻列表成功",
        "data": {
            "list": news_list,
            "total": total,
            "hasMore": hsa_more
        }
    }


@router.get("/detail")
async def get_news_detail(news_id: int = Query(..., alias="id"), db: AsyncSession = Depends(get_db)):
    # 获取新闻详情 + 浏览量+1 + 相关新闻
    news_detail = await news.get_news_detail(db, news_id)
    if not news_detail:
        raise HTTPException(status_code=404, detail="新闻不存在")

    views_result = await news.increase_news_views(db, news_detail.id)
    if not views_result:
        raise HTTPException(status_code=500, detail="新闻不存在")

    related_news = await news.get_related_news(db, news_detail.id, news_detail.category_id)
    print("related_news", related_news)

    return {
        "code": 200,
        "message": "success",
        "data": {
            "id": news_detail.id,
            "title": news_detail.title,
            "content": news_detail.content,
            "image": news_detail.image,
            "author": news_detail.author,
            "publishTime": news_detail.publish_time,
            "categoryId": news_detail.category_id,
            "views": news_detail.views,
            "relatedNews": related_news
        }
    }