# Enterprise Policy Assistant

## Project Overview

Enterprise Policy Assistant is a Multi-Agent AI system designed to help employees, managers, and HR teams interact with company policies, employee information, and leave management processes through natural language queries.

The system combines:

- Multi-Agent Architecture
- Retrieval-Augmented Generation (RAG)
- ChromaDB Vector Database
- Streamlit Frontend
- MySQL Database
- Role-Based Access Control (RBAC)

---

## Business Problem

Organizations often store policies, employee information, and leave records across multiple systems.

Employees frequently ask questions such as:

- What is the leave carry forward policy?
- How many earned leaves do I have left?
- Show my profile.
- Apply leave for next week.
- Approve leave request 15.

Manually handling these requests increases HR workload.

---

## Solution

Enterprise Policy Assistant provides a centralized AI-powered platform that:

- Retrieves company policies using RAG
- Provides employee information
- Handles leave requests
- Supports leave approvals and rejections
- Maintains audit logs
- Enforces role-based permissions

---

## Core Features

### Employee Features

- View profile
- View leave balance
- Submit leave requests
- View leave history

### HR & Manager Features

- Approve leave requests
- Reject leave requests
- View employee leave information

### Policy Features

- Policy question answering
- Semantic search using ChromaDB
- Context-aware responses

### Security Features

- Authentication
- Role-based authorization
- Audit logging

---

## Technology Stack

### Frontend

- Streamlit

### Backend

- Python
- SQLAlchemy

### Database

- MySQL

### AI & RAG

- Sentence Transformers
- ChromaDB
- Mistral LLM

### Security

- bcrypt
- RBAC

---