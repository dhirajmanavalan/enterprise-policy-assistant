# 🏢 Enterprise Policy Assistant

An AI-powered Multi-Agent Enterprise Assistant that helps employees, managers, and HR teams interact with company policies, employee information, leave management workflows, and approval processes through natural language conversations.

The system combines Multi-Agent Architecture, Retrieval-Augmented Generation (RAG), ChromaDB, MySQL, and Streamlit to deliver an intelligent employee support platform.

---

## 🚀 Features

### 👤 Employee Services

- View Employee Profile
- View Leave Balance
- Submit Leave Requests
- View Leave History
- Check Earned Leave Availability

### 📋 Leave Management

- Apply for Leave
- Track Leave Status
- Approve Leave Requests
- Reject Leave Requests
- Leave Balance Updates

### 📚 Policy Management

- Policy Question Answering
- Leave Policy Retrieval
- Work From Home Policy Retrieval
- Reimbursement Policy Retrieval
- Semantic Search using RAG

### 🔐 Security & Governance

- User Authentication
- Role-Based Access Control (RBAC)
- Audit Logging
- Authorization Validation

### 🤖 AI Features

- Multi-Agent Orchestration
- Retrieval-Augmented Generation (RAG)
- Context-Aware Responses
- Hybrid Query Support

---

# 🏗️ System Architecture

```text
User
 │
 ▼
Streamlit Frontend
 │
 ▼
EnterpriseAssistantOrchestrator
 │
 ▼
AuthenticationAgent
 │
 ▼
QueryRouterAgent
 │
 ├────────────► PolicyRAGAgent
 │
 ├────────────► EmployeeDataAgent
 │
 ├────────────► LeaveRequestAgent
 │
 └────────────► LeaveApprovalAgent
 │
 ▼
ResponseAgent
 │
 ▼
AuditAgent
 │
 ▼
MySQL Database
```

---

# 🤖 Multi-Agent Architecture

## AuthenticationAgent

Responsible for:

- User Authentication
- Credential Validation
- Role Verification

---

## QueryRouterAgent

Responsible for:

- Query Classification
- Agent Selection
- Workflow Routing

---

## EmployeeDataAgent

Responsible for:

- Employee Profile Retrieval
- Leave Balance Retrieval
- Employee Information Queries

---

## LeaveRequestAgent

Responsible for:

- Leave Application Processing
- Leave Validation
- Leave Request Creation

---

## LeaveApprovalAgent

Responsible for:

- Leave Approval
- Leave Rejection
- Authorization Validation

---

## PolicyRAGAgent

Responsible for:

- Policy Retrieval
- Semantic Search
- Context Generation

---

## ResponseAgent

Responsible for:

- Response Formatting
- User-Friendly Output Generation

---

## AuditAgent

Responsible for:

- Activity Logging
- Query Tracking
- Audit Trail Creation

---

# 🗄️ Database Design

## Tables

### Users

Stores:

- Username
- Password Hash
- Role
- Employee Reference

### Employees

Stores:

- Employee Information
- Department Information
- Designation

### Leave Requests

Stores:

- Leave Applications
- Approval Status
- Leave Details

### Leave Balances

Stores:

- Casual Leave
- Sick Leave
- Earned Leave

### Audit Logs

Stores:

- Query History
- Agent Activity
- User Actions

---

# 📚 RAG Pipeline

```text
Policy Documents
      ↓
Document Loader
      ↓
Text Splitter
      ↓
Embedding Model
      ↓
ChromaDB
      ↓
Retriever
      ↓
Context Builder
      ↓
Mistral LLM
      ↓
Response
```

---

# 💻 Technology Stack

## Frontend

- Streamlit

## Backend

- Python
- SQLAlchemy

## Database

- MySQL

## AI & RAG

- ChromaDB
- Sentence Transformers
- Mistral LLM

## Security

- bcrypt
- RBAC

## Logging

- Python Logging
- Audit Tracking

---

# 📂 Project Structure

```text
enterprise-policy-assistant/
│
├── agents/
│   ├── orchestrator/
│   └── specialists/
│
├── db/
│
├── rag/
│
├── shared/
│
├── docs/
│   ├── architecture/
│   │   ├── overview.md
│   │   ├── agent-flow.md
│   │   └── database-rag-design.md
│   │
│   └── setup-guide.md
│
├── app.py
├── main.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/your-username/enterprise-policy-assistant.git

cd enterprise-policy-assistant
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

```bash
.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Database

Update database credentials in:

```text
db/session.py
```

---

## Run Application

### Console Version

```bash
python main.py
```

### Streamlit Frontend

```bash
streamlit run app.py
```

---

# 👥 Sample Users

## Employee

```text
Username : abidhi
Password : Abi@123
```

## HR

```text
Username : poorna
Password : Poorna@123
```

---

# 🧪 Demo Queries

## Employee Queries

```text
Show my profile

Show my leave balance

How many earned leave do I have left?

Show my leave requests
```

---

## Leave Request Queries

```text
I want sick leave from 2026-06-19 to 2026-06-22
```

---

## Policy Queries

```text
What is the leave carry forward policy?

What is the reimbursement policy?

What is the work from home policy?
```

---

## Approval Queries

```text
Approve leave request 15

Reject leave request 15
```

---

## Hybrid Query

```text
What is the leave carry forward policy and show my profile
```

---

# 🔒 Role-Based Access Control

| Role | Permissions |
|--------|-------------|
| Employee | View Profile, Leave Balance, Apply Leave |
| HR | Approve/Reject Leave, Employee Data |
| Manager | Approve/Reject Leave |
| Admin | Full Access |

---

# 📈 Future Enhancements

- Natural Language Date Parsing
- Email Notifications
- Leave Analytics Dashboard
- Team Leave Calendar
- Manager Escalation Workflow
- JWT Authentication
- REST API Integration
- Docker Deployment
- Kubernetes Deployment

---

# 🎯 Project Highlights

✅ Multi-Agent Architecture

✅ Retrieval-Augmented Generation (RAG)

✅ ChromaDB Vector Database

✅ Leave Management Workflow

✅ Role-Based Access Control

✅ Audit Logging

✅ Streamlit Frontend

✅ Enterprise Use Case

---

## Author

**Dhiraj Kumar M**

Aspiring Full Stack Java Developer | AI & Data Science Graduate

GitHub: https://github.com/dhirajmanavalan

LinkedIn: https://www.linkedin.com/in/dhirajkumar-/