from sqlalchemy import Column, Date, Integer, String, UniqueConstraint

from app.db.base import Base


class Employee(Base):
    __tablename__ = "Employees"

    id = Column(Integer, primary_key=True, autoincrement=True)

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    birth_date = Column(Date, nullable=False)
    hire_date = Column(Date, nullable=False)
    position = Column(String(50), nullable=False)
    salary = Column(Integer, nullable=False)

    __table_args__ = (UniqueConstraint("email", name="UC_employee_email"),)
