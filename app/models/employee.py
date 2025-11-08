from datetime import date
from decimal import Decimal

from pydantic import BaseModel, EmailStr, Field, condecimal, field_validator


class Employee(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr = Field(max_length=100)
    birth_date: date
    hire_date: date
    position: str = Field(max_length=50)
    salary: condecimal(max_digits=10, decimal_places=2)  # type: ignore

    @field_validator("salary", mode="after")
    def salary_convertor(cls, v: Decimal) -> Decimal:
        return Decimal(float(v) * 100)


class POSTEmployeeRequest(Employee): ...


class POSTEmployeeResponse(BaseModel):
    id: int
