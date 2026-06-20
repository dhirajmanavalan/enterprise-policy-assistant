# Railway Operations Guide - Enterprise Policy Assistant

This document contains all operational commands required to monitor, troubleshoot, and maintain the deployed Enterprise Policy Assistant on Railway.

---

# 1. Open Railway Console

Navigate to:

```text
Railway Project
→ Enterprise Policy Assistant
→ Service
→ Deployments
→ Open Console
```

---

# 2. Check Database Connection

Enter Python:

```bash
python
```

Run:

```python
from db.session import engine
print(engine)
```

Expected:

```text
Engine(mysql+pymysql://root:***@mysql.railway.internal:3306/railway)
```

Exit Python:

```python
exit()
```

---

# 3. Check Total Users

```bash
python
```

```python
from db.session import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM users"))
    print(result.scalar())
```

Expected:

```text
10
```

---

# 4. Show All Users

```python
from db.session import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(
        text("SELECT id, username, role FROM users")
    )

    for row in result:
        print(row)
```

---

# 5. Check Audit Logs

Latest 10 audit logs:

```python
from db.session import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(
        text("""
        SELECT id,
               username,
               query_type,
               raw_query
        FROM audit_logs
        ORDER BY id DESC
        LIMIT 10
        """)
    )

    for row in result:
        print(row)
```

---

# 6. Count Audit Logs

```python
from db.session import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(
        text("SELECT COUNT(*) FROM audit_logs")
    )

    print(result.scalar())
```

---

# 7. View All Leave Requests

```python
from db.session import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(
        text("""
        SELECT id,
               employee_id,
               leave_type,
               status,
               start_date,
               end_date
        FROM leave_requests
        ORDER BY id DESC
        """)
    )

    for row in result:
        print(row)
```

---

# 8. View Pending Leave Requests

Most useful command during demos and testing.

```python
from db.session import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(
        text("""
        SELECT id,
               employee_id,
               leave_type,
               start_date,
               end_date,
               status
        FROM leave_requests
        WHERE status='pending'
        """)
    )

    for row in result:
        print(row)
```

---

# 9. View Approved Leave Requests

```python
from db.session import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(
        text("""
        SELECT *
        FROM leave_requests
        WHERE status='approved'
        """)
    )

    for row in result:
        print(row)
```

---

# 10. View Rejected Leave Requests

```python
from db.session import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(
        text("""
        SELECT *
        FROM leave_requests
        WHERE status='rejected'
        """)
    )

    for row in result:
        print(row)
```

---

# 11. Check Employee Leave Balances

```python
from db.session import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(
        text("""
        SELECT employee_id,
               casual_leave_total,
               casual_leave_used,
               sick_leave_total,
               sick_leave_used,
               earned_leave_total,
               earned_leave_used
        FROM leave_balances
        """)
    )

    for row in result:
        print(row)
```

---

# 12. Check ChromaDB Vector Count

```python
from rag.vector_store import get_or_create_collection

collection = get_or_create_collection()

print(collection.count())
```

Expected:

```text
> 0
```

If count is 0, re-run ingestion.

---

# 13. Rebuild RAG Embeddings

Run whenever policy retrieval stops working.

```bash
python -m rag.ingest
```

Expected:

```text
[INGEST] Starting policy ingestion...
[PIPELINE] Starting document ingestion pipeline...
[VECTOR STORE] Stored XX chunks in ChromaDB
[INGEST] Policy ingestion finished.
```

---

# 14. Test RAG Directly

```python
from rag.pipeline import query_rag

print(
    query_rag(
        "What is the leave carry forward policy?"
    )
)
```

---

# 15. Seed Database Again

Use only when Railway database becomes empty.

```python
from db.seed_data import run_all_seeds

run_all_seeds()
```

---

# 16. Verify Deployment Health

Check Railway logs:

```text
Railway
→ Service
→ Deployments
→ View Logs
```

Healthy deployment:

```text
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8080
Network URL: http://0.0.0.0:8080
```

---

# Demo Test Accounts

## Employee

```text
Username: dhiru_offl
Password: Dhi@123
```

## Manager

```text
Username: madhu.mitha
Password: Madhu@123
```

## HR

```text
Username: nagendra.enukolu
Password: Nagendra@123
```

---

# Emergency Recovery Checklist

## Check User Count

```python
from db.session import engine
from sqlalchemy import text

with engine.connect() as conn:
    print(
        conn.execute(
            text("SELECT COUNT(*) FROM users")
        ).scalar()
    )
```

## Check Audit Count

```python
from db.session import engine
from sqlalchemy import text

with engine.connect() as conn:
    print(
        conn.execute(
            text("SELECT COUNT(*) FROM audit_logs")
        ).scalar()
    )
```

## Check Leave Requests

```python
from db.session import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(
        text("SELECT * FROM leave_requests")
    )

    for row in result:
        print(row)
```

## Rebuild RAG

```bash
python -m rag.ingest
```

## Reseed Database

```python
from db.seed_data import run_all_seeds

run_all_seeds()
```

---

# Recommended Git Commit

```bash
git add docs/railway.md
git commit -m "docs: add railway operations and troubleshooting guide"
git push origin main
```

This document serves as the operational handbook for deployment verification, database monitoring, RAG troubleshooting, audit tracking, and demo support.