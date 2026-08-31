FROM vllm/vllm-openai:latest

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install Streamlit and HTTP client
RUN pip install --no-cache-dir streamlit requests

# Copy application
COPY app.py /app/app.py
COPY entrypoint.sh /app/entrypoint.sh

# Convert Windows CRLF line endings to Linux LF
RUN sed -i 's/\r$//' /app/entrypoint.sh

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Configuration
ENV MODEL_ID=Qwen/Qwen2.5-1.5B-Instruct-AWQ
ENV GPU_UTIL=0.85
ENV MAX_MODEL_LEN=2048
ENV VLLM_HOST=http://127.0.0.1:8000
ENV VLLM_PORT=8000
ENV STREAMLIT_PORT=80

EXPOSE 80
EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]