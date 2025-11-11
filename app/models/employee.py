import enum
import html
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


class Position(enum.StrEnum):
    MARKETING_COORDINATOR = "Marketing Coordinator"
    HR_SPECIALIST = "HR Specialist"
    DATA_ANALYST = "Data Analyst"
    PROJECT_MANAGER = "Project Manager"
    SOFTWARE_ENGINEER = "Software Engineer"


class Employee(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr = Field(max_length=100)
    birth_date: date
    hire_date: date
    position: Position = Field(max_length=50)
    salary: condecimal(max_digits=10, decimal_places=2)  # type: ignore

    @field_validator("salary", mode="after")
    def salary_convertor(cls, v: Decimal) -> Decimal:
        if v < Decimal(0):
            raise ValueError("Salary cannot be a negative number")
        return Decimal(float(v) * 100)

    @field_validator("first_name", "last_name", mode="after")
    def escape_field(cls, v: str) -> str:
        return html.escape(v)


class POSTEmployeeRequest(Employee): ...


class POSTEmployeeResponse(BaseModel):
    id: int


class EmployeeOutput(Employee):
    id: int

    model_config = ConfigDict(from_attributes=True)

    @field_validator("salary", mode="after")
    def salary_convertor(cls, v: Decimal) -> Decimal:
        return Decimal(v / 100)

    @field_serializer("salary")
    def salary_floating_point(self, v: Decimal) -> Decimal:
        return v.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)


class GETEmployeeResponse(EmployeeOutput): ...


class PATCHEmployeeRequest(Employee): ...


class PATCHEmployeeResponse(EmployeeOutput): ...


class GETListEmployeeQueryParams(BaseModel):
    offset: int = Field(default=0, ge=0, le=100)
    limit: int = Field(default=25, gt=0)
    position: str | None = Field(default=None)
    min_salary: Decimal | None = Field(default=None)
    max_salary: Decimal | None = Field(default=None)

    @field_validator("max_salary", "min_salary", mode="after")
    def salary_convertor(cls, v: Decimal) -> Decimal:
        return Decimal(float(v) * 100)


class GETListEmployeeResponse(BaseModel):
    total: int
    offset: int
    limit: int
    employees: list[GETEmployeeResponse]
