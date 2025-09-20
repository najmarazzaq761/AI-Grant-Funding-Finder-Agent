import streamlit as st
from crewai import Crew
from tasks import data_fetching_task, matching_task, response_generation_task
from agents import data_fetch_expert, matching_expert, response_expert


# Streamlit UI
st.title("🎓Scholarship Finder")

url = "https://www.mastersportal.com/"

with st.form("student_form"):
    age = st.number_input("Your Age")
    country= st.text_input("Country", "Pakistan")
    degree_level = st.selectbox("Degree Level", ["Undergraduate", "Masters", "PhD"])
    field_of_study = st.text_input("Field of Study", "Computer Science")
    cgpa = st.number_input("CGPA", min_value=0.0, max_value=4.0, step=0.1)
    financial_need = st.checkbox("Financial Need")
    submitted = st.form_submit_button("Find Scholarships")

if submitted:
    
    # Step 1: Run Agent 1 (Data Fetcher)

    fetch_task = data_fetching_task(data_fetch_expert, url)
    crew1 = Crew(agents=[data_fetch_expert], tasks=[fetch_task])
    scholarships = crew1.kickoff()

    
    # Step 2: Run Agent 2 (Matcher) and show results
    
    student_profile = {
        "age": age,
        "country": country,
        "degree_level": degree_level,
        "field_of_study": field_of_study,
        "cgpa": cgpa,
        "financial_need": financial_need
    }

    match_task = matching_task(matching_expert, student_profile, scholarships)
    crew2 = Crew(agents=[matching_expert], tasks=[match_task])
    matched_results = crew2.kickoff()

    st.subheader("Matched Scholarships")
    st.json(matched_results)  # formatted json results

    # Store for later use
    st.session_state["matched"] = matched_results



# Step 3: Agent 3 (Response Generator on button click)

if "matched" in st.session_state:
    if st.button("📄 Generate Report"):
        response_task = response_generation_task(response_expert, st.session_state["matched"])
        crew3 = Crew(agents=[response_expert], tasks=[response_task])
        # Run crew
        result = crew3.kickoff()

        # Extract markdown text (adjust depending on what your Crew returns)
        if hasattr(result, "raw"):
            report_text = result.raw
        elif hasattr(result, "outputs"):
            report_text = str(result.outputs)
        else:
            report_text = str(result)  # fallback

        # Show in Streamlit
        st.markdown(report_text)

        # Download button
        st.download_button(
            label="⬇ Download Report",
            data=report_text,
            file_name="schlorships_report.md",
            mime="text/markdown"
        )

