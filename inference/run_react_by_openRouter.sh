# =============================================================================
# DeepResearch Configuration
# =============================================================================
QWEN_DOC_PARSER_USE_IDP=false
QWEN_IDP_ENABLE_CSI=false
NLP_WEB_SEARCH_ONLY_CACHE=false
NLP_WEB_SEARCH_ENABLE_READPAGE=false
NLP_WEB_SEARCH_ENABLE_SFILTER=false
QWEN_SEARCH_ENABLE_CSI=false
SPECIAL_CODE_MODE=false
PYTHONDONTWRITEBYTECODE=1

# =============================================================================
# Model and Inference Hyperparameters
# =============================================================================
MODEL_PATH=alibaba/tongyi-deepresearch-30b-a3b
DATASET=eval_data/example_with_local_tool.jsonl
OUTPUT_PATH=output
ROLLOUT_COUNT=1
TEMPERATURE=0.85
PRESENCE_PENALTY=1.1
MAX_WORKERS=1


# =============================================================================
# API Keys and External Services
# =============================================================================

# Serper API for web search and Google Scholar
# Get your key from: https://serper.dev/
export SERPER_KEY_ID=YOUR_KEY

# Jina API for web page reading
# Get your key from: https://jina.ai/
export JINA_API_KEYS=YOUR_KEY

# Summary model API (OpenAI-compatible) for page summarization
# Get your key from: https://platform.openai.com/
export API_KEY=YOUR_KEY
export OPENAI_API_KEY=YOUR_KEY
export OPENAI_BASE_URL=https://openrouter.ai/api/v1
export API_BASE=https://openrouter.ai/api/v1
export SUMMARY_MODEL_NAME=x-ai/grok-4-fast:free
# =============================================================================

python run_multi_react.py --model $MODEL_PATH --dataset "$DATASET" --output "$OUTPUT_PATH" --max_workers $MAX_WORKERS --roll_out_count $ROLLOUT_COUNT
