# seed_data.py
from src.database import init_db, SessionLocal
from src.models import SyllabusLog

def seed_syllabus():
    # 1. Trigger metadata sync to physically create the 'syllabus_log' table
    init_db()
    
    db = SessionLocal()
    try:
        # Check if dummy data already exists to avoid duplication
        existing = db.query(SyllabusLog).first()
        if not existing:
            print("📦 Seeding dummy syllabus remediation data...")
            dummy_topic = SyllabusLog(
                topic_covered="SQL Advanced Joins",
                resource_link="https://university.edu/resources/sql-joins-masterclass",
                lab_assignment="Lab Exercise 3: Complex Multi-Table Queries"
            )
            db.add(dummy_topic)
            db.commit()
            print("🚀 Successfully seeded 'SQL Advanced Joins' into SyllabusLog!")
        else:
            print("ℹ️ SyllabusLog table already contains data. Skipping seed phase.")
    except Exception as e:
        print(f"❌ Error seeding database: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_syllabus()