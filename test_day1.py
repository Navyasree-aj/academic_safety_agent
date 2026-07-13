# test_day1.py
from src.agent import agent_executor

def run_tests():
    print("==================================================")
    print("TEST CASE 1: High Performing / Low Risk Student")
    print("==================================================")
    initial_state_1 = {
        "student_id": "STU_001",
        "attendance_percentage": 92.5,
        "recent_marks": [85.0, 90.0, 78.0],
        "logs": []
    }
    output_1 = agent_executor.invoke(initial_state_1)
    print("\nFinal State Log Audit Trail:")
    for log in output_1["logs"]:
        print(f" -> {log}")
    print(f"Final Risk Level: {output_1['calculated_risk_level']}")

    print("\n==================================================")
    print("TEST CASE 2: High Risk / Absentee Student")
    print("==================================================")
    initial_state_2 = {
        "student_id": "STU_002",
        "attendance_percentage": 68.0, # Triggers failure mitigation logic
        "recent_marks": [45.0, 50.0, 35.0],
        "logs": []
    }
    output_2 = agent_executor.invoke(initial_state_2)
    print("\nFinal State Log Audit Trail:")
    for log in output_2["logs"]:
        print(f" -> {log}")
    print(f"Final Risk Level: {output_2['calculated_risk_level']}")

if __name__ == "__main__":
    run_tests()