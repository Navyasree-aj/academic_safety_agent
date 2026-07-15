# test_day4.py
import json
from src.agent import agent_executor

def run_scalar_tests():
    print("=========================================================")
    print(" 🔢 TESTING HYBRID GRAPH RUN ON ALICE (HIGH DEFICIT) ")
    print("=========================================================")
    output_alice = agent_executor.invoke({"student_id": "STU_991", "logs": []})
    print(f"🎯 Risk Tier: {output_alice.get('calculated_risk_level')}")
    print(f"📊 Calculated Urgency Score: {output_alice.get('urgency_score')} / 100.0")
    
    print("\n=========================================================")
    print(" 🔢 TESTING HYBRID GRAPH RUN ON BOB (EXCELLENT STATUS) ")
    print("=========================================================")
    output_bob = agent_executor.invoke({"student_id": "STU_992", "logs": []})
    print(f"🎯 Risk Tier: {output_bob.get('calculated_risk_level')}")
    print(f"📊 Calculated Urgency Score: {output_bob.get('urgency_score')} / 100.0")

if __name__ == "__main__":
    run_scalar_tests()