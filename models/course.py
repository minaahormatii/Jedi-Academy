import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID
import uuid

from db import db
from models.padawan_course_xref import padawans_courses_association_table


class Courses(db.Model):
    __tablename__ = "Courses"

    course_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    master_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Masters.master_id"), nullable=True)
    course_name = db.Column(db.String(), nullable=False, unique=True)
    difficulty = db.Column(db.String())
    duration_weeks = db.Column(db.Integer())

    master = db.relationship("Masters", back_populates="courses")

    padawans = db.relationship("Padawans", secondary=padawans_courses_association_table, back_populates="courses")

    def __init__(self, master_id, course_name, difficulty=None, duration_weeks=None):
        self.master_id = master_id
        self.course_name = course_name
        self.difficulty = difficulty
        self.duration_weeks = duration_weeks

    def new_course_obj():
                return Courses("", "", None, None)


class CoursesSchema(ma.Schema):
    class Meta:
        fields = ['course_id', 'course_name', 'difficulty', 'duration_weeks', 'master', 'padawans']

    course_id = ma.fields.UUID()
    course_name = ma.fields.String(required=True)
    difficulty = ma.fields.String(allow_none=True)
    duration_weeks = ma.fields.Integer(allow_none=True)
    master = ma.fields.Nested("MastersSchema")
    padawans = ma.fields.Nested("PadawansSchema", many=True)


course_schema = CoursesSchema()
courses_schema = CoursesSchema(many=True)