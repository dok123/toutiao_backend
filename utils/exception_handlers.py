# @Time : 2026/4/1 0001 21:23
# @Author : HaoJun Chen
# @APP : PyCharm
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from utils.exception import http_exception_handler, integrity_error_handler, sqlalchemy_error_handler, general_exception_handler



def register_exception_handlers(app):
    """
    注册全局异常处理函数：子类在前，父类在后；具体的在前，抽象（不具体）在后
    :param app:
    :return:
    """
    # HttpException:异常处理器类型，general_exception_handler：异常处理器的名字（函数名）
    app.add_exception_handler(HTTPException, http_exception_handler)  # 业务层面错误
    app.add_exception_handler(IntegrityError, integrity_error_handler)  # 数据完整性约束
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)  # 数据库层面错误
    app.add_exception_handler(Exception, general_exception_handler)  # 兜底
