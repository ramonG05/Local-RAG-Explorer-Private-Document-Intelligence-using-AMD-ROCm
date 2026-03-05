import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

# 1. Definimos la ruta de forma dinámica y absoluta
# Subimos un nivel desde 'app/' para llegar a la raíz y luego entrar a 'data/vector_db'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VECTOR_DB_DIR = os.path.join(BASE_DIR, "data", "vector_db")

def process_pdf(file_path, embeddings_model):
    """
    Carga un PDF, lo divide en fragmentos y crea un vectorstore.
    """
    
    # 1. Asegurar que la carpeta de datos existe
    if not os.path.exists(VECTOR_DB_DIR):
        os.makedirs(VECTOR_DB_DIR)
        
    # 2. Cargar el PDF
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    
    # 3. Dividimos el texto en trozos (Chunks)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=500)
    splits = text_splitter.split_documents(docs)

    # 4. Creamos la base de datos vectorial con los embeddings pasados como parámetro
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings_model,
        persist_directory=VECTOR_DB_DIR
    )
    
    return vectorstore