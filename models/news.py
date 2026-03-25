# @Time : 2026/3/25 0025 22:18
# @Author : HaoJun Chen
# @APP : PyCharm
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String

class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

class Category(Base):
    __tablename__ = "news_category"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True,comment="分类ID")  # autoincrement= True 自增
    name: Mapped[str] = mapped_column(String(50), unique=True,nullable=False, comment="分类名称")
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="排序")

    def __repr__(self):  # 打印规则，如果不用这个方法，打印出来是对象所在的内存地址
        return f"<Category(id={self.id}, name={self.name}, sort_order={self.sort_order})>"