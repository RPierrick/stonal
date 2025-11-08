from datetime import date
from decimal import ROUND_HALF_UP, Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    condecimal,
    field_serializer,
    field_validator,
)


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


class GETEmployeeResponse(Employee):
    id: int

    model_config = ConfigDict(from_attributes=True)

    @field_validator("salary", mode="after")
    def salary_convertor(cls, v: Decimal) -> Decimal:
        return Decimal(v / 100)

    @field_serializer("salary")
    def salary_floating_point(self, v: Decimal) -> Decimal:
        return v.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
