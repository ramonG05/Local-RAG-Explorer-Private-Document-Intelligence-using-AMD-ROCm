import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* Cambiar el fondo de la barra lateral */
        [data-testid="stSidebar"] {
            background-color: #f0f2f6;
        }
        
        /* Estilizar el título principal */
        h1 {
            color: #2e4053;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }

        /* Mejorar el diseño de los mensajes de éxito */
        .stAlert {
            border-radius: 10px;
        }

        /* Hacer que el botón de subida resalte */
        .stFileUploader {
            border: 2px dashed #4CAF50;
            padding: 10px;
            border-radius: 15px;
        }
        </style>
    """, unsafe_allow_html=True)