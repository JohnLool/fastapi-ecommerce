from pydantic import BaseModel
from typing import Literal, Optional


class AttributeDefinitionIn(BaseModel):
    name: str
    type: Literal['str', 'int', 'float', 'bool']
    required: bool = False

class AttributeDefinitionOut(AttributeDefinitionIn):
    slug: Optional[str] = None