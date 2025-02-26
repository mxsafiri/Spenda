from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

# Association table for group members
group_members = Table(
    'group_members',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('group_id', Integer, ForeignKey('groups.id'))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    # Relationships
    expenses_paid = relationship("Expense", back_populates="payer")
    groups = relationship("Group", secondary=group_members, back_populates="members")
    debts_owed = relationship("Debt", foreign_keys="Debt.debtor_id", back_populates="debtor")
    debts_owed_to = relationship("Debt", foreign_keys="Debt.creditor_id", back_populates="creditor")

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    members = relationship("User", secondary=group_members, back_populates="groups")
    expenses = relationship("Expense", back_populates="group")

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    description = Column(String)
    date = Column(DateTime(timezone=True), server_default=func.now())
    payer_id = Column(Integer, ForeignKey("users.id"))
    group_id = Column(Integer, ForeignKey("groups.id"))
    
    # Relationships
    payer = relationship("User", back_populates="expenses_paid")
    group = relationship("Group", back_populates="expenses")
    splits = relationship("Split", back_populates="expense")

class Split(Base):
    __tablename__ = "splits"

    id = Column(Integer, primary_key=True, index=True)
    expense_id = Column(Integer, ForeignKey("expenses.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    
    # Relationships
    expense = relationship("Expense", back_populates="splits")

class Debt(Base):
    __tablename__ = "debts"

    id = Column(Integer, primary_key=True, index=True)
    debtor_id = Column(Integer, ForeignKey("users.id"))
    creditor_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    
    # Relationships
    debtor = relationship("User", foreign_keys=[debtor_id], back_populates="debts_owed")
    creditor = relationship("User", foreign_keys=[creditor_id], back_populates="debts_owed_to")
