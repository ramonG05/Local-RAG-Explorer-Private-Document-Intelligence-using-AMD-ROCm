import os

def clean_temp_files(file_path):
    """Borra archivos temporales para mantener el servidor limpio."""
    if os.path.exists(file_path):
        os.remove(file_path)