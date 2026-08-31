#!/bin/bash
set -e
# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
MODEL_ID="${MODEL_ID:-Qwen/Qwen2.5-1.5B-Instruct-AWQ}"
# Bumped: 1.5B model needs ~3GB+ just for weights on this 4GB card
GPU_UTIL="${GPU_UTIL:-0.85}"
MAX_MODEL_LEN="${MAX_MODEL_LEN:-256}"
VLLM_HOST="${VLLM_HOST:-http://127.0.0.1:8000}"
VLLM_PORT="${VLLM_PORT:-8000}"
STREAMLIT_PORT="${STREAMLIT_PORT:-80}"
# ---------------------------------------------------------
# Force legacy GPU model runner (avoid UVA requirement)
# ---------------------------------------------------------
export VLLM_USE_V2_MODEL_RUNNER=0
# ---------------------------------------------------------
# Display configuration
# ---------------------------------------------------------
echo "============================================================"
echo "        PRIVATE QWEN DEPLOYMENT"
echo "============================================================"
echo "Model:           ${MODEL_ID}"
echo "GPU utilization: ${GPU_UTIL}"
echo "Max context:     ${MAX_MODEL_LEN}"
echo "vLLM host:       ${VLLM_HOST}"
echo "vLLM port:       ${VLLM_PORT}"
echo "Streamlit port:  ${STREAMLIT_PORT}"
echo "Model runner:    legacy (V2 disabled)"
echo "============================================================"
# ---------------------------------------------------------
# Start vLLM
# ---------------------------------------------------------
echo ""
echo "Starting vLLM..."
echo ""
vllm serve "${MODEL_ID}" \
    --host 0.0.0.0 \
    --port "${VLLM_PORT}" \
    --gpu-memory-utilization "${GPU_UTIL}" \
    --max-model-len "${MAX_MODEL_LEN}" \
    --served-model-name "${MODEL_ID}" \
    --enforce-eager &
VLLM_PID=$!
echo ""
echo "vLLM started with PID ${VLLM_PID}"
echo ""
# ---------------------------------------------------------
# Wait for vLLM
# ---------------------------------------------------------
echo "Waiting for vLLM to become ready..."
MAX_WAIT=1800
WAITED=0
while true; do
    if curl -sf \
        "http://127.0.0.1:${VLLM_PORT}/health" \
        > /dev/null
    then
        echo ""
        echo "============================================================"
        echo "vLLM IS READY"
        echo "============================================================"
        echo ""
        break
    fi
    if ! kill -0 "${VLLM_PID}" 2>/dev/null; then
        echo ""
        echo "ERROR: vLLM process stopped unexpectedly."
        echo ""
        exit 1
    fi
    if [ "${WAITED}" -ge "${MAX_WAIT}" ]; then
        echo ""
        echo "ERROR: vLLM did not become ready within ${MAX_WAIT} seconds."
        echo ""
        kill "${VLLM_PID}" 2>/dev/null || true
        exit 1
    fi
    echo "vLLM still loading... (${WAITED}s)"
    sleep 5
    WAITED=$((WAITED + 5))
done
# ---------------------------------------------------------
# Start Streamlit
# ---------------------------------------------------------
echo ""
echo "Starting Streamlit..."
echo ""
exec streamlit run app.py \
    --server.address=0.0.0.0 \
    --server.port="${STREAMLIT_PORT}" \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false