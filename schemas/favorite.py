# @Time : 2026/4/8 0008 22:02
# @Author : HaoJun Chen
# @APP : PyCharm
from pydantic import BaseModel, Field


class FavoriteCheckResponse(BaseModel):
    is_favorite: bool = Field(..., alias="isFavorite")


# 添加收藏
class FavoriteAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId")

