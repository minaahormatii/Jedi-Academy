import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID
import uuid

from db import db


class AppUsers(db.Model):
    __tablename__ = "AppUsers"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    temple_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Temples.temple_id"), nullable=False)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(), nullable=False)
    midi_count = db.Column(db.Integer(), default=0)
    active = db.Column(db.Boolean(), nullable=False, default=True)

    temple = db.relationship("Temples", back_populates="users")
    auth = db.relationship("AuthTokens", back_populates="user", cascade="all, delete-orphan")
    master = db.relationship("Masters", back_populates="users", cascade="all, delete-orphan")
    padawans = db.relationship("Padawans", back_populates="user", cascade="all, delete-orphan")
    sabers = db.relationship("Sabers", back_populates="user", cascade="all, delete-orphan")


    def __init__(self, temple_id, username, email, password, role, midi_count=0, active=True):
        self.temple_id = temple_id
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self.midi_count = midi_count
        self.active = active

    def new_user_obj():
        return AppUsers("", "", "", "", "", 0, True)


class AppUsersSchema(ma.Schema):
    class Meta:
        fields = ["user_id", "username", "email", "role", "midi_count", "active", "temple"]

    user_id = ma.fields.UUID()
    username = ma.fields.String(required=True)
    email = ma.fields.String(required=True)
    role = ma.fields.String(required=True)
    midi_count = ma.fields.Integer(allow_none=True)
    active = ma.fields.Boolean(dump_default=True)

    temple = ma.fields.Nested("TemplesSchema", exclude=["users"])


user_schema = AppUsersSchema()
users_schema = AppUsersSchema(many=True)