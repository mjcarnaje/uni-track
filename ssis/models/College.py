from typing import Optional, List

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_serializer import SerializerMixin

from .. import db
from .Course import Course


class College(db.Model, SerializerMixin):
    __tablename__ = 'college'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(256), unique=True)
    code: Mapped[str] = mapped_column(String(16), unique=True)
    photo: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    courses: Mapped[List['Course']] = relationship(
        "Course", backref="college", lazy=True)
    students: Mapped[List["Student"]] = relationship(
        "Student", back_populates="college")
