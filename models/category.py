from sqlalchemy import Column,String,Enum as EnumSQL,UUID,ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel,EntryType
class CategoryModel(BaseModel):
    """
    CategoryModel represents a category entity in the family budget tracker system.
    Attributes:
        __tablename__ (str): The name of the database table associated with this model.
        user_id (UUID): A foreign key referencing the ID of the associated user.
        family_id (UUID): A foreign key referencing the ID of the associated family.
        name (str): The name of the category.
        type (EntryType): The type of the category, represented as an enumeration.
        user (UserModel): A relationship to the UserModel, representing the user associated with this category.
        family (FamilyModel): A relationship to the FamilyModel, representing the family associated with this category.
    """
    
    __tablename__ = "categories"
    user_id=Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    family_id=Column(UUID(as_uuid=True), ForeignKey('families.id'), nullable=False)
    name = Column(String, nullable=False)
    type= Column(EnumSQL(EntryType, name="entry_type", native_enum=True),nullable=False)
    user=relationship('UserModel',back_populates='category')
    family=relationship('FamilyModel',back_populates='category')