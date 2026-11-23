import streamlit as st
import pandas as pd
import re
import time

# ==========================================
# 1. DATA LAYER (Systems Programming: Abstraction)
# ==========================================
class Database:
    """Encapsulates the data (Advanced Programming 3.5.1)"""
    def __init__(self):
        self.ownership_records = {
            "tegeta": {
                "name": "Tegeta Exploration & Resources / Sahara",
                "desc": "Heavily linked to state capture networks, coal supply prepayments, and non-delivery.",
                "owner": "Gupta Family Network (95%)",
                "pep": "Yes (Direct executive alignment)",
                "risk": "HIGH RISK"
            },
            "bosasa": {
                "name": "Bosasa (African Global Operations)",
                "desc": "Implicated in systemic state capture bribery and correctional services tender fraud.",
                "owner": "Gavin Watson Estate & Associates",
                "pep": "Yes (Extensive political patronage network)",
                "risk": "HIGH RISK"
            },
            "mckinsey": {
                "name": "McKinsey & Company & Trillian",
                "desc": "Consulting agreements set aside; funds exceeding R1 billion repaid.",
                "owner": "Global Partnership / Trillian Capital",
                "pep": "Under Review",
                "risk": "MEDIUM RISK"
            }
        }
        
        # Converting the HTML table into a Pandas DataFrame
        self.tenders_df = pd.DataFrame([
            {"Title": "Transnet 1,064 Locomotive Procurement", "Department": "Transnet", "Company": "CSR, CNR, Bombardier", "Amount": "R 54.5 Billion", "Status": "Set Aside"},
            {"Title": "Estina Dairy Farm Project", "Department": "Agriculture", "Company": "Estina (Pty) Ltd", "Amount": "R 280 Million", "Status": "Cancelled"},
            {"Title": "Eskom Management Consulting", "Department": "Eskom", "Company": "McKinsey & Trillian", "Amount": "R 1.6 Billion", "Status": "Funds Recovered"},
            {"Title": "SABC Security & IT Systems", "Department": "State Owned", "Company": "Infobala / LornaVision", "Amount": "R 185 Million", "Status": "Cancelled"},
            {"Title": "Digital Vibes Communications", "Department": "Health", "Company": "Digital Vibes", "Amount": "R 150 Million", "Status": "Declared Invalid"}
        ])

    def get_company(self, query):
        for key, data in self.ownership_records.items():
            if key in query.lower():
                return data
        return None

# ==========================================
# 2. SERVICE LAYER (Advanced Programming: Patterns)
# ==========================================

class AIService:
    """Uses the Strategy Pattern (Advanced Programming 3.5.1) to handle chatbot queries."""
    def __init__(self):
        self.strategies = [
            (r"history|about", self._handle_history),
            (r"tender|search", self._handle_navigation),
            (r"ownership|company|unmask", self._handle_navigation),
            (r"popia|law|legal", self._handle_legal)
        ]

    def get_response(self, query):
        for pattern, handler in self.strategies:
            if re.search(pattern, query, re.IGNORECASE):
                return handler(query)
        return "I can help you explore the Tender Tracker or explain legal terms. What would you like to know?"

    def _handle_history(self, query):
        return "This platform is a public-interest transparency concept in response to public procurement information being scattered. It brings tender records and ownership info together."

    def _handle_navigation(self, query):
        if "tender" in query.lower():
            return "You can search tenders by navigating to the **Tender Tracker** tab on the left sidebar."
        return "Head over to the **Beneficial Ownership** tab on the left to check shell companies and PEP links."

    def _handle_legal(self, query):
        return "POPIA is South Africa’s Protection of Personal Information Act. It regulates how organizations collect, use, and store personal information."

class OwnershipService:
    """Uses Composition (Advanced Programming 3.5.1) to combine Database and UI logic."""
    def __init__(self, database):
        self.db = database

    def search(self, query):
        return self.db.get_company(query)

# ==========================================
# 3. PRESENTATION LAYER (Streamlit UI)
# ==========================================

# Page Configuration
st.set_page_config(page_title="Madlanga Platform", page_icon="⚖️", layout="wide")

# Custom CSS to mimic the Tailwind design AND fix grey text globally
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    
    /* Hero Banner */
    .hero { background: linear-gradient(135deg, #0f172a 0%, #7f1d1d 100%); color: white; padding: 40px; border-radius: 10px; text-align: center; margin-bottom: 20px; }
    .hero h1 { color: white !important; }
    
    /* Ownership Risk Cards */
    .high-risk { background-color: #fee2e2; border-left: 5px solid #dc2626; padding: 15px; border-radius: 5px; margin-bottom: 15px; }
    .medium-risk { background-color: #fef3c7; border-left: 5px solid #d97706; padding: 15px; border-radius: 5px; margin-bottom: 15px; }
    
    /* --- GLOBAL TEXT FIXES --- */
    /* Force standard text paragraphs to be dark */
    .stMarkdown p, .stText, .stMarkdown li {
        color: #1e293b !important; 
        font-size: 16px;
    }
    
    /* Force all headers to be dark navy */
    h1, h2, h3, h4, h5, h6 {
        color: #0f172a !important; 
    }
    
    /* Force input labels to be dark */
    label {
        color: #0f172a !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Services (Dependency Injection)
@st.cache_resource
def init_services():
    db = Database()
    ai = AIService()
    ownership = OwnershipService(db)
    return db, ai, ownership

db, ai_service, ownership_service = init_services()

# Sidebar Navigation
st.sidebar.title("⚖️ Madlanga Platform")
st.sidebar.markdown("Tender Transparency & Accountability")
st.sidebar.warning("⚠️ Prototype demonstration only. Data is illustrative.")

page = st.sidebar.radio("Navigate to:", ["Home", "Tender Tracker", "Beneficial Ownership", "Whistleblower"])

# ==========================================
# PAGE ROUTING
# ==========================================

if page == "Home":
    st.markdown("""
        <div class="hero">
            <h1>Holding Officials Accountable, Restoring Trust.</h1>
            <p>Taxpayers and ordinary citizens now have a centralized platform to easily verify who is awarded government tenders and track commission recommendations.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Brief History & Project Context")
    st.write("""
        Ordinary South Africans pay taxes but for too long have been unable to see where their money goes. 
        Tender notices have historically been scattered across disconnected government websites, and real corporate owners 
        have hidden behind complex shell companies and fronting.
    """)

elif page == "Tender Tracker":
    st.title("🔍 Central Searchable Tender Tracker")
    st.write("Track major public procurement and Madlanga Commission examined tenders.")
    
    # Search and Filter
    col1, col2 = st.columns(2)
    with col1:
        search_query = st.text_input("Search Tender / Entity", placeholder="e.g. Transnet, Eskom...")
    with col2:
        dept_filter = st.selectbox("Department / Sector", ["All"] + list(db.tenders_df['Department'].unique()))
    
    # Filter logic
    filtered_df = db.tenders_df
    if search_query:
        filtered_df = filtered_df[filtered_df.apply(lambda row: search_query.lower() in str(row).lower(), axis=1)]
    if dept_filter != "All":
        filtered_df = filtered_df[filtered_df['Department'] == dept_filter]
        
    st.info(f"Showing {len(filtered_df)} results")
    
    # Display Table
    st.dataframe(filtered_df, use_container_width=True)

elif page == "Beneficial Ownership":
    st.title("🏢 Beneficial Ownership Public Register")
    st.write("Unmask shell companies, fronting entities, and politically connected directors.")
    
    # Search Interface
    query = st.text_input("Search company name (e.g. Tegeta, Bosasa, McKinsey):")
    
    if query:
        result = ownership_service.search(query)
        
        if result:
            if result['risk'] == "HIGH RISK":
                st.markdown(f"""
                    <div class="high-risk">
                        <h3>Company Record: {result['name']}</h3>
                        <p>{result['desc']}</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="medium-risk">
                        <h3>Company Record: {result['name']}</h3>
                        <p>{result['desc']}</p>
                    </div>
                """, unsafe_allow_html=True)
                
            st.write(f"**Ultimate Beneficial Owner:** {result['owner']}")
            st.write(f"**PEP Link:** {result['pep']}")
        else:
            st.warning(f"No high-risk shell indicators found for: '{query}'. Company record is pending full disclosure audit.")

elif page == "Whistleblower":
    st.title("🛡️ Whistleblower Protection & Secure Portal")
    st.write("Submit anonymous reports on tender corruption.")
    
    with st.form("whistleblower_form"):
        st.selectbox("Target Department / State Entity", ["Transnet SOC Ltd", "Eskom Holdings", "PRASA", "Other"])
        st.selectbox("Type of Irregularity", ["Tender Fraud", "Inflated Invoicing", "Fronting", "Bribery"])
        desc = st.text_area("Detailed Description of Corruption")
        
        uploaded_file = st.file_uploader("Upload Evidence Document (POPIA Compliance Shield)", type=["pdf", "png", "jpg"])
        
        consent = st.checkbox("I understand this report is submitted anonymously under POPIA compliance rules.")
        
        submit = st.form_submit_button("Submit Encrypted Report")
        
        if submit:
            if not desc or not consent:
                st.error("Please provide a description and agree to the terms.")
            else:
                with st.spinner("Encrypting and transmitting..."):
                    time.sleep(1.5) # Simulate network delay
                st.success("Report Securely Encrypted & Submitted!")
                st.info(f"Your anonymous tracking token is: **TOK-{pd.Timestamp.now().strftime('%M%S')}-2026**")

# ==========================================
# FLOATING AI CHATBOT (Moved to Sidebar for Streamlit)
# ==========================================
with st.sidebar.expander("🤖 AI Navigator Chatbot", expanded=False):
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello! I am your AI Guide. Ask me about this platform or legal terms."}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        response = ai_service.get_response(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        