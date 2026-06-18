# Agent Workflow

## 1. Employee Profile Query

Query:

Show my profile

Flow:

```text
User
 ↓
AuthenticationAgent
 ↓
QueryRouterAgent
 ↓
EmployeeDataAgent
 ↓
ResponseAgent
 ↓
AuditAgent
```

---

## 2. Leave Balance Query

Query:

How many earned leave do I have left?

Flow:

```text
User
 ↓
AuthenticationAgent
 ↓
QueryRouterAgent
 ↓
EmployeeDataAgent
 ↓
ResponseAgent
 ↓
AuditAgent
```

---

## 3. Leave Request Submission

Query:

I want sick leave from 2026-06-19 to 2026-06-22

Flow:

```text
User
 ↓
AuthenticationAgent
 ↓
QueryRouterAgent
 ↓
LeaveRequestAgent
 ↓
ResponseAgent
 ↓
AuditAgent
```

---

## 4. Policy Retrieval

Query:

What is the leave carry forward policy?

Flow:

```text
User
 ↓
AuthenticationAgent
 ↓
QueryRouterAgent
 ↓
PolicyRAGAgent
 ↓
RAG Pipeline
 ↓
ResponseAgent
 ↓
AuditAgent
```

---

## 5. Leave Approval

Query:

Approve leave request 15

Flow:

```text
User (HR)
 ↓
AuthenticationAgent
 ↓
QueryRouterAgent
 ↓
LeaveApprovalAgent
 ↓
ResponseAgent
 ↓
AuditAgent
```

---

## 6. Leave Rejection

Query:

Reject leave request 15

Flow:

```text
User (HR)
 ↓
AuthenticationAgent
 ↓
QueryRouterAgent
 ↓
LeaveApprovalAgent
 ↓
ResponseAgent
 ↓
AuditAgent
```

---

## 7. Unauthorized Access

Query:

Approve leave request 15

User Role:

Employee

Result:

```text
Authorization Failed

Only HR, Manager, or Admin can approve leave requests.
```

---