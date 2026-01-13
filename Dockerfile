FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
COPY database.py .
COPY game_models.py .
COPY templates/ templates/
COPY static/ static/

EXPOSE 5002

CMD ["python", "app.py"]
