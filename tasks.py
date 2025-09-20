from crewai import Task

def data_fetching_task(agent, url):
    return Task(
        description=f"""
        Scrape and fetch scholarship opportunities from the website: {url}.
        Extract each opportunity with:
        - title
        - type (Scholarship, Fellowship, Internship, Grant, etc.)
        - eligibility
        - requirements
        - coverage
        - deadline
        - location
        - url

        Return the result in JSON array format (not markdown).
        """,
        expected_output="A structured JSON array of scholarships with all details.",
        agent=agent,
        output_file=None 
    )


def matching_task(agent, student_profile, scholarships):
    return Task(
        description=f"""
        Match the following student profile to the available scholarships.

        Student Profile: {student_profile}  
        Scholarships Data: {scholarships}  

        Compare eligibility, GPA, financial need, and field of study.  
        Rank the scholarships with:
        - title
        - match_score (0-1)
        - reason (why matched)

        Return output in JSON format:
        {{
            "student_profile": ...,
            "matched_opportunities": [...]
        }}
        """,
        expected_output="A JSON object containing student profile and ranked matched scholarships.",
        agent=agent,
        output_file=None  # Only show in UI as Markdown, no file
    )


def response_generation_task(agent, matched_scholarships):
    return Task(
        description=f"""
        Generate a personalized, student-friendly response based on these matched scholarships:

        {matched_scholarships}

        Format response in Markdown with:
        - Scholarship name + location
        - Why it is a good fit (based on GPA, financial need, field)
        - Benefits (coverage, stipend, travel support, etc.)
        - Deadline
        - Application link
        - A final recommendation

        Make the tone encouraging and clear for students.
        """,
        expected_output="A well-written markdown response listing scholarships with reasons and recommendations.",
        agent=agent,
        output_file="schlorships_report.md"  # Saves to file + can download
    )
