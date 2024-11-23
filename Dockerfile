# Usa un'immagine Python
FROM python:3.10-slim

# Imposta la directory di lavoro
WORKDIR /app

# Copia i file necessari nel container
COPY requirements.txt .
COPY main.py .
COPY config.json .

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Comando di avvio
CMD ["python", "main.py"]
