from sqlalchemy.orm import Mapped, mapped_column

from .base_orm import BaseOrm
from ..enums import UserRole


class UserOrm(BaseOrm):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(index=True)
    role: Mapped[UserRole]
