from app.models.attendance import Attendance

def attendance_response(
    attendance: Attendance,
) -> dict:

    employee = attendance.employee

    employee_name = (
        f"{employee.first_name} "
        f"{employee.last_name}"
    )

    return {
        "id": attendance.id,

        "employee_id":
            attendance.employee_id,

        "employee_name":
            employee_name,

        "attendance_date":
            attendance.attendance_date,

        "status":
            attendance.status,

        "check_in":
            attendance.check_in,

        "check_out":
            attendance.check_out,

        "remarks":
            attendance.remarks,
    }