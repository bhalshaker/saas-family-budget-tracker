from sqlalchemy import Column,String
from .base import BaseModel

class FamilyModel(BaseModel):
    __tablename__ = "families"
    family_name = Column(String(), nullable=False)
    #TODO: Add currency column