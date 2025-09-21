import streamlit as st
from crewai import Crew
from tasks import data_fetching_task, matching_task, response_generation_task
from agents import data_fetch_expert, matching_expert, response_expert
import sys
import sqlite3


# Custom CSS for Styling
st.markdown("""
    <style>
    /* Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #6a0dad, #9b30ff, #d8b4fe);
        color: #fff;
    }
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #4b0082;
        color: white;
    }
    /* Form Card */
    .stForm {
        background: white;
        color: black;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
    }
    /* Form Labels */
    label, .stTextInput label, .stNumberInput label, .stSelectbox label, .stCheckbox label {
        color: black !important;
        font-weight: 600 !important;
    }
            
    /* Input Fields */
    input, textarea {
        background-color: #1e1e1e !important; /* black */
        color: white !important; /* white text */
        border-radius: 8px !important;
        border: 1px solid #6a0dad !important;
        padding: 8px !important;
    }
    /* Checkbox label fix */
    div.stCheckbox label {
        color: white !important;
    }
            
    /* Dropdown options */
    div[data-baseweb="select"] > div {
        background-color: #1e1e1e !important;
        color: white !important;
    }
    /* Placeholder */
    input::placeholder {
        color: #cccccc !important;
    }
    /* Titles */
    h1, h2, h3 {
        color: #4b0082;
    }
    </style>
""", unsafe_allow_html=True)


# Sidebar Selector

st.sidebar.title("Select Your Role")
user_role = st.sidebar.radio("Are you a:", ["Landing Page", "Student", "Researcher", "Startup Founder"])

# Landing Page

if user_role == "Landing Page":
    st.title("🎓 Opportunities Finder")
    st.subheader("About the Opportunities Finder")
    st.write("""
    The **Opportunities Finder** helps students, researchers, and startup founders discover the best scholarships, 
    research opportunities, and funding programs tailored to their profile.  

     **How it works:**  
    - If you are a **Student**, provide your academic background and aspirations to find scholarships.  
    - If you are a **Researcher**, provide your expertise and field to find research grants. 
    - If you are a **Startup Founder**, share your startup info to find funding opportunities.
    """)
    st.info(" Use the sidebar to navigate to your role form.")


# Student Form

elif user_role == "Student":
    st.header("Student Scholarship Form")

    with st.form("student_form"):
        age = st.number_input("Your Age", min_value=15, max_value=60)
        country = st.text_input("Country of Citizenship/Residency", "Pakistan")

        degree_completed = st.selectbox("Degree Completed", [ "Master's","Bachelor's","High School/Intermediate"])

        # ✅ Conditional inputs (appear immediately)
        cgpa, percentage = None, None
        if degree_completed == "High School/Intermediate":
            percentage = st.number_input("Percentage (%)", min_value=0.0, max_value=100.0, step=0.1)
        else:
            cgpa = st.number_input("CGPA", min_value=0.0, max_value=4.0, step=0.1)

        prev_field = st.text_input("Previous Field of Study", "Computer Science")
        degree_applying = st.selectbox("Degree Applying For", ["Undergraduate", "Masters", "PhD"])
        target_field = st.text_input("Target Field", "Computer Science")

        submitted = st.form_submit_button("Find Scholarships")

    if submitted:
        # Step 1: Data Fetcher
        url = "https://www.mastersportal.com/"
        fetch_task = data_fetching_task(data_fetch_expert, url)
        crew1 = Crew(agents=[data_fetch_expert], tasks=[fetch_task])
        scholarships = crew1.kickoff()

        # Step 2: Matching
        student_profile = {
            "age": age,
            "country": country,
            "degree_completed": degree_completed,
            "percentage": percentage,
            "cgpa": cgpa,
            "prev_field": prev_field,
            "degree_applying": degree_applying,
            "target_field": target_field
        }

        match_task = matching_task(matching_expert, student_profile, scholarships)
        crew2 = Crew(agents=[matching_expert], tasks=[match_task])
        matched_results = crew2.kickoff()

        st.subheader("Matched Scholarships")
        st.json(matched_results)
        st.session_state["matched"] = matched_results

    if "matched" in st.session_state:
        if st.button("📄 Generate Report"):
            response_task = response_generation_task(response_expert, st.session_state["matched"])
            crew3 = Crew(agents=[response_expert], tasks=[response_task])
            result = crew3.kickoff()

            if hasattr(result, "raw"):
                report_text = result.raw
            elif hasattr(result, "outputs"):
                report_text = str(result.outputs)
            else:
                report_text = str(result)

            st.markdown(report_text)
            st.download_button("⬇ Download Report", data=report_text, file_name="scholarships_report.md", mime="text/markdown")


#  Researcher Form

elif user_role == "Researcher":
    st.header("Researcher Grant Finder")
    with st.form("research_form"):
        country = st.text_input("Country of Residence", "Pakistan")
        field = st.text_input("Research Area/Field", "Artificial Intelligence")
        proposal = st.text_area("Research Proposal / Idea Summary")
        position = st.text_input("Current Academic/Job Position", "PhD Student")
        submitted = st.form_submit_button("Find Research Opportunities")

    if submitted:
        st.success(" Researcher opportunities module coming soon!")


#  Startup Founder Form

elif user_role == "Startup Founder":
    st.header("Startup Funding Finder")
    with st.form("startup_form"):
        country = st.text_input("Country of Operation", "Pakistan")
        startup_name = st.text_input("Startup Name")
        industry = st.text_input("Industry/Domain", "FinTech")
        stage = st.selectbox("Stage", ["Idea", "Prototype", "Revenue", "Scaling"])
        funding_req = st.number_input("Funding Requirement ($)", min_value=0, step=1000)
        pitch = st.text_area("Short Pitch / Startup Description")
        submitted = st.form_submit_button(" Find Funding Opportunities")

    if submitted:
        st.success(" Startup funding opportunities module coming soon!")
