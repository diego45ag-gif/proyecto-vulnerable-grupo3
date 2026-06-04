FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

# Instalar los requerimientos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente directamente al contenedor
COPY app/ .

# Usuario seguro sin privilegios de root (SDLC)
RUN useradd -u 8888 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5001

CMD ["python", "main.py"]