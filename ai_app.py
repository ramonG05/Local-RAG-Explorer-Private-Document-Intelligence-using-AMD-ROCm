import streamlit as st
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama

# Esto intenta buscar si estás en Docker, si no, usa localhost
ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Y luego usas la variable:
llm = ChatOllama(model="llama3", base_url=ollama_host)
embeddings = OllamaEmbeddings(model="llama3", base_url=ollama_host)

# Configuración de la página
st.set_page_config(page_title="RAG-Box Local AI", layout="wide")
st.header("🤖 RAG-Box: Private AI Document Reader")

# Sidebar para configuración
with st.sidebar:
    st.info("Corriendo localmente en: AMD Radeon RX 6950 XT")
    model_name = "llama3"

# 1. Interfaz de subida
uploaded_file = st.file_uploader("Arrastra aquí tu PDF", type="pdf")

if uploaded_file:
    # Guardamos el archivo localmente
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getvalue())

    # Indicador de carga
    with st.spinner("Analizando documento..."):
        # Cargamos y dividimos el texto
        loader = PyPDFLoader("temp.pdf")
        docs = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1800, chunk_overlap=300)
        splits = text_splitter.split_documents(docs)

        # Creamos la base de datos en memoria (rápido)
        # Usamos los embeddings de Ollama para que tu gráfica haga el trabajo sucio
        embeddings = OllamaEmbeddings(model=model_name)
        vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)

    st.success("¡Documento listo para preguntas!")

    # 2. Sistema de Chat
    user_question = st.text_input("¿Qué quieres saber de este archivo?")

    if user_question:
        # Buscamos los 3 trozos más parecidos a la pregunta
        context_docs = vectorstore.similarity_search(user_question, k=10)
        context_text = "\n\n".join([doc.page_content for doc in context_docs])

        # Creamos el Prompt para la IA
        full_prompt = f"""
        Eres un analista de documentos oficial. Tu objetivo es ser extremadamente preciso.
    Utiliza ÚNICAMENTE el contexto proporcionado para responder. 
    Si el contexto no menciona la razón específica, di "No encuentro la razón exacta en el documento".
        CONTEXTO: {context_text}
        PREGUNTA: {user_question}
        """

        llm = ChatOllama(model=model_name)
        response = llm.invoke(full_prompt)
        
        st.markdown("### Respuesta de la IA:")
        st.write(response.content)