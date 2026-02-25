# 1. Usamos una versión ligera de Python como base
FROM python:3.10-slim

# 2. Le decimos a Docker en qué carpeta interna va a trabajar
WORKDIR /app

# 3. Copiamos el archivo de librerías primero (para optimizar la caché de Docker)
COPY requirements.txt .

# 4. Instalamos las dependencias dentro del contenedor
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos el resto de tu código (el app.py, etc.)
COPY . .

# 6. Exponemos el puerto que usa Streamlit por defecto
EXPOSE 8501

# 7. El comando que ejecutará el contenedor al encenderse
CMD ["streamlit", "run", "ai_app.py", "--server.address=0.0.0.0"]