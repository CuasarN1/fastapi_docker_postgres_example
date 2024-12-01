from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, false

from project.infrastructure.postgres.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=True)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=false())


class Study(Base):
    __tablename__ = "studies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)


class UserMarks(Base):
    __tablename__ = "user_marks"

    id: Mapped[int] = mapped_column(primary_key=True)
    mark: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"))
    study_id: Mapped[int] = mapped_column(ForeignKey("studies.id", ondelete="CASCADE", onupdate="CASCADE"))
