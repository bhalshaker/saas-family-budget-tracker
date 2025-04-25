from sqlalchemy import Column,String,Numeric,DateTime,UUID,ForeignKey,Enum
from sqlalchemy.orm import relationship
from .base import BaseModel,EntryType
class TransactionModel(BaseModel):
    __tablename__ = "transactions"
    user_id=Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    family_id=Column(UUID(as_uuid=True), ForeignKey('families.id'), nullable=False)
    account_id=Column(UUID(as_uuid=True), ForeignKey('accounts.id'), nullable=False)
    category_id=Column(UUID(as_uuid=True), ForeignKey('categories.id'), nullable=False)
    amount=Column(Numeric(scale=3),nullable=False)
    date=Column(DateTime(),nullable=False)
    description=Column(String(),nullable=True)
    transaction_type=Column(Enum(EntryType, name="entry_type", native_enum=True),nullable=False)
    attachment=relationship('AttachmentModel',back_populates='transaction',uselist=False)
    user=relationship('UserModel',back_populates='transaction')
    family=relationship('FamilyModel',back_populates='transaction')
    account=relationship('AccountModel',back_populates='transaction')
    category=relationship('CategoryModel',back_populates='transaction')
    budgets=relationship('BudgetTransactionModel',back_populates='transaction')