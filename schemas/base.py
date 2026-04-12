# @Time : 2026/4/12 0012 18:36
# @Author : HaoJun Chen
# @APP : PyCharm

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class NewsItemBase(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    author: Optional[str] = None
    category_id: int = Field(..., alias="categoryId")
    views: int
    publish_time: Optional[datetime] = Field(None, alias="publishTime")
    model_config = ConfigDict(
        from_attributes=True,  # 允许从 ORM 中获取值
        populate_by_name=True,
    )
