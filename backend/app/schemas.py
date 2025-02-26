from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    
    class Config:
        orm_mode = True

class GroupBase(BaseModel):
    name: str

class GroupCreate(GroupBase):
    pass

class Group(GroupBase):
    id: int
    created_at: datetime
    members: List[User] = []

    class Config:
        orm_mode = True

class ExpenseBase(BaseModel):
    amount: float
    description: str
    payer_id: int
    group_id: int

class ExpenseCreate(ExpenseBase):
    pass

class Expense(ExpenseBase):
    id: int
    date: datetime
    splits: List['Split'] = []

    class Config:
        orm_mode = True

class SplitBase(BaseModel):
    expense_id: int
    user_id: int
    amount: float

class SplitCreate(SplitBase):
    pass

class Split(SplitBase):
    id: int

    class Config:
        orm_mode = True

class DebtBase(BaseModel):
    debtor_id: int
    creditor_id: int
    amount: float

class DebtCreate(DebtBase):
    pass

class Debt(DebtBase):
    id: int

    class Config:
        orm_mode = True
