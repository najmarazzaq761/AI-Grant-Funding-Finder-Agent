# 🎓 AI Grant & Scholarship Finder Agent

An AI-powered application that helps **students**, **researchers**, and **startup founders** discover relevant **scholarships, grants, fellowships, and funding opportunities** tailored to their profile.  

Built with **CrewAI + Streamlit**, this tool scrapes opportunities from trusted sources, matches them with the user’s background, and generates a **personalized recommendation report**.

---

## 🚀 Features

- 🧑‍🎓 **For Students**: Find scholarships based on age, country, academic background, GPA/percentage, financial need, and field of study.  
- 🔬 **For Researchers**: (Coming Soon) Discover grants and fellowships by providing research field, country, and project idea.  
- 💡 **For Startup Founders**: (Coming Soon) Explore startup funding opportunities by sharing details about your venture, stage, and funding needs.  
- 📊 **Smart Matching**: AI matches opportunities against your profile (eligibility, CGPA, financial needs, etc.).  
- 📝 **Detailed Reports**: Generates a personalized markdown report with scholarship details, deadlines, and application links.  

---

## 🖼️ UI Preview

- Custom **Streamlit UI** with a modern **purple gradient theme**.  
- Sidebar role selection (Student | Researcher | Startup Founder).  
- Clean input forms with conditional logic (CGPA vs Percentage, etc.).  

---

## ⚙️ Tech Stack

- [Python 3.10+](https://www.python.org/)  
- [Streamlit](https://streamlit.io/) – Frontend UI  
- [CrewAI](https://github.com/joaomdmoura/crewAI) – Multi-agent orchestration  
- [LangChain](https://www.langchain.com/) – Document loading & embeddings  
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) – Web scraping  
- [FAISS](https://github.com/facebookresearch/faiss) – Vector storage & retrieval  

---

## 📂 Project Structure

```

AI-Grant-Funding-Finder-Agent/
│
├── agents.py                # AI agent definitions (data fetcher, matcher, responder)
├── tasks.py                 # Agent task descriptions
├── frontend.py              # Streamlit UI
├── utils/                   # Utility scripts (scrapers, embeddings, etc.)
├── requirements.txt         # Dependencies
└── README.md                # Project documentation

````

---

## ▶️ How to Run

1. **Clone the Repository**
   ```bash
   git clone https://github.com/najmarazzaq761/AI-Grant-Funding-Finder-Agent.git
   cd AI-Grant-Funding-Finder-Agent
