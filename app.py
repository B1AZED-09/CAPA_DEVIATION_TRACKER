import streamlit as st
import sqlite3
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# --- 1. DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('deviations.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS deviations 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  date TEXT,
                  batch TEXT,
                  severity TEXT,
                  description TEXT,
                  root_cause TEXT,
                  corrective_action TEXT,
                  preventive_action TEXT,
                  status TEXT DEFAULT 'Open')''')
    conn.commit()
    return conn

conn = init_db()

# --- 2. AUTHENTICATION CONFIG ---
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"

def login():
    st.title("🔐 GMP Systems Login")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    
    if st.button("Sign In"):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Invalid credentials. Access denied.")

def logout():
    st.session_state["authenticated"] = False
    st.rerun()

# --- 3. SESSION CHECKS ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# --- 4. MAIN APP (If logged in) ---
if st.session_state["authenticated"]:
    st.set_page_config(page_title="GMP Deviation Tracker", layout="wide")
    st.sidebar.header("Navigation")
    st.sidebar.button("🚪 Logout", on_click=logout, type="primary")
    st.sidebar.markdown("**Logged in as:** admin")
    
    mode = st.sidebar.radio("Go to", ["New Deviation", "Dashboard", "PDF Generator"])

    # --- NEW DEVIATION FORM ---
    if mode == "New Deviation":
        st.header("Log a New Deviation")
        col1, col2 = st.columns(2)
        with col1:
            batch = st.text_input("Batch Number", placeholder="e.g., BATCH-2026-001")
            severity = st.selectbox("Severity", ["Critical", "Major", "Minor"])
        with col2:
            date = st.date_input("Date", datetime.now())
        
        description = st.text_area("Description of Deviation")
        root_cause = st.text_area("Root Cause (5 Whys)")
        c_action = st.text_area("Corrective Action (Fix it now)")
        p_action = st.text_area("Preventive Action (Stop it happening again)")
        
        if st.button("Submit Deviation"):
            if batch and description:
                c = conn.cursor()
                c.execute("INSERT INTO deviations (date, batch, severity, description, root_cause, corrective_action, preventive_action) VALUES (?, ?, ?, ?, ?, ?, ?)",
                          (str(date), batch, severity, description, root_cause, c_action, p_action))
                conn.commit()
                st.success("Deviation logged successfully!")
            else:
                st.error("Batch and Description are required.")

    # --- DASHBOARD ---
    elif mode == "Dashboard":
        st.header("Active Deviations")
        c = conn.cursor()
        c.execute("SELECT * FROM deviations WHERE status != 'Closed'")
        rows = c.fetchall()
        if rows:
            st.table(rows)
        else:
            st.info("No active deviations.")

    # --- PDF GENERATOR ---
    elif mode == "PDF Generator":
        st.header("Generate Audit-Ready Report")
        dev_id = st.number_input("Enter Deviation ID", min_value=1)
        
        if st.button("Download PDF"):
            c = conn.cursor()
            c.execute("SELECT * FROM deviations WHERE id=?", (dev_id,))
            row = c.fetchone()
            
            if row:
                buffer = io.BytesIO()
                pdf = canvas.Canvas(buffer, pagesize=letter)
                width, height = letter
                
                pdf.setFont("Helvetica-Bold", 16)
                pdf.drawString(100, height - 100, "GMP DEVIATION & CAPA REPORT")
                pdf.setFont("Helvetica", 12)
                pdf.drawString(100, height - 120, f"ID: {row[0]} | Date: {row[1]}")
                
                y = height - 160
                pdf.drawString(100, y, "Batch Affected:")
                pdf.drawString(250, y, row[2])
                
                y -= 20
                pdf.drawString(100, y, "Severity:")
                pdf.drawString(250, y, row[3])
                
                y -= 20
                pdf.drawString(100, y, "Description:")
                pdf.drawString(250, y, row[4])
                
                y -= 40
                pdf.drawString(100, y, "Root Cause Analysis:")
                y -= 20
                pdf.drawString(100, y, row[5])
                
                y -= 40
                pdf.drawString(100, y, "Corrective Action:")
                y -= 20
                pdf.drawString(100, y, row[6])
                
                y -= 40
                pdf.drawString(100, y, "Preventive Action:")
                y -= 20
                pdf.drawString(100, y, row[7])
                
                pdf.line(100, 100, width - 100, 100)
                pdf.drawString(100, 80, "Authorized by: ________________________")
                
                pdf.save()
                buffer.seek(0)
                st.download_button(label="Download PDF Report", data=buffer, file_name=f"DEV-{dev_id}.pdf", mime="application/pdf")
            else:
                st.error("Deviation ID not found.")

# --- 5. LOGIN SCREEN (If not authenticated) ---
else:
    login()