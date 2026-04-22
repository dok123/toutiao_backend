# @Time : 2026/4/22 0022 22:44
# @Author : HaoJun Chen
# @APP : PyCharm
from typing import List, Dict, Any

from config.cache_conf import set_cache, get_json_cache

# 新闻相关的缓存方法：新闻分类的读取和写入
# key-value
CATEGORIES_KEY = "news:categories"


# 获取新闻分类缓存
async def get_cache_categories():
    return await get_json_cache(CATEGORIES_KEY)


# 写入新闻分类缓存,缓存的数据，过期时间
# 分类、配置 7200; 列表:600; 详情: 1800; 验证码: 120 -- 数据越稳定，缓存越持久
# 避免所有的key同时过期引起缓存雪崩
async def set_cache_categories(data: List[Dict[str, Any]], expire: int = 60 * 60 * 2):
    print("2222222222222222222")
    return await set_cache(CATEGORIES_KEY, data, expire)
