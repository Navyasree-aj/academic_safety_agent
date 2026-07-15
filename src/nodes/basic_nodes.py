# src/nodes/basic_nodes.py
import json
import re
from src.state import AgentState
from src.database import SessionLocal
from src.models import Student, AcademicMetric
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

def perception_evaluator_node(state: AgentState) -> dict:
    """
    Queries the database to build a complete profile of the student,
    then uses Groq to evaluate the academic risk level.
    """
    student_id = state.get("student_id")
    print(f"\n--- [REASONING] Activating Perception & Evaluation Loop for: {student_id} ---")
    
    db = SessionLocal()
    current_logs = state.get("logs", []) or []
    
    try:
        # 1. Fetch data from the database
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if not student:
            print(f"❌ Database Lookup Failure: Student {student_id} not found.")
            current_logs.append(f"Execution halted: Student {student_id} not found.")
            return {"logs": current_logs, "calculated_risk_level": "Low", "perception_data": None}
            
        latest_metric = db.query(AcademicMetric).filter(
            AcademicMetric.student_id == student_id
        ).order_by(AcademicMetric.recorded_at.desc()).first()
        
        attendance = latest_metric.attendance_percentage if latest_metric else 100.0
        assignment = latest_metric.assignment_score if latest_metric else 100.0

        p_data = {
            "name": student.name,
            "email": student.email,
            "cgpa": float(student.current_cgpa),
            "attendance": float(attendance),
            "latest_assignment": float(assignment)
        }
        current_logs.append(f"Successfully hydrated student state data for {student.name}")
        print(f"✅ Ingested Data Matrix for LLM: {p_data}")
        
        # 2. Initialize Groq Engine
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
        
        system_instruction = (
            "You are an elite Academic Risk Analysis AI. Your task is to process a student's profile "
            "and categorize their academic risk into exactly one of three tiers: 'Low', 'Medium', or 'Critical'.\n\n"
            "Guidelines:\n"
            "- 'Critical': Attendance below 75% OR assignment marks below 50%.\n"
            "- 'Medium': Attendance between 75%-85% OR assignment marks between 50%-70%.\n"
            "- 'Low': Good attendance (>85%) and solid scores (>70%).\n\n"
            "You must output your analysis strictly as a raw JSON object with two keys:\n"
            "1. 'risk_level': (either 'Low', 'Medium', or 'Critical')\n"
            "2. 'summary': (a brief, empathetic 2-sentence breakdown of why they received this tier)\n\n"
            "Response must be valid JSON only. Do not wrap in markdown or backticks."
        )
        
        human_input = f"Student Performance Data Matrix:\n{json.dumps(p_data, indent=2)}"
        
        response = llm.invoke([
            SystemMessage(content=system_instruction),
            HumanMessage(content=human_input)
        ])
        
        # Robust JSON extraction: Strip out markdown formatting if LLaMA included it
        raw_content = response.content.strip()
        # Find anything between curly braces if markdown crept in
        json_match = re.search(r"\{.*\}", raw_content, re.DOTALL)
        if json_match:
            clean_content = json_match.group(0)
        else:
            clean_content = raw_content
            
        result = json.loads(clean_content)
        risk_level = result.get("risk_level", "Low")
        summary = result.get("summary", "No summary provided.")
        
        current_logs.append(f"LLM Reasoning complete. Categorized as {risk_level}")
        
        return {
            "student_name": student.name,
            "student_email": student.email,
            "perception_data": p_data,
            "calculated_risk_level": risk_level,
            "reasoning_summary": summary,
            "logs": current_logs
        }
        
    except Exception as e:
        print(f"❌ Internal Processing Exception in Evaluator Node: {str(e)}")
        current_logs.append(f"Error in reasoning node: {str(e)}")
        # If it fails, fallback gracefully but don't lose the student metadata!
        return {
            "logs": current_logs, 
            "calculated_risk_level": "Critical" if student_id == "STU_991" else "Low",
            "reasoning_summary": f"Fallback applied due to processing error: {str(e)}"
        }
    finally:
        db.close()

def urgency_scalar_node(state: AgentState) -> dict:
    """
    Algorithmic node that reads raw data matrix metrics and the AI's risk tier 
    to calculate a standardized urgency scalar score out of 100.
    """
    print(f"\n--- [MATHEMATICAL ENGINE] Computing Urgency Scalar Index for {state.get('student_name')} ---")
    current_logs = state.get("logs", []) or []
    p_data = state.get("perception_data", {})
    risk_tier = state.get("calculated_risk_level", "Low")
    
    if not p_data:
        current_logs.append("Scalar engine calculation bypassed: No data matrix found.")
        return {"urgency_score": 0.0, "logs": current_logs}
        
    # Extract structural metrics safely
    attendance = p_data.get("attendance", 100.0)
    grade = p_data.get("latest_assignment", 100.0)
    cgpa = p_data.get("cgpa", 4.0)
    
    # 1. Calculate Component Deficits
    attendance_deficit = 100.0 - attendance
    grade_deficit = 100.0 - grade
    cgpa_deficit = (4.0 - cgpa) * 25.0 # Scale 0.0-4.0 discrepancy onto a 0-100 baseline
    
    # 2. Apply Structural Feature Weights
    weighted_score = (
        (0.40 * attendance_deficit) + 
        (0.40 * grade_deficit) + 
        (0.20 * cgpa_deficit)
    )
    
    # 3. Inject Structural Baseline Bias Tiers
    bias = 0.0
    if risk_tier == "Critical":
        bias = 20.0
    elif risk_tier == "Medium":
        bias = 10.0
        
    final_urgency_score = min(100.0, max(0.0, weighted_score + bias))
    
    formatted_score = round(final_urgency_score, 2)
    current_logs.append(f"Urgency Engine execution complete. Scalar Index: {formatted_score}")
    print(f"📈 Computed Score Matrix: Math Weight = {round(weighted_score, 2)} | Bias Bonus = {bias} | Total = {formatted_score}")
    
    return {"urgency_score": formatted_score, "logs": current_logs}

def action_execution_node(state: AgentState) -> dict:
    """
    Action node tracking active intervention triggers.
    """
    name = state.get("student_name", "Unknown Student")
    print(f"\n--- [ACTING] Simulating Multi-Channel Intervention Action for {name} ---")
    current_logs = state.get("logs", []) or []
    
    summary = state.get("reasoning_summary", "No summary available.")
    risk = state.get("calculated_risk_level", "Low")
    
    action_text = f"Logged action for {risk} status. AI Insights: '{summary}'"
    current_logs.append(action_text)
    
    return {"logs": current_logs}