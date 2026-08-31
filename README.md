# 🔒 Private LLM

A fully local AI chatbot running Qwen inference on your own GPU using vLLM and Docker.

No OpenAI API. No Anthropic API. No third-party LLM calls.

## ✨ Features

- 🧠 Qwen 2.5 1.5B Instruct
- ⚡ vLLM high-performance inference
- 🎮 NVIDIA GPU acceleration
- 🐳 Dockerized deployment
- 🔌 OpenAI-compatible API
- 💬 Streamlit chat interface
- 🔐 Fully local inference
- ❤️ Conversation history
- 🟢 Automatic server health monitoring
- 📦 AWQ quantized model for lower GPU memory usage

## 🏗️ Tech Stack

- Python
- Streamlit
- vLLM
- PyTorch
- CUDA
- Docker
- NVIDIA Container Toolkit
- Qwen 2.5

## 🚀 Run Locally

### 1. Clone

```bash
git clone https://github.com/YOUR_USERNAME/private-llm.git
cd private-llm

2. Build
docker compose build
3. Start
docker compose up

The application will be available at:

http://localhost

vLLM API:

http://localhost:8000
⚙️ Model
Qwen/Qwen2.5-1.5B-Instruct-AWQ

The model runs locally through vLLM with NVIDIA GPU acceleration.

🔐 Privacy

All prompts and responses are processed locally.

No external LLM API is required.

📸 Screenshots

Add your screenshots here:
![image alt](https://github.com/Atharv28ye/Private-llm-chatbot/blob/9ad714d1205aee524193ddda4e69019e08b62dcb/11.png)
![image alt](https://github.com/Atharv28ye/Private-llm-chatbot/blob/9ad714d1205aee524193ddda4e69019e08b62dcb/22.png)
![image alt](https://github.com/Atharv28ye/Private-llm-chatbot/blob/9ad714d1205aee524193ddda4e69019e08b62dcb/33.png)
👨‍💻 Author
Atharv Puranik

Built as a local GPU-powered LLM deployment project combining AI inference, Docker, CUDA and production-style serving.
🔒 Fully local Qwen LLM deployment using vLLM, Docker, CUDA and NVIDIA GPU acceleration. No external LLM APIs.
This version is short, but still makes the project immediately look like a **serious AI + DevOps/infrastructure project


