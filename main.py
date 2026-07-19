# main.py
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agent import compile_agent  # <-- Changed: Import the compilation FUNCTION instead
from src.database import init_db

# Sync database tables
init_db()

# Compile a completely fresh, un-cached runtime engine graph instance on startup
agent_executor = compile_agent()  # <-- Dynamically instantiated here

# Initialize our FastAPI Application
app = FastAPI(
    title="Academic Safety Guard - Agent Service",
    description="REST API exposing our LangGraph hybrid reasoning agent.",
    version="1.0.0"
)

class EvaluationRequest(BaseModel):
    student_id: str

class EvaluationResponse(BaseModel):
    student_id: str
    student_name: str | None
    calculated_risk_level: str | None
    urgency_score: float | None
    reasoning_summary: str | None
    trigger_batch_insight: bool | None        
    batch_failure_rate: float | None          
    missed_topic_data: dict | None            
    execution_logs: list[str]

@app.get("/")
def read_root():
    return {"status": "online", "agent": "Academic Safety Guard LangGraph Engine"}

@app.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_student(payload: EvaluationRequest):
    """HTTP POST endpoint to run the reasoning agent against a student record."""
    try:
        print(f"\n⚡ API Triggered: Evaluating student {payload.student_id}")
        
        # Invoke our freshly compiled graph execution flow
        initial_state = {"student_id": payload.student_id, "logs": []}
        result = agent_executor.invoke(initial_state)
        
        if not result.get("student_name") and not result.get("perception_data"):
            raise HTTPException(
                status_code=404, 
                detail=f"Student record with ID '{payload.student_id}' does not exist."
            )
            
        return EvaluationResponse(
            student_id=payload.student_id,
            student_name=result.get("student_name"),
            calculated_risk_level=result.get("calculated_risk_level"),
            urgency_score=result.get("urgency_score"),
            reasoning_summary=result.get("reasoning_summary"),
            trigger_batch_insight=result.get("trigger_batch_insight"),  
            batch_failure_rate=result.get("batch_failure_rate"),        
            missed_topic_data=result.get("missed_topic_data"),          
            execution_logs=result.get("logs", [])
        )
        
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        print(f"❌ API Exception: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal crash: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)