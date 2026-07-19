from flask import Flask, request, jsonify, render_template
from pypdf import PdfReader
import chromadb
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

chroma_client = chromadb.Client()
collection = None  # starts empty, gets filled when user uploads

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    global collection

    # Get the uploaded file
    file = request.files["pdf"]

    # Read and extract text
    reader = PdfReader(file)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text()

    # Chunk it
    chunk_size = 800
    chunks = [full_text[i:i+chunk_size].strip() 
              for i in range(0, len(full_text), chunk_size) 
              if len(full_text[i:i+chunk_size].strip()) > 50]

    # Reset ChromaDB collection
    try:
        chroma_client.delete_collection("user_docs")
    except:
        pass
    collection = chroma_client.create_collection("user_docs")
    collection.add(
        documents=chunks,
        ids=[str(i) for i in range(len(chunks))]
    )

    return jsonify({"message": f"PDF uploaded. {len(chunks)} chunks stored."})

@app.route("/ask", methods=["POST"])
def ask():
    if collection is None:
        return jsonify({"answer": "Please upload a PDF first."})

    question = request.json["question"]
    results = collection.query(query_texts=[question], n_results=7)
    relevant_chunk = "\n\n".join(results["documents"][0])

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful assistant answering questions about a document. Answer only what is asked. Do not mix information from different sections. Be precise and do not infer or assume anything not explicitly stated in the document. However, you do not have to give texts exactly copied from the pdf. U can reframe the sentences but don't change the meanings."},
            {"role": "user", "content": f"Question: {question}\n\nDocument Information:\n{relevant_chunk}"}
        ]
    )

    return jsonify({"answer": response.choices[0].message.content})

if __name__ == "__main__":
    app.run(debug=True)