# @Time : 2026/3/30 0030 21:27
# @Author : HaoJun Chen
# @APP : PyCharm

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_conf import get_db
from schemas.users import UserRequest
from crud import users

router = APIRouter(prefix="/api/user", tags=["users"])


@router.post("/register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    """

    :param user_data:
    :param db:
    :return:
    """
    # {
    #     "username": "chenhaojun",
    #     "password": "123456"
    # }
    # 如果有报错什么 longer 降级 pip install bcrypt == 4.3.0

    #  注册逻辑：验证用户是否存在 -> 创建用户 -> 生成token -> 响应结果
    existing = await users.get_user_by_username(db, user_data.username)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已存在")
    user = await users.create_user(db, user_data)
    return {
        "code": 200,
        "message": "注册成功",
        "data": {
            "token": "用户访问令牌",
            "userInfo": {
                "id": user.id,
                "username": user.username,
                "bio": user.bio,
                "avatar": user.avatar,
            }
        }
    }
