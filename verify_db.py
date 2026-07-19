# verify_db.py
from src.database import SessionLocal
from src.models import Student, AcademicMetric, SyllabusLog

db = SessionLocal()
try:
    print("--- 🔍 DATABASE DIAGNOSTIC AUDIT ---")
    
    # 1. Inspect Student Metrics
    metric = db.query(AcademicMetric).filter(AcademicMetric.student_id == "STU_991").first()
    if metric:
        print(f"🔹 Alice Attendance: {metric.attendance_percentage}%")
        print(f"🔹 Alice Assignment Score: {metric.assignment_score}")
    else:
        print("❌ No academic metrics found for STU_991!")

    # 2. Check Global Failures
    total = db.query(AcademicMetric).count()
    failed = db.query(AcademicMetric).filter(AcademicMetric.assignment_score < 50.0).count()
    print(f"🔹 Total Students in DB: {total}")
    print(f"🔹 Students with Score < 50: {failed}")
    print(f"🔹 Real-time Class Failure Rate: {(failed/total)*100 if total > 0 else 0}%")

    # 3. Check Syllabus Content
    syllabus_count = db.query(SyllabusLog).count()
    print(f"🔹 Syllabus Log Row Count: {syllabus_count}")
    if syllabus_count > 0:
        latest = db.query(SyllabusLog).order_by(SyllabusLog.id.desc()).first()
        print(f"   ↳ Latest Topic: {latest.topic_covered}")

finally:
    db.close()