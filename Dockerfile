FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
COPY ./src ./src
RUN mkdir -p /app/storage/uploads /app/logs
EXPOSE 8000 7860
CMD ["python", "-m", "src.server.main"]
