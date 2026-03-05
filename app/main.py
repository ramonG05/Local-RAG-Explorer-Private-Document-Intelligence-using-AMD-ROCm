import streamlit as st
import os
from langchain_ollama import OllamaEmbeddings, ChatOllama
from styles import apply_custom_styles 
from processor import process_pdf
import torch
import psutil

# Saves the uploads in the data/uploads folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "data", "uploads")

# Creates the folder if it doesn't exist
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# This tries to find if you are in Docker, if not, uses localhost
ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Then you use the variable:
llm = ChatOllama(model="llama3", base_url=ollama_host)
embeddings = OllamaEmbeddings(model="llama3", base_url=ollama_host)

# Page configuration
st.set_page_config(page_title="RAG-Box Local AI", layout="wide")
apply_custom_styles()
st.header("🤖 RAG-Box: Private AI Document Reader")

# Sidebar for configuration
with st.sidebar:
    st.title("Configuration")
    model_name = "llama3"
    
    # Dynamic hardware detection
    try:
        if torch.cuda.is_available():
            # Detects the GPU
            device_info = f"Core: {torch.cuda.get_device_name(0)} 🚀"
        else:
            # If there is no GPU, identifies the processor
            import platform
            device_info = f"Core: {platform.processor()} ⚡ (CPU Mode)"
    except Exception:
        device_info = "Core: Local Hardware"

    st.info(device_info)
    st.write(f"**Running Model:** {model_name}")
    
# Upload interface
uploaded_file = st.file_uploader("Drag and drop your PDF here", type="pdf")

if uploaded_file:
        # Defines the full path inside the data/uploads folder
        # 'temp_path' ahora apunta a RAG-BOX/data/uploads/temp.pdf
    temp_path = os.path.join(UPLOAD_DIR, "temp.pdf")
    
    #  Saves the file in the corporate location
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    #  Loading indicator
    with st.spinner("Analyzing and saving context to database..."):
        # Calls the function passing the correct technical path
        vectorstore = process_pdf(temp_path, embeddings)

    st.success("Document analyzed and context saved")

    # Chat system
    user_question = st.text_input("What do you want to know about this file?")

    if user_question:
        # Searches the 20 most similar chunks to the question
        context_docs = vectorstore.similarity_search(user_question, k=20)
        context_text = "\n\n".join([doc.page_content for doc in context_docs])

        # Prompt for the AI
        full_prompt = f"""
        You are an official document analyst. Your goal is to be extremely precise.
    Use only the provided context to answer. 
    If the context does not mention the specific reason, say "I cannot find the exact reason in the document".
        CONTEXT: {context_text}
        QUESTION: {user_question}
        """
        
        response = llm.invoke(full_prompt)
        
        st.markdown("### AI Response:")
        st.write(response.content)