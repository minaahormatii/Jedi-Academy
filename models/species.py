import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID
import uuid

from db import db

class Species(db.Model):
    __tablename__ = "Species"

    species_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    species_name = db.Column(db.String(), nullable=False, unique=True)
    homeworld = db.Column(db.String())
    lifespan = db.Column(db.Integer())

    masters = db.relationship(
        "Masters",
        back_populates="species"
    )

    padawans = db.relationship(
        "Padawans",
        back_populates="species"
    )

    def __init__(self, species_name, homeworld=None, lifespan=0):
        self.species_name = species_name
        self.homeworld = homeworld
        self.lifespan = lifespan

    def new_species_obj():
                return Species("", "", 0)


class SpeciesSchema(ma.Schema):
    class Meta:
        fields = ['species_id', 'species_name', 'homeworld', 'lifespan', 'masters', 'padawans']

    species_id = ma.fields.UUID()
    species_name = ma.fields.String(required=True)
    homeworld = ma.fields.String(allow_none=True)
    lifespan = ma.fields.Integer(allow_none=True)
    masters = ma.fields.Nested("MastersSchema", many=True)
    padawans = ma.fields.Nested("PadawansSchema", many=True)


species_schema = SpeciesSchema()
species_many_schema = SpeciesSchema(many=True)
