import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID
import uuid

from db import db


class Sabers(db.Model):
    __tablename__ = "Sabers"

    saber_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("AppUsers.user_id"),
        nullable=False,
    )
    saber_name = db.Column(db.String(), nullable=False, unique=True)
    blade_color = db.Column(db.String())

    user = db.relationship(
        "AppUsers",
        back_populates="sabers",
    )

    def __init__(self, owner_id, saber_name, blade_color=None):
        self.owner_id = owner_id
        self.saber_name = saber_name
        self.blade_color = blade_color

    def new_saber_obj():
            return Sabers("", "", None)


class SabersSchema(ma.Schema):
    class Meta:
        fields = ['saber_id', 'saber_name', 'blade_color', 'user']

    saber_id = ma.fields.UUID()
    saber_name = ma.fields.String(required=True)
    blade_color = ma.fields.String(allow_none=True)
    user = ma.fields.Nested("AppUsersSchema")


saber_schema = SabersSchema()
sabers_schema = SabersSchema(many=True)