# test_day2.py
from src.database import SessionLocal
from src.models import Student, AcademicMetric

def verify_perception_layer(student_id: str):
    db = SessionLocal()
    try:
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if not student:
            print(f"Error: Student {student_id} not found.")
            return
            
        latest_metric = db.query(AcademicMetric).filter(
            AcademicMetric.student_id == student_id
        ).order_by(AcademicMetric.recorded_at.desc()).first()
        
        print(f"\n[PERCEPTION READ] Name: {student.name}")
        print(f" -> Current CGPA: {student.current_cgpa}")
        print(f" -> Ingested Attendance: {latest_metric.attendance_percentage}%")
        print(f" -> Ingested Assignment Grade: {latest_metric.assignment_score}/100")
    finally:
        db.close()

if __name__ == "__main__":
    verify_perception_layer("STU_991")
    verify_perception_layer("STU_992")