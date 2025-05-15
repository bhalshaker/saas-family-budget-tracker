from pydantic import BaseModel

class CreateBudgetTransaction(BaseModel):
    budget_id: str
    transaction_id: str
    assigned_amount: float