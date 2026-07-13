# seed_db.py
from src.database import engine, Base, SessionLocal
from src.models import Student, AcademicMetric

def seed_database():
    print("Connecting to target database and generating table mappings...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        if db.query(Student).first():
            print("Database already contains records. Skipping seeding step.")
            return

        print("Populating testing records...")
        
        # Profile 1: At-Risk Target (Alice Smith)
        stu1 = Student(
            student_id="STU_991",
            name="Alice Smith",
            email="alice@university.edu",
            parent_phone="+1234567890",
            parent_email="parent.alice@mail.com",
            mentor_email="professor.jones@university.edu",
            current_cgpa=2.4
        )
        metric1 = AcademicMetric(attendance_percentage=62.0, assignment_score=45.0, exam_score=52.0)
        stu1.metrics.append(metric1)

        # Profile 2: Clean Standard Target (Bob Miller)
        stu2 = Student(
            student_id="STU_992",
            name="Bob Miller",
            email="bob@university.edu",
            parent_phone="+1987654321",
            parent_email="parent.bob@mail.com",
            mentor_email="professor.jones@university.edu",
            current_cgpa=3.8
        )
        metric2 = AcademicMetric(attendance_percentage=96.5, assignment_score=88.0, exam_score=92.0)
        stu2.metrics.append(metric2)

        db.add(stu1)
        db.add(stu2)
        db.commit()
        print("Successfully created tables and populated seed records!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()