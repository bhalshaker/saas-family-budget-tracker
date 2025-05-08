from sqlalchemy import Column,String,Numeric,DateTime,UUID,ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class GoalModel(BaseModel):
    """
    GoalModel represents a financial goal associated with a user and a family.
    Attributes:
        __tablename__ (str): The name of the database table for this model ("goals").
        user_id (UUID): Foreign key referencing the ID of the associated user.
        family_id (UUID): Foreign key referencing the ID of the associated family.
        name (str): The name of the financial goal.
        target_amount (Decimal): The target amount to be saved for the goal, with a precision of 3 decimal places.
        saved_amount (Decimal): The amount already saved towards the goal, with a precision of 3 decimal places.
        due_date (datetime): The due date for achieving the goal.
        user (UserModel): Relationship to the UserModel, representing the user associated with the goal.
        family (FamilyModel): Relationship to the FamilyModel, representing the family associated with the goal.
    """

    __tablename__ = "goals"
    user_id=Column(UUID(as_uuid=True), ForeignKey('users.id',deferrable=True), nullable=False)
    family_id=Column(UUID(as_uuid=True), ForeignKey('families.id',deferrable=True), nullable=False)
    name = Column(String(), nullable=False)
    target_amount=Column(Numeric(scale=3),nullable=True)
    saved_amount=Column(Numeric(scale=3),nullable=True)
    due_date=Column(DateTime(),nullable=True)
    user=relationship('UserModel',back_populates='goal')
    family=relationship('FamilyModel',back_populates='goal')