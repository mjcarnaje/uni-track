from typing import Optional

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .. import db


class Course(db.Model):
    __tablename__ = 'course'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(256), unique=True)
    code: Mapped[str] = mapped_column(String(16), unique=True)
    photo: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    college_id: Mapped[int] = mapped_column(Integer, ForeignKey("college.id"))
