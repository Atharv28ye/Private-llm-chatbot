import os
import requests
import streamlit as st


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

VLLM_HOST = os.getenv(
    "VLLM_HOST",
    "http://127.0.0.1:8000"
).rstrip("/")

# MUST match the model ID exposed by vLLM
MODEL_ID = os.getenv(
    "MODEL_ID",
    "Qwen/Qwen2.5-1.5B-Instruct-AWQ"
)

REQUEST_TIMEOUT = int(
    os.getenv("REQUEST_TIMEOUT", "300")
)


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Private LLM",
    page_icon="🔒",
    layout="centered"
)


# ---------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .main {
        max-width: 900px;
        margin: auto;
    }

    /* Server status box */
    .status-box {
        padding: 18px 22px;
        border-radius: 14px;
        margin-bottom: 20px;

        /* Dark box so text is always visible */
        background: #1f2229;

        /* Visible border */
        border: 1px solid #3a3f4b;

        /* Force readable text */
        color: #f5f7fa;
    }

    /* Make ALL text inside status box readable */
    .status-box h3 {
        color: #ffffff !important;
        margin-bottom: 10px;
    }

    .status-box p {
        color: #d1d5db !important;
        margin: 6px 0;
    }

    .status-box b {
        color: #ffffff !important;
    }

    /* Online status */
    .online {
        color: #4ade80 !important;
    }

    /* Offline status */
    .offline {
        color: #f87171 !important;
    }

    /* Loading status */
    .loading {
        color: #fbbf24 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------------------------------------------------
# vLLM health check
# ---------------------------------------------------------

def check_vllm():

    try:
        response = requests.get(
            f"{VLLM_HOST}/health",
            timeout=5
        )

        return response.status_code == 200

    except requests.RequestException:
        return False


# ---------------------------------------------------------
# Verify model
# ---------------------------------------------------------

def get_model():

    try:

        response = requests.get(
            f"{VLLM_HOST}/v1/models",
            timeout=5
        )

        response.raise_for_status()

        data = response.json()

        models = data.get("data", [])

        if not models:
            return MODEL_ID

        available_model = models[0].get("id")

        if available_model:
            return available_model

    except Exception:
        pass

    return MODEL_ID


# ---------------------------------------------------------
# Generate response using vLLM
# ---------------------------------------------------------

def generate_response(messages):

    model = get_model()

    # Keep only the most recent messages so that
    # input + output stays within the 256-token context.
    recent_messages = messages[-4:]

    payload = {
        "model": model,
        "messages": recent_messages,
        "temperature": 0.7,
        "top_p": 0.9,
        "max_tokens": 32,
        "stream": False
    }

    try:

        response = requests.post(
            f"{VLLM_HOST}/v1/chat/completions",
            json=payload,
            timeout=REQUEST_TIMEOUT
        )

        if response.status_code != 200:

            try:
                error_data = response.json()
            except Exception:
                error_data = response.text

            raise RuntimeError(
                f"vLLM returned HTTP {response.status_code}: "
                f"{error_data}"
            )

        data = response.json()

        return data["choices"][0]["message"]["content"]

    except requests.RequestException as error:

        raise RuntimeError(
            f"Could not connect to vLLM: {error}"
        )


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:

    st.title("🔒 Private LLM")

    st.markdown("### Local inference")

    st.write(
        "Your prompts are sent to the "
        "local vLLM server running inside "
        "this machine."
    )

    st.divider()

    st.write("**Model**")

    st.code(
        MODEL_ID
    )

    st.write("**Inference engine**")

    st.code("vLLM")

    st.write("**API**")

    st.code("OpenAI-compatible")

    st.divider()

    if st.button(
        "🔄 Refresh server status",
        use_container_width=True
    ):

        st.rerun()

    if st.button(
        "🗑️ Clear chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("🔒 Private LLM Chat")

st.caption(
    "Self-hosted Qwen inference using vLLM"
)


# ---------------------------------------------------------
# Server status
# ---------------------------------------------------------

vllm_ready = check_vllm()


if not vllm_ready:

    st.markdown(
        """
        <div class="status-box">

        <h3 class="offline">
        🔴 SERVER OFFLINE
        </h3>

        <p>
        The vLLM model server is still starting.
        </p>

        <p>
        The model may take a few minutes to load
        onto the GPU during startup.
        </p>

        <p>
        Once the server is ready, click
        <b>Refresh server status</b> in the sidebar.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        f"""
        <div class="status-box">

        <h3 class="online">
        🟢 SERVER ONLINE
        </h3>

        <p>
        Model is ready for inference.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# Display previous messages
# ---------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ---------------------------------------------------------
# Chat input
# ---------------------------------------------------------

if vllm_ready:

    prompt = st.chat_input(
        "Message your private LLM..."
    )

    if prompt:

        user_message = {
            "role": "user",
            "content": prompt
        }

        st.session_state.messages.append(
            user_message
        )

        with st.chat_message("user"):

            st.markdown(prompt)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                try:

                    answer = generate_response(
                        st.session_state.messages
                    )

                    st.markdown(answer)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer
                        }
                    )

                except Exception as error:

                    st.error(
                        f"Local model error:\n\n{error}"
                    )

else:

    st.chat_input(
        "Waiting for vLLM server...",
        disabled=True
    )


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.divider()

st.caption(
    "🔐 Local GPU inference • "
    "No OpenAI API • No Anthropic API • "
    "No third-party LLM calls"
)