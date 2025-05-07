# Usa una imagen base ligera de Python
FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia el requirements y luego el resto
COPY requirements.txt .
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Instala dependencias Python
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copia el resto del proyecto
COPY . .

# Expone el puerto 8000 (Railway redirige el tráfico)
EXPOSE 8000

# Inicia el servidor
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "app:app"]
