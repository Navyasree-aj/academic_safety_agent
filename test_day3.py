# test_day3.py
import os
import json
from dotenv import load_dotenv
from src.agent import agent_executor

def run_reasoning_tests():
    # 1. Load environment configurations from your .env file
    load_dotenv()
    
    # 2. Safety check: ensure your AI credentials are read properly
    if not os.getenv("GROQ_API_KEY"):
        print("❌ CRITICAL ERROR: Please set your GROQ_API_KEY inside your environment or .env file.")
        return

    print("=========================================================")
    print(" 🔎 RUNNING REASONING AGENT ON AT-RISK RECORD (ALICE) ")
    print("=========================================================")
    
    # Fire the LangGraph compiled engine for Alice
    initial_state_alice = {"student_id": "STU_991", "logs": []}
    output_alice = agent_executor.invoke(initial_state_alice)
    
    print("\n--- [GRAPH OUTPUT AUDIT TRAIL] ---")
    for log in output_alice.get("logs", []):
        print(f" 🪵 {log}")
        
    print(f"\n🎯 Final Calculated Risk: {output_alice.get('calculated_risk_level')}")
    print(f"💡 AI Summary Insight: {output_alice.get('reasoning_summary')}")
    print(f"📦 Packed Ingested Data Matrix: {json.dumps(output_alice.get('perception_data'), indent=2)}")
    
    print("\n=========================================================")
    print(" 🔎 RUNNING REASONING AGENT ON EXCELLENT RECORD (BOB) ")
    print("=========================================================")
    
    # Fire the LangGraph compiled engine for Bob
    initial_state_bob = {"student_id": "STU_992", "logs": []}
    output_bob = agent_executor.invoke(initial_state_bob)
    
    print("\n--- [GRAPH OUTPUT AUDIT TRAIL] ---")
    for log in output_bob.get("logs", []):
        print(f" 🪵 {log}")
        
    print(f"\n🎯 Final Calculated Risk: {output_bob.get('calculated_risk_level')}")
    print(f"💡 AI Summary Insight: {output_bob.get('reasoning_summary')}")
    print(f"📦 Packed Ingested Data Matrix: {json.dumps(output_bob.get('perception_data'), indent=2)}")

if __name__ == "__main__":
    run_reasoning_tests()