FROM python:3.12-slim

# Set working directory
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src

EXPOSE 8080
ENV PYTHONPATH="/app/src"
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]