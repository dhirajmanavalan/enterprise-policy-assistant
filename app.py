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
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
}

[data-testid="stSidebar"] {
    background-color: #1E1E2F;
}

h1 {
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.title("🔐 Login")

    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    st.markdown("---")

    st.subheader("💡 Sample Queries")

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

    st.subheader("⚙️ Available Features")

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

st.title("🏢 Enterprise Policy Assistant")

st.markdown(
    "Ask policy, leave, employee, or HR-related questions."
)

st.markdown("---")

# ---------------------------------------------------
# QUERY INPUT
# ---------------------------------------------------

query = st.text_area(
    "💬 Ask your question",
    height=120
)

# ---------------------------------------------------
# SUBMIT BUTTON
# ---------------------------------------------------

if st.button("🚀 Submit", use_container_width=True):

    if not username or not password or not query:

        st.warning(
            "Please enter username, password, and query."
        )

    else:

        with st.spinner("Processing request..."):

            orchestrator = EnterpriseAssistantOrchestrator()

            result = orchestrator.handle_request(
                username=username,
                password=password,
                user_query=query
            )

        # -------------------------------------------
        # SUCCESS / ERROR
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

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Employee ID",
                    user.get("employee_id")
                )

            with col2:
                st.metric(
                    "Role",
                    user.get("role", "").title()
                )

            with col3:
                st.metric(
                    "Department",
                    user.get("department")
                )

            with col4:
                st.metric(
                    "Username",
                    user.get("username")
                )

            st.info(
                f"""
**Full Name:** {user.get('full_name', 'N/A')}

**Designation:** {user.get('designation', 'N/A')}

**Email:** {user.get('email', 'N/A')}
"""
            )

        st.markdown("---")

        # -------------------------------------------
        # QUERY DETAILS
        # -------------------------------------------

        st.subheader("🤖 Query Details")

        col1, col2 = st.columns(2)

        with col1:
            st.info(
                f"**Query Type:** {result.get('query_type')}"
            )

        with col2:
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

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Audit Log ID",
                    audit.get("audit_log_id")
                )

            with col2:
                st.metric(
                    "Query ID",
                    audit.get("query_id")
                )