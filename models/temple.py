import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID
import uuid

from db import db

class Temples(db.Model):
    __tablename__ = "Temples"

    temple_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    temple_name = db.Column(db.String(), nullable=False, unique=True)
    planet = db.Column(db.String())
    master_count = db.Column(db.Integer(), default=0)
    padawan_limit = db.Column(db.Integer(), default=0)
    active = db.Column(db.Boolean(), default=True)

    users = db.relationship("AppUsers", back_populates="temple")

    def __init__(self, temple_name, planet=None, master_count=0, padawan_limit=0, active=True):
        self.temple_name = temple_name
        self.planet = planet
        self.master_count = master_count
        self.padawan_limit = padawan_limit
        self.active = active

    def new_temple_obj():
        return Temples("", None, 0, 0, True)


class TemplesSchema(ma.Schema):
    class Meta:
        fields = ['temple_id', 'temple_name', 'planet', 'master_count', 'padawan_limit', 'active', 'users']

    temple_id = ma.fields.UUID()
    temple_name = ma.fields.String(required=True)
    planet = ma.fields.String(allow_none=True)
    master_count = ma.fields.Integer(allow_none=True)
    padawan_limit = ma.fields.Integer(allow_none=True)
    active = ma.fields.Boolean(allow_none=True)
    users = ma.fields.Nested("AppUsersSchema", many=True, exclude=['temple'])


temple_schema = TemplesSchema()
temples_schema = TemplesSchema(many=True)
