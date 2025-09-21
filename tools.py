import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from crewai.tools import tool
import streamlit as st
import sys
import sqlite3


@st.cache_data
def fetch_all_links(base_url):
    """Fetch all internal links from the website's base URL."""
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = set()

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        from urllib.parse import urljoin

        if href.startswith("/"):  
            links.add(urljoin(base_url, href))
        elif base_url in href: 
            links.add(href)

    return list(links)


@st.cache_data
def load_data(base_url="https://www.mastersportal.com/"):
    """Load data from all pages of the website."""
    all_links = fetch_all_links(base_url)
    all_data = []
    for link in all_links:
        try:
            loader = WebBaseLoader([link])
            all_data.extend(loader.load())
        except Exception as e:
            st.warning(f"Failed to load data from {link}: {e}")
    return all_data


@st.cache_data
def split_data(_data):
    """Split data into chunks."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500)
    return text_splitter.split_documents(_data)


@st.cache_resource
def create_vector_store(_docs):
    """Create FAISS vector store."""
    if not _docs:
        return None
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )
    return FAISS.from_documents(documents=_docs, embedding=embeddings)


def scrape_and_embed(base_url="https://www.mastersportal.com/"):
    """Main function to scrape site and build vectorstore."""
    data = load_data(base_url)
    docs = split_data(data)
    vectorstore = create_vector_store(docs)
    return vectorstore



# Custom Tool for Agent

@tool("scholarship_scraper_tool")
def scholarship_scraper_tool(query: str):
    """
    Custom tool: scrapes MastersPortal and performs semantic search.
    """
    vectorstore = scrape_and_embed("https://www.mastersportal.com/")
    if vectorstore:
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
        results = retriever.get_relevant_documents(query)
        return "\n\n".join([doc.page_content for doc in results])
    else:
        return "No data could be retrieved."

