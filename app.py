import streamlit as st
from agents.orchestrator.agent import EnterpriseAssistantOrchestrator

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Enterprise Policy Assistant",
    page_icon="🏢",
    layout="wide"
)

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background-color: #0F172A;
}

[data-testid="stSidebar"] {
    background-color: #1E293B;
}

.stButton button {
    background: linear-gradient(90deg,#2563EB,#7C3AED);
    color:white;
    border:none;
    border-radius:10px;
    font-weight:600;
}

.profile-card {
    background:#1E293B;
    padding:20px;
    border-radius:15px;
    color:white;
    margin-bottom:20px;
}

.metric-box {
    background:#1E293B;
    padding:15px;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
with st.expander("🎯 Demo Credentials"):

    st.code("""
Employee
Username: dhiru_offl
Password: Dhi@123

HR
Username: nagendra.enukolu
Password: Nagendra@123

Manager
Username: madhu.mitha
Password: Madhu@123
""")
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.title("🔐 Employee Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if not st.session_state.logged_in:

        if st.button("Login", use_container_width=True):

            try:

                orchestrator = EnterpriseAssistantOrchestrator()

                auth_result = (
                    orchestrator.authentication_agent.authenticate(
                        username,
                        password
                    )
                )

                if auth_result.get("authenticated"):

                    st.session_state.logged_in = True
                    st.session_state.user = auth_result["user"]

                    st.success("Login Successful")
                    st.rerun()

                else:
                    st.error("Invalid Username or Password")

            except Exception as e:
                st.error(str(e))

    if st.session_state.logged_in:

        st.success(
            f"Logged in as {st.session_state.user['username']}"
        )

        if st.button("Logout", use_container_width=True):

            st.session_state.logged_in = False
            st.session_state.user = None

            st.rerun()

        st.markdown("---")

        if st.checkbox("Show Sample Queries"):

            sample_queries = [
                "Show my profile",
                "Show my leave balance",
                "How many earned leave do I have left?",
                "Show my leave requests",
                "I want sick leave from 2026-06-19 to 2026-06-22",
                "What is the leave carry forward policy?",
                "Approve leave request 15",
                "Reject leave request 15",
                "What is the leave carry forward policy and show my profile"
            ]

            for query_hint in sample_queries:
                st.code(query_hint)

        st.markdown("---")

        st.subheader("⚙️ Features")

        st.markdown("""
        - Employee Profile
        - Leave Balance
        - Leave Requests
        - Leave Approval
        - Leave Rejection
        - Company Policies
        - Hybrid Queries
        - Audit Tracking
        """)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.markdown("""
<div style="
background:linear-gradient(90deg,#2563EB,#7C3AED);
padding:25px;
border-radius:15px;
text-align:center;
color:white;
margin-bottom:20px;
">
<h1>🏢 Enterprise Policy Assistant</h1>
<p>AI Powered HR & Policy Management Platform</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# DASHBOARD CARDS
# ---------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Policies", "4")

with col2:
    st.metric("Agents", "7")

with col3:
    st.metric("Status", "🟢 Active")

# ---------------------------------------------------
# LOGIN REQUIRED
# ---------------------------------------------------

if not st.session_state.logged_in:

    st.info(
        "Please login using your employee credentials to continue."
    )

    st.stop()

# ---------------------------------------------------
# USER PROFILE
# ---------------------------------------------------

user = st.session_state.user

st.markdown(f"""
<div class="profile-card">
<h3>👤 {user.get('full_name','N/A')}</h3>
<p><b>Role:</b> {user.get('role','N/A').title()}</p>
<p><b>Department:</b> {user.get('department','N/A')}</p>
<p><b>Employee ID:</b> {user.get('employee_id','N/A')}</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# AGENT FLOW
# ---------------------------------------------------

st.subheader("🤖 Multi-Agent Workflow")

graph = """
digraph {
Authentication -> QueryRouter
QueryRouter -> PolicyRAG
QueryRouter -> EmployeeData
QueryRouter -> LeaveRequest
QueryRouter -> LeaveApproval
PolicyRAG -> Response
EmployeeData -> Response
LeaveRequest -> Response
LeaveApproval -> Response
Response -> Audit
}
"""

st.graphviz_chart(graph)

# ---------------------------------------------------
# QUERY INPUT
# ---------------------------------------------------

query = st.text_area(
    "💬 Ask your question",
    height=120,
    placeholder="Ask about policies, leave, employee details..."
)

# ---------------------------------------------------
# SUBMIT
# ---------------------------------------------------

if st.button("🚀 Submit Request", use_container_width=True):

    if not query:

        st.warning("Please enter a query.")

    else:

        with st.spinner("Processing request..."):

            orchestrator = EnterpriseAssistantOrchestrator()

            result = orchestrator.handle_request(
                username=username,
                password=password,
                user_query=query
            )

        # -------------------------------------------
        # STATUS
        # -------------------------------------------

        if result.get("status") == "success":

            st.success(
                "Request Processed Successfully"
            )

        else:

            st.error(
                result.get(
                    "message",
                    "Request Failed"
                )
            )

        st.markdown("---")

        # -------------------------------------------
        # USER INFORMATION
        # -------------------------------------------

        if result.get("authenticated_user"):

            user = result["authenticated_user"]

            st.subheader("👤 Employee Information")

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                st.metric(
                    "Employee ID",
                    user.get("employee_id")
                )

            with c2:
                st.metric(
                    "Role",
                    user.get("role", "").title()
                )

            with c3:
                st.metric(
                    "Department",
                    user.get("department")
                )

            with c4:
                st.metric(
                    "Username",
                    user.get("username")
                )

            st.info(f"""
**Full Name:** {user.get('full_name', 'N/A')}

**Designation:** {user.get('designation', 'N/A')}

**Email:** {user.get('email', 'N/A')}
""")

        st.markdown("---")

        # -------------------------------------------
        # QUERY DETAILS
        # -------------------------------------------

        st.subheader("🤖 Query Details")

        c1, c2 = st.columns(2)

        with c1:
            st.info(
                f"**Query Type:** {result.get('query_type')}"
            )

        with c2:
            st.info(
                f"**Target Agents:** {result.get('target_agents')}"
            )

        st.markdown("---")

        # -------------------------------------------
        # FINAL RESPONSE
        # -------------------------------------------

        st.subheader("📄 Final Response")

        if result.get("response_result"):

            st.success(
                result["response_result"].get(
                    "final_response",
                    "No response generated"
                )
            )

        st.markdown("---")

        # -------------------------------------------
        # AGENT DETAILS
        # -------------------------------------------

        with st.expander("🔍 Agent Execution Details"):

            st.json(result)

        # -------------------------------------------
        # AUDIT DETAILS
        # -------------------------------------------

        if result.get("audit_result"):

            st.subheader("📋 Audit Information")

            audit = result["audit_result"]

            c1, c2 = st.columns(2)

            with c1:
                st.metric(
                    "Audit Log ID",
                    audit.get("audit_log_id")
                )

            with c2:
                st.metric(
                    "Query ID",
                    audit.get("query_id")
                )

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("---")

st.markdown("""
<div style="
text-align:center;
padding:20px;
border-radius:10px;
background-color:#1E293B;
color:white;
">

<h4>🚀 Developed By</h4>

<h3>DHIRAJKUMAR M</h3>

<p>
Software Developer | AI & Data Science Graduate
</p>

<p>
🔗 GitHub:
<a href="https://github.com/dhirajmanavalan/enterprise-policy-assistant" target="_blank">
Enterprise Policy Assistant
</a>
</p>

<p>
💼 LinkedIn:
<a href="https://www.linkedin.com/in/dhirajkumar-/" target="_blank">
Dhiraj Kumar
</a>
</p>

</div>
""", unsafe_allow_html=True)

st.info(
    "This application uses demo employee and policy data for demonstration purposes."
)

st.markdown("---")

st.caption(
    "Enterprise Policy Assistant • Multi-Agent AI Platform • Version 1.0"
)