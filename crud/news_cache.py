# @Time : 2026/3/25 0025 22:29
# @Author : HaoJun Chen
# @APP : PyCharm
from fastapi.encoders import jsonable_encoder

from models.news import Category, News
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from cache.news_cache import get_cache_categories, set_cache_categories, get_cache_news_list, set_cache_news_list
from schemas.base import NewsItemBase


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    # 尝试从缓存中获取数据
    cached_categories = await get_cache_categories()
    if cached_categories:
        return cached_categories

    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories = result.scalars().all()  # categories 是ORM结果
    print("categories", categories)
    # 写入缓存
    if categories:
        categories = jsonable_encoder(categories)  # 将 ORM 对象等复杂对象，转换成字典、列表、字符串、json等
        await set_cache_categories(categories, expire=60 * 60 * 2)
    # 返回数据
    return categories


async def get_news_list(
        db: AsyncSession,
        category_id: int,  # alias="categoryId"
        skip: int = 0,
        limit: int = 10,
):
    # 读取缓存-新闻列表
    # 页码：跳过的数量skip = (页码-1) * 每页数量  --》 跳过的数量 // 每页数量 + 1
    page = skip // limit + 1
    cache_news_list = await get_cache_news_list(category_id, page, limit)  # 缓存json数据
    if cache_news_list:
        return [News(**item) for item in cache_news_list]

    # 查询的是指定分类下的所有新闻
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    news_list = result.scalars().all()

    # 写入缓存-新闻列表
    if news_list:
        # 先把 ORM 数据 转换 字典才能写入缓存
        # ORM 转成 Pydantic,  再转为字典
        # by_alias=False 不使用别名，保存 python 风格， 因为 Redis 数据是给后端用的
        news_data = [NewsItemBase.model_validate(item).model_dump(mode="json", by_alias=False) for item in news_list]
        await set_cache_news_list(category_id, page, limit, news_data)
    # 返回数据
    return news_list


async def get_news_count(db: AsyncSession, category_id: int):
    """
    # 查询的是指定分类下的所有新闻数量
    :param db:
    :param category_id:
    :return:
    """
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()  # scalar_one：只能有一个结果，否者就报错


async def get_news_detail(db: AsyncSession, news_id: int):
    """
    # 获取新闻详情
    :param db:
    :param news_id:
    :return:
    """
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def increase_news_views(db: AsyncSession, news_id: int):
    """
    # 更新新闻浏览量
    :param db:
    :param news_id:
    :return:
    """
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()

    # 更新 -》 检查数据库是否真的命中了数据库 -》 命中了返回  True
    return result.rowcount > 0


async def get_related_news(db: AsyncSession, news_id: int, category_id: int, limit: int = 5):
    # order_by 排序 -》 浏览量和发布时间
    stmt = select(News).where(
        News.id != news_id,
        News.category_id == category_id
    ).order_by(
        News.views.desc(),  # 默认是升序， desc 表示降序
        News.publish_time.desc()
    ).limit(limit)

    result = await db.execute(stmt)
    # 列表推导式 推导出新闻的核心数据，然后再 return
    return [{
        "id": news.id,
        "title": news.title,
        "content": news.content,
        "image": news.image,
        "author": news.author,
        "publishTime": news.publish_time,
        "categoryId": news.category_id,
        "views": news.views,
    } for news in result.scalars().all()]
