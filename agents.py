from crewai import Agent, LLM
from tools import scholarship_scraper_tool
from crewai import LLM
from dotenv import load_dotenv
import os
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm=LLM(
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
        base_url="https://api.groq.com/openai/v1",
        api_key=GROQ_API_KEY
    )


# Agent 1: Data Fetching
data_fetch_expert = Agent(
    role="Scholarship Data Collection Expert",
    goal="Scrape and structure scholarship opportunities from websites.",
    backstory="An expert researcher who knows how to collect and extract scholarship data.",
    tools=[scholarship_scraper_tool],
    llm=llm,
    allow_delegation=True,
)

# Agent 2: Matching
matching_expert = Agent(
    role="Scholarship Matching Expert",
    goal="Match student profiles to the most relevant scholarships.",
    backstory="An AI expert who analyzes profiles and finds the most suitable scholarships.",
    tools=[],
    llm=llm,
    verbose=True,
    allow_delegation=True,
)

# Agent 3: Response Generation
response_expert = Agent(
    role="Scholarship Response Generator",
    goal="Generate a student-friendly response based on matched scholarships.",
    backstory="A helpful advisor who explains scholarship opportunities clearly.",
    tools=[],
    llm=llm,
    allow_delegation=False,
)
