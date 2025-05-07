# Usa una imagen base liviana de Python
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY requirements.txt .
COPY . .

# Instala las dependencias
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

    # Instala las dependencias del sistema necesarias para OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 8000 (el que usará Gunicorn)
EXPOSE 8000

# Comando para iniciar el servidor con Gunicorn
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "app:app"]
