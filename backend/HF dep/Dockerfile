FROM python:3.11-slim

WORKDIR /app

# Install git and gcc (needed for some python packages to build)
RUN apt-get update && apt-get install -y \
    gcc \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Hugging Face Spaces specific port
EXPOSE 7860

# Command to start the app
CMD ["uvicorn", "src.hackathon_todo_api.main:app", "--host", "0.0.0.0", "--port", "7860"]