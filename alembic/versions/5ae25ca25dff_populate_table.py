"""Populate table

Revision ID: 5ae25ca25dff
Revises: df3937484d39
Create Date: 2025-11-07 13:47:53.118463

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.orm import Session

from app.db import Employee
from datetime import date


# revision identifiers, used by Alembic.
revision: str = '5ae25ca25dff'
down_revision: Union[str, Sequence[str], None] = 'df3937484d39'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    session = Session(bind=bind)
    session.add_all([
        Employee(first_name="John", last_name="Doe", email="john.doe@corp.com", birth_date=date(1980, 5, 15), hire_date=date(2010, 6, 1), position="Software Engineer", salary=7500000),
        Employee(first_name="Jane", last_name="Smith", email="jane.smith@corp.com", birth_date=date(1985, 8, 22), hire_date=date(2012, 9, 15), position="Project Manager", salary=9000000),
        Employee(first_name="Emily", last_name="Johnson", email="emily.johnson@corp.com", birth_date=date(1990, 12, 30), hire_date=date(2015, 3, 20), position="Data Analyst", salary=6000000),
        Employee(first_name="Jessica", last_name="Davis", email="jessica.davis@corp.com", birth_date=date(1992, 7, 19), hire_date=date(2018, 7, 30), position="Marketing Coordinator", salary=5500000),
        Employee(first_name="Alice", last_name="Williams", email="alice.williams@corp.com", birth_date=date(1988, 2, 15), hire_date=date(2015, 6, 1), position="Software Engineer", salary=8000000),
        Employee(first_name="David", last_name="Jones", email="david.jones@corp.com", birth_date=date(1983, 9, 22), hire_date=date(2011, 3, 15), position="Project Manager", salary=9500000),
        Employee(first_name="Sophia", last_name="Garcia", email="sophia.garcia@corp.com", birth_date=date(1995, 12, 30), hire_date=date(2019, 1, 20), position="Data Analyst", salary=7000000),
        Employee(first_name="James", last_name="Martinez", email="james.martinez@corp.com", birth_date=date(1978, 11, 10), hire_date=date(2005, 7, 5), position="HR Specialist", salary=6500000),
        Employee(first_name="Olivia", last_name="Lopez", email="olivia.lopez@corp.com", birth_date=date(1990, 7, 19), hire_date=date(2018, 8, 30), position="Marketing Coordinator", salary=6000000),
    ])
    session.commit()


def downgrade() -> None:
    """Downgrade schema."""
    pass
