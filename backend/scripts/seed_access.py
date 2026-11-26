from os import getenv
from sqlalchemy import select

from db.session import SessionLocal
from modules.access.models import Role, User
from modules.access.schemas import UserCreate
from modules.access.services import create_user, get_role
from modules.employees.models import Employee

def main() -> None:
    employee_id = getenv("SEED_ACCESS_EMPLOYEE_ID", "").strip()
    username = getenv("SEED_ACCESS_USERNAME", "").strip()
    password = getenv("SEED_ACCESS_PASSWORD", "")

    if not employee_id or not username or not password:
        raise SystemExit("Seed configuration is incomplete.")

    if len(password) < 8 or len(password) > 1024:
        raise SystemExit("Seed password must have between 8 and 1024 characters.")

    with SessionLocal() as db:
        if db.scalar(select(User.id).limit(1)) is not None:
            print("Seed skipped. An account already exists.")
            return

        if db.get(Employee, employee_id) is None:
            raise SystemExit("Employee record was not found.")

        manager_role = get_role(db, "hr_manager")
        if manager_role is None:
            manager_role = Role(name="hr_manager")
            db.add(manager_role)

        if get_role(db, "employee") is None:
            db.add(Role(name="employee"))

        data = UserCreate(
            employee_id=employee_id,
            username=username,
            password=password
        )
        create_user(db, data, manager_role)

    print("Seed account created.")

if __name__ == "__main__":
    main()