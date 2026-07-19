# RAG PDF Chatbot

A Retrieval Augmented Generation (RAG) based chatbot that lets you upload any PDF and ask natural language questions about it.

## What it does
- Upload any PDF document through a web interface.
- Ask questions about the document in plain English.
- Get accurate, context-aware answers powered by an LLM.
- Validated with a factual Q&A benchmark achieving 83% accuracy.

## Tech Stack
- **Python** - core language
- **Flask** - web server and API routes
- **ChromaDB** - vector database for semantic search
- **Groq API** (llama-3.1-8b-instant) - LLM for answer generation
- **pypdf** - PDF text extraction

## How it works
1. User uploads a PDF → text is extracted and split into chunks
2. Chunks are stored in ChromaDB as vector embeddings
3. User asks a question → ChromaDB finds the 7 most relevant chunks via cosine similarity search
4. Relevant chunks + question are sent to Groq LLM
5. LLM generates a grounded answer based only on the document

## How to run locally

1. Clone the repo
git clone https://github.com/Soumyadip-CR3/Rag-pdf-chatbot.git

2. Install dependencies
pip install flask chromadb groq pypdf python-dotenv

3. Create a .env file and add your Groq API key
GROQ_API_KEY=your_groq_api_key_here
Get a free key at: https://console.groq.com

4. Run the app
python app.py

Then open your browser and go to http://127.0.0.1:5000

## Project Structure
app.py - Main Flask application
templates/index.html - Frontend interface
.gitignore - Excludes .env and cache files
README.md - Project documentation
