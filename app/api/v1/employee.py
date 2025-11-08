from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.core.exception_handler import exception_handler
from app.db.base import SessionLocal
from app.models.employee import (
    GETEmployeeResponse,
    GETListEmployeeQueryParams,
    GETListEmployeeResponse,
    PATCHEmployeeRequest,
    PATCHEmployeeResponse,
    POSTEmployeeRequest,
    POSTEmployeeResponse,
)
from app.services.employee import EmployeeService


app = APIRouter()


def get_employee_service() -> EmployeeService:
    return EmployeeService(session=SessionLocal())


@app.post("/", status_code=status.HTTP_201_CREATED)
@exception_handler
def create_employee(
    employee: POSTEmployeeRequest,
    service: EmployeeService = Depends(get_employee_service),
) -> POSTEmployeeResponse:
    employee_id = service.create_employee(employee)
    return POSTEmployeeResponse(id=employee_id)


@app.get("/{employee_id}")
@exception_handler
def retrive_employee(
    employee_id: int, service: EmployeeService = Depends(get_employee_service)
) -> GETEmployeeResponse:
    employee_db = service.retrive_employee(employee_id)
    return GETEmployeeResponse.model_validate(employee_db)


@app.patch("/{employee_id}")
@exception_handler
def update_employee(
    employee_id: int,
    employee: PATCHEmployeeRequest,
    service: EmployeeService = Depends(get_employee_service),
) -> PATCHEmployeeResponse:
    employee_db = service.update_employee(employee_id, employee)
    return PATCHEmployeeResponse.model_validate(employee_db)


@app.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
@exception_handler
def delete_employee(
    employee_id: int,
    service: EmployeeService = Depends(get_employee_service),
) -> None:
    service.delete_employee(employee_id)


@app.get("/")
@exception_handler
def list_employees(
    filter_query: Annotated[GETListEmployeeQueryParams, Query()],
    service: EmployeeService = Depends(get_employee_service),
) -> GETListEmployeeResponse:
    list_employee_db = service.list_employee(filter_query)
    return GETListEmployeeResponse(
        total=len(list_employee_db),
        offset=filter_query.offset,
        limit=filter_query.limit,
        employees=[
            GETEmployeeResponse.model_validate(employee_db)
            for employee_db in list_employee_db
        ],
    )
