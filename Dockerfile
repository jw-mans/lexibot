FROM python:3.13.9-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
&& pip install --no-cache-dir -r requirements.txt

COPY src/ ./src
ENV PYTHONUNBUFFERED=1
CMD [ "python", "-m", "src.bot.route" ]
