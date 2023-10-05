import datetime
import enum
from typing import Optional

from sqlalchemy import TIMESTAMP, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .. import db


class Gender(enum.Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"


class Student(db.Model):
    __tablename__ = 'student'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[str] = mapped_column(String(16), unique=True)
    first_name: Mapped[str] = mapped_column(String(256))
    last_name: Mapped[str] = mapped_column(String(256))
    gender: Mapped[Gender] = mapped_column(String(16))
    birthday: Mapped[datetime.datetime] = mapped_column(Date)
    photo: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True))
    college_id: Mapped[int] = mapped_column(Integer, ForeignKey("college.id"))
    course_id: Mapped[int] = mapped_column(Integer, ForeignKey("course.id"))
