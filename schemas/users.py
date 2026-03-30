# @Time : 2026/3/30 0030 21:35
# @Author : HaoJun Chen
# @APP : PyCharm


from pydantic import BaseModel


class UserRequest(BaseModel):
    username: str
    password: str
