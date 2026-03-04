import streamlit as st
import os
from langchain_ollama import OllamaEmbeddings, ChatOllama
from styles import apply_custom_styles 
from processor import process_pdf

# Esto intenta buscar si estás en Docker, si no, usa localhost
ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Y luego usas la variable:
llm = ChatOllama(model="llama3", base_url=ollama_host)
embeddings = OllamaEmbeddings(model="llama3", base_url=ollama_host)

# Configuración de la página
st.set_page_config(page_title="RAG-Box Local AI", layout="wide")
apply_custom_styles()
st.header("🤖 RAG-Box: Private AI Document Reader")

# Sidebar para configuración
with st.sidebar:
    st.info("Running locally on AMD Radeon rx 6950 xt")
    model_name = "llama3"

# Interfaz de subida
uploaded_file = st.file_uploader("Arrastra aquí tu PDF", type="pdf")

if uploaded_file:
    #  Guardamos el archivo (Se queda en main porque es gestión de la interfaz)
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getvalue())

    #  Indicador de carga
    with st.spinner("Analizando documento..."):
        # SUSTITUCIÓN: Llamamos a la función modular
        # Le pasamos la ruta y el objeto 'embeddings' que definiste arriba en el main
        vectorstore = process_pdf("temp.pdf", embeddings)

    st.success("¡Documento listo para preguntas!")

    # Sistema de Chat
    user_question = st.text_input("¿Qué quieres saber de este archivo?")

    if user_question:
        # Buscamos los 20 trozos más parecidos a la pregunta
        context_docs = vectorstore.similarity_search(user_question, k=20)
        context_text = "\n\n".join([doc.page_content for doc in context_docs])

        # Creamos el Prompt para la IA
        full_prompt = f"""
        Eres un analista de documentos oficial. Tu objetivo es ser extremadamente preciso.
    Utiliza solo el contexto proporcionado para responder. 
    Si el contexto no menciona la razón específica, di "No encuentro la razón exacta en el documento".
        CONTEXTO: {context_text}
        PREGUNTA: {user_question}
        """
        
        response = llm.invoke(full_prompt)
        
        st.markdown("### Respuesta de la IA:")
        st.write(response.content)