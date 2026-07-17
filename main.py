# main.py
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agent import agent_executor

# Initialize our FastAPI Application
app = FastAPI(
    title="Academic Safety Guard - Agent Service",
    description="REST API exposing our LangGraph hybrid reasoning agent.",
    version="1.0.0"
)

# Define our strict incoming request schema
class EvaluationRequest(BaseModel):
    student_id: str

# Define our structured response schema
class EvaluationResponse(BaseModel):
    student_id: str
    student_name: str | None
    calculated_risk_level: str | None
    urgency_score: float | None
    reasoning_summary: str | None
    execution_logs: list[str]

@app.get("/")
def read_root():
    return {"status": "online", "agent": "Academic Safety Guard LangGraph Engine"}

@app.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_student(payload: EvaluationRequest):
    """
    HTTP POST endpoint to run the reasoning agent against a student record.
    """
    try:
        print(f"\n⚡ API Triggered: Evaluating student {payload.student_id}")
        
        # Invoke our LangGraph executor
        initial_state = {"student_id": payload.student_id, "logs": []}
        result = agent_executor.invoke(initial_state)
        
        # If student wasn't found, check if metadata returned empty
        if not result.get("student_name") and not result.get("perception_data"):
            raise HTTPException(
                status_code=404, 
                detail=f"Student record with ID '{payload.student_id}' does not exist in database."
            )
            
        return EvaluationResponse(
            student_id=payload.student_id,
            student_name=result.get("student_name"),
            calculated_risk_level=result.get("calculated_risk_level"),
            urgency_score=result.get("urgency_score"),
            reasoning_summary=result.get("reasoning_summary"),
            execution_logs=result.get("logs", [])
        )
        
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        print(f"❌ API Exception: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal agent execution crash: {str(e)}")

if __name__ == "__main__":
    # Run server locally on Port 8000
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)