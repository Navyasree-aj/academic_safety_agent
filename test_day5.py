# test_day5.py
from src.agent import agent_executor

def run_dispatch_tests():
    print("=========================================================")
    print(" 📡 EXECUTING DISPATCH LOOP ON ALICE (CRITICAL / HIGH SCORE) ")
    print("=========================================================")
    output_alice = agent_executor.invoke({"student_id": "STU_991", "logs": []})
    
    print("\n=========================================================")
    print(" 📡 EXECUTING DISPATCH LOOP ON BOB (LOW / SAFE SCORE) ")
    print("=========================================================")
    output_bob = agent_executor.invoke({"student_id": "STU_992", "logs": []})

if __name__ == "__main__":
    run_dispatch_tests()