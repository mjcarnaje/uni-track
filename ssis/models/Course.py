from typing import Optional, List

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_serializer import SerializerMixin

from .. import db


class Course(db.Model, SerializerMixin):
    __tablename__ = 'course'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(256), unique=True)
    code: Mapped[str] = mapped_column(String(16), unique=True)
    photo: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    college_id: Mapped[int] = mapped_column(Integer, ForeignKey("college.id"))
    students: Mapped[List["Student"]] = relationship(
        "Student", back_populates="course")

    def __repr__(self):
        return f"<Course name:{self.name} college_id:{self.college_id}>"
