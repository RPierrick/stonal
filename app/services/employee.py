from sqlalchemy import exc
from sqlalchemy.orm import Session

from app.core.custom_exceptions import NotFoundError, UniqueConstraintError
from app.db import Employee
from app.models.employee import POSTEmployeeRequest


class EmployeeService:
    def __init__(self, session: Session):
        self._session = session

    def _commit(self) -> None:
        try:
            self._session.commit()
        except exc.IntegrityError as err:
            raise UniqueConstraintError(str(err.orig)) from err

    def create_employee(self, body: POSTEmployeeRequest) -> int:
        employee = Employee(**body.model_dump())
        with self._session.begin():
            self._session.add(employee)
            self._commit()
        return employee.id  # type: ignore

    def retrive_employee(self, employee_id: int) -> Employee:
        employee = self._session.get(Employee, employee_id)
        if employee is None:
            raise NotFoundError(f"Employee id : {employee_id} not found")
        return employee
