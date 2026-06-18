# Setup Guide

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

Update database configuration:

```python
db/session.py
```

Provide:

- Host
- Username
- Password
- Database Name

---

## Create Database Tables

```bash
python setup_database.py
```

---

## Populate Policy Documents

```bash
python ingest_policies.py
```

---

## Run Console Application

```bash
python main.py
```

---

## Run Streamlit Frontend

```bash
streamlit run app.py
```

---

## Sample Users

### Employee

```text
Username : abidhi
Password : Abi@123
```

### HR

```text
Username : poorna
Password : Poorna@123
```

---

## Demo Queries

```text
Show my profile

Show my leave balance

Show my leave requests

How many earned leave do I have left?

I want sick leave from 2026-06-19 to 2026-06-22

Approve leave request 15

Reject leave request 15

What is the leave carry forward policy?

What is the leave carry forward policy and show my profile
```

---