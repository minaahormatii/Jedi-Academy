import marshmallow as ma
from models.master import MastersSchema
from sqlalchemy.dialects.postgresql import UUID
import uuid

from db import db
from models.padawan_course_xref import padawans_courses_association_table


class Padawans(db.Model):
    __tablename__ = "Padawans"

    padawan_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    master_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("Masters.master_id"),
        nullable=False,
    )
    user_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("AppUsers.user_id"),
        nullable=False,
    )
    species_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("Species.species_id"),
        nullable=False,
    )
    padawan_name = db.Column(db.String(), nullable=False, unique=True)
    age = db.Column(db.Integer())
    training_level = db.Column(db.Integer())
    graduation_date = db.Column(db.Date())

    species = db.relationship(
        "Species",
        back_populates="padawans",
    )
    user = db.relationship(
        "AppUsers",
        back_populates="padawans",
    )
    master = db.relationship(
        "Masters",
        back_populates="padawans",
    )
    courses = db.relationship(
        "Courses",
        secondary=padawans_courses_association_table,
        back_populates="padawans",
    )

    def __init__(self, master_id, user_id, species_id, padawan_name, age=0, training_level=0, graduation_date=None):
        self.master_id = master_id
        self.user_id = user_id
        self.species_id = species_id
        self.padawan_name = padawan_name
        self.age = age
        self.training_level = training_level
        self.graduation_date = graduation_date

    def new_padawan_obj():
        return Padawans("", "", "", "", 0, 0, None)


# class PadawansSchema(ma.Schema):
#     class Meta:
#         fields = [
#             'padawan_id',
#             'padawan_name',
#             'age',
#             'training_level',
#             'graduation_date',
#             'master',
#             'user',
#             'species'
#         ]

#     padawan_id = ma.fields.UUID()
#     padawan_name = ma.fields.String(required=True)
#     age = ma.fields.Integer(allow_none=True)
#     training_level = ma.fields.Integer(allow_none=True)
#     graduation_date = ma.fields.Date(allow_none=True)
#     master = ma.fields.Nested("MastersSchema", exclude=["padawans"])
#     user = ma.fields.Nested("AppUsersSchema")
#     species = ma.fields.Nested("SpeciesSchema")

class PadawansSchema(ma.Schema):
    class Meta:
        fields = [
            'padawan_id',
            'master_id',
            'user_id',
            'species_id',
            'padawan_name',
            'age',
            'training_level',
            'graduation_date'
        ]

    padawan_id = ma.fields.UUID()
    master_id = ma.fields.UUID()
    user_id = ma.fields.UUID()
    species_id = ma.fields.UUID()
    padawan_name = ma.fields.String(required=True)
    age = ma.fields.Integer(allow_none=True)
    training_level = ma.fields.Integer(allow_none=True)
    graduation_date = ma.fields.Date(allow_none=True)


padawan_schema = PadawansSchema()
padawans_schema = PadawansSchema(many=True)