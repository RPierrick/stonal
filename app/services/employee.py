from decimal import Decimal

from sqlalchemy import exc, select
from sqlalchemy.orm import Session

from app.core.custom_exceptions import NotFoundError, UniqueConstraintError
from app.db import Employee
from app.models.employee import (
    GETListEmployeeQueryParams,
    PATCHEmployeeRequest,
    POSTEmployeeRequest,
)


class EmployeeService:
    def __init__(self, session: Session):
        self._session = session

    def _commit(self) -> None:
        try:
            self._session.commit()
        except exc.IntegrityError as err:
            raise UniqueConstraintError(str(err.orig)) from err

    def create_employee(self, employee: POSTEmployeeRequest) -> int:
        employee_db = Employee(**employee.model_dump())
        with self._session.begin_nested():
            self._session.add(employee_db)
            self._commit()
        return employee_db.id  # type: ignore

    def retrive_employee(self, employee_id: int) -> Employee:
        employee = self._session.get(Employee, employee_id)
        if employee is None:
            raise NotFoundError(f"Employee id : {employee_id} not found")
        return employee

    def update_employee(
        self, employee_id: int, employee: PATCHEmployeeRequest
    ) -> Employee:
        employee_db = self.retrive_employee(employee_id)
        for key, value in employee.model_dump().items():
            setattr(employee_db, key, value)
        self._commit()
        return employee_db

    def delete_employee(self, employee_id: int) -> None:
        employee_db = self.retrive_employee(employee_id)
        self._session.delete(employee_db)
        self._commit()

    def _list_by_position(self, position: str) -> list[Employee]:
        stmt = select(Employee).where(Employee.position == position)
        return self._session.execute(stmt).scalars().all()  # type: ignore

    def _list_by_salary_range(
        self, min_salary: Decimal | None, max_salary: Decimal | None
    ) -> list[Employee]:
        stmt = select(Employee)
        if min_salary is not None:
            stmt = stmt.where(Employee.salary >= min_salary)
        if max_salary is not None:
            stmt = stmt.where(Employee.salary <= max_salary)
        return self._session.execute(stmt).scalars().all()  # type: ignore

    def _list_using_pagination(self, offset: int, limit: int) -> list[Employee]:
        stmt = select(Employee).offset(offset).limit(limit).order_by(Employee.id)
        return self._session.execute(stmt).scalars().all()  # type: ignore

    def list_employee(self, filter_query: GETListEmployeeQueryParams) -> list[Employee]:
        if filter_query.position is not None:
            return self._list_by_position(filter_query.position)
        if filter_query.min_salary is not None or filter_query.max_salary is not None:
            return self._list_by_salary_range(
                filter_query.min_salary, filter_query.max_salary
            )
        return self._list_using_pagination(filter_query.offset, filter_query.limit)
