from app.models.employees import Employee

def employee_response(employee: Employee) -> dict:
    return {
        "id": employee.id,

        "first_name": employee.first_name,
        "middle_name": employee.middle_name,
        "last_name": employee.last_name,

        "employee_code": employee.employee_code,

        "department_id": employee.department_id,
        "department_name": employee.department.name,

        "designation_id": employee.designation_id,
        "designation_name": employee.designation.name,

        "joining_date": employee.joining_date,

        "salary": employee.salary,

        "is_active": employee.is_active,
    }