from typing import TypeVar

from pydantic import BaseModel

from app.database import Base


ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper:
    model = ModelType | None
    schema = SchemaType | None
    
    @classmethod
    def map_to_domain_entity(cls, data):
        return cls.schema.model_validate(data, from_attributes=True)