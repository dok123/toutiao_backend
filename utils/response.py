# @Time : 2026/3/31 0031 21:45
# @Author : HaoJun Chen
# @APP : PyCharm

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


def success_response(message: str = "success", data=None):
    content = {
        "code": 200,
        "message": message,
        "data": data
    }
    # 目标：把任何的 FastAPI, Pydantic, ORM 对象都转换成 JSON 响应 （使用 jsonable_encoder 完成）
    return JSONResponse(content=jsonable_encoder(content))
