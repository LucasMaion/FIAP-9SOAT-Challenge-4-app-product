from peewee import CharField, ForeignKeyField

from src.adapters.driven.infra.models.base_model import BaseModel
from src.adapters.driven.infra.models.persona import Persona


class User(BaseModel):
    username = CharField(unique=True)
    externalId = CharField(unique=True, null=True)
    person = ForeignKeyField(Persona, backref="person", null=True)
