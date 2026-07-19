Academic Safety Guard: Hybrid AI Reasoning Agent
An automated student retention and academic support engine built using FastAPI, LangGraph, and PostgreSQL. The platform evaluates real-time student performance metrics, dynamically generates targeted syllabus remediation packages, and triggers cross-channel notifications when systemic classroom failure metrics are breached.

🏗️ System Architecture
The engine utilizes a deterministic, linear state pipeline structured via LangGraph to ensure dependable execution logs and execution safety:

Plaintext
[START] ──> Perception Evaluator Node ──> Urgency Scalar Node ──> Action Executor Node ──> [END]
Perception Evaluator Node: Hydrates student data from PostgreSQL, computes real-time class failure rates, and extracts syllabus deficiency topics.

Urgency Scalar Node: Generates risk category evaluations and urgency scores based on behavioral metrics.

Action Executor Node: Synthesizes the dynamic remediation copy, updates final routing logs, and dispatches multi-channel alerts.

🛠️ Prerequisites & Installation
1. Clone and Navigate to the Repository
Bash
git clone https://github.com/YOUR_USERNAME/academic_safety_agent.git
cd academic_safety_agent
2. Set Up a Virtual Environment
Bash
# Create environment
python -m venv venv

# Activate environment (Windows PowerShell)
.\venv\Scripts\Activate

# Activate environment (Mac/Linux)
source venv/bin/activate
3. Install Required Components
Bash
pip install -r requirements.txt
(Ensure fastapi, uvicorn, pydantic, langgraph, and sqlalchemy are present in your requirements file).

🚀 Running the Evaluation Pipeline
Step 1: Initialize the Server
Boot up the core service engine. The initialization scripts will automatically handle database table synchronization.

Bash
python main.py
Verify that the console returns a successful database sync message before testing endpoints.

Step 2: Run Database Diagnostics (Optional Validation)
To audit the pre-seeded mock database environment and confirm that target metrics are fully in place to trip safety thresholds, open a separate terminal window and run:

Bash
python verify_db.py
Step 3: Trigger Endpoint Evaluation
Submit an HTTP POST request targeting the evaluation endpoint using PowerShell or curl to observe the complete LangGraph execution output.

PowerShell Input:

PowerShell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/evaluate" -Method Post -ContentType "application/json" -Body '{"student_id": "STU_991"}' | ConvertTo-Json
Alternative Linux/macOS cURL Input:

Bash
curl -X POST "http://127.0.0.1:8000/evaluate" \
     -H "Content-Type: application/json" \
     -d '{"student_id": "STU_991"}'
📋 Expected Evaluation Output
A successful implementation will return a structured JSON response containing calculated risk indices, localized course remediation states, and automated system logs:

JSON
{
    "student_id": "STU_991",
    "student_name": "Alice Smith",
    "calculated_risk_level": "Critical",
    "urgency_score": 65.2,
    "reasoning_summary": "Alice, your current academic performance indicates a high risk due to low attendance and assignment scores, which may impact your overall academic success. It's essential to focus on improving your attendance and assignment grades to get back on track. To help you catch up, we have attached the localized Catch-Up Kit for SQL Advanced Joins to this email.",
    "trigger_batch_insight": true,
    "batch_failure_rate": 0.5,
    "missed_topic_data": {
        "topic": "SQL Advanced Joins",
        "remediation_status": "Pending Kit Dispatch"
    },
    "execution_logs": [
        "Successfully hydrated student state data for Alice Smith",
        "Syllabus Remediation triggered for topic: SQL Advanced Joins",
        "Instructor Batch Insight logged! Class Failure Rate: 50.0%",
        "LLM Reasoning complete. Categorized as Critical",
        "Urgency Engine execution complete. Scalar Index: 65.2",
        "Injected localized Syllabus Catch-Up Kit for SQL Advanced Joins.",
        "Dispatched automated outreach email to alice@university.edu",
        "Escalated high-urgency alert to internal Slack webhook channel.",
        "Action processing finalized. Channels hit: Faculty Insight Dashboard, Student Email + Catch-Up Kit, Advisor Slack"
    ]
}
📂 Project Structure
Plaintext
academic_safety_agent/
│
├── src/
│   ├── nodes/
│   │   └── basic_nodes.py     # Graph processing node definitions
│   ├── agent.py               # LangGraph structural workflow topology
│   ├── state.py               # TypedDict graph state structural schema
│   ├── models.py              # SQLAlchemy ORM models
│   └── database.py            # Session mapping and engine creation
│
├── main.py                    # FastAPI server wrapper and endpoint routers
├── verify_db.py               # Validation script inspecting local database bounds
└── README.md                  # Evaluation guide documentation
