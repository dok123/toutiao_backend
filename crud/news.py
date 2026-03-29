# @Time : 2026/3/25 0025 22:29
# @Author : HaoJun Chen
# @APP : PyCharm

from models.news import Category, News
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select, func, update


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    stmt = Select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_news_list(
        db: AsyncSession,
        category_id: int,  # alias="categoryId"
        skip: int = 0,
        limit: int = 10,
):
    # 查询的是指定分类下的所有新闻
    stmt = Select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_news_count(db: AsyncSession, category_id: int):
    """
    # 查询的是指定分类下的所有新闻数量
    :param db:
    :param category_id:
    :return:
    """
    stmt = Select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()  # scalar_one：只能有一个结果，否者就报错


async def get_news_detail(db: AsyncSession, news_id: int):
    """
    # 获取新闻详情
    :param db:
    :param news_id:
    :return:
    """
    stmt = Select(News).where(News.id == news_id)
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
    stmt = Select(News).where(
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
