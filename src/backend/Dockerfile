# -----------------------------
# 1) Base Python image
# -----------------------------
FROM python:3.10-slim

# -----------------------------
# 2) Create working directory
# -----------------------------
WORKDIR /app

# -----------------------------
# 3) Copy project files to container
# -----------------------------
COPY . /app

# -----------------------------
# 4) Install system dependencies (optional)
# -----------------------------
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# 5) Install Python dependencies
# -----------------------------
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------
# 6) Expose Flask port
# -----------------------------
EXPOSE 5000

# -----------------------------
# 7) Start backend server
# (Change app.py to your main Python file)
# -----------------------------
CMD ["python", "app.py"]
