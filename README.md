# GitHub Issues Q&A Assistant

A Streamlit-based application that allows users to ask questions about GitHub issues using natural language. The application uses LangChain, OpenAI embeddings, and Qdrant vector store to provide intelligent responses based on the content of GitHub issues.

## Features

- Downloads and processes GitHub issues from a specified repository
- Stores issue content in a vector database (Qdrant) for efficient retrieval
- Provides a chat interface to ask questions about the issues
- Supports both open and closed issues
- Uses LangChain and OpenAI for intelligent question answering

## Prerequisites

- Python 3.9+
- Qdrant server running locally or remotely
- OpenAI API key
- GitHub Personal Access Token
- Required Python packages (see Installation section)

## Installation

1. Clone the repository:


2. Install required packages:

Required packages include:
- streamlit
- python-dotenv
- langchain
- langchain-openai
- qdrant-client
- PyGithub
- jupyter (for running notebooks)

3. Create a configuration file named `.7ytrepmnt` with the following environment variables:

env:README.md
OPENAI_API_KEY=your_openai_api_key
GITHUB_TOKEN=your_github_token
QDRANT_HOST_URL=your_qdrant_host_url


## Usage

### 1. Data Ingestion (Using Jupyter Notebook)

The `download-github-issues.ipynb` and `ingest-issues-to-qdrant.ipynb` notebooks contain code to:
- Download GitHub issues from a specified repository
- Process and split the issues into chunks
- Store the chunks in Qdrant vector store


### 2. Running the Q&A Assistant

Start the Streamlit application:
```bash
streamlit run gh-issues-qa-assistant.py
```

