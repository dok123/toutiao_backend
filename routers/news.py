# @Time : 2026/3/22 0022 18:27
# @Author : HaoJun Chen
# @APP : PyCharm

from fastapi import APIRouter

# 创建 APIRouter 实例
# prefix 路由前缀
# tags  分组（标签）
router = APIRouter(prefix="/api/news", tags=["news"])

@router.get("/categories")
async def get_categories():
    return {"msg": "获取新闻分类列表成功"}