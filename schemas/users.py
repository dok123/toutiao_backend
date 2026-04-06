# @Time : 2026/3/30 0030 21:35
# @Author : HaoJun Chen
# @APP : PyCharm


from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class UserRequest(BaseModel):
    username: str
    password: str


# user_info 对应的类：基础类
class UserInfoBase(BaseModel):
    """
    用户信息基础数据模型
    """
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")


class UserInfoResponse(UserInfoBase):
    id: int
    username: str

    # 模型类配置
    model_config = ConfigDict(
        from_attributes=True,  # 允许从 ORM 中获取值
    )


# data 数据类型
class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(..., alias="userInfo")

    # 模型类配置
    model_config = ConfigDict(
        populate_by_name=True,  # 兼容别名和字段名（如 UserAuthResponse 类里面的 user_info 和别名 userInfo）
        from_attributes=True,  # 允许从 ORM 中获取值
    )


# 更新用户的模型类
class UpdateUserRequest(BaseModel):
    nickname: str = None
    avatar: str = None
    gender: str = None
    bio: str = None
    phone: str = None
