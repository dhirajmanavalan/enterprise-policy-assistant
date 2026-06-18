# Database and RAG Design

## Database Design

The application uses MySQL.

---

## Users Table

Stores authentication information.

| Column | Description |
|----------|-------------|
| id | Primary Key |
| username | Login Username |
| password_hash | Encrypted Password |
| role | employee/hr/manager/admin |
| employee_id | Employee Reference |

---

## Employees Table

Stores employee information.

| Column | Description |
|----------|-------------|
| id | Primary Key |
| employee_id | Employee Number |
| first_name | First Name |
| last_name | Last Name |
| department_id | Department |
| designation | Job Role |

---

## Leave Requests Table

Stores leave applications.

| Column | Description |
|----------|-------------|
| id | Request ID |
| employee_id | Employee |
| leave_type | Sick/Casual/Earned |
| start_date | Leave Start |
| end_date | Leave End |
| status | Pending/Approved/Rejected |

---

## Leave Balances Table

Stores yearly leave balances.

| Column | Description |
|----------|-------------|
| employee_id | Employee |
| year | Year |
| casual_leave_total | Total Casual Leave |
| casual_leave_used | Used Casual Leave |
| sick_leave_total | Total Sick Leave |
| sick_leave_used | Used Sick Leave |
| earned_leave_total | Total Earned Leave |
| earned_leave_used | Used Earned Leave |

---

# RAG Architecture

## Policy Retrieval Pipeline

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

## Embedding Model

Sentence Transformer:

```text
all-MiniLM-L6-v2
```

---

## Vector Database

ChromaDB

Stores:

- Policy embeddings
- Metadata
- Document chunks

---

## Benefits

- Semantic Search
- Faster Retrieval
- Reduced Hallucination
- Context-Aware Answers

---