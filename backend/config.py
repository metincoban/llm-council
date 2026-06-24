"""Configuration for the LLM Council — Multi-Provider."""

import os
from dotenv import load_dotenv

load_dotenv(override=True)

# ═══ API KEYS & ENDPOINTS ═══
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Provider routing: model prefix → (api_key, api_url, use_key_as_query)
# Only include providers with VERIFIED working direct API keys.
# Models with no matching provider fall through to OpenRouter automatically.
PROVIDERS = {
    # "openai/" disabled — key invalid, routed via OpenRouter
    # "deepseek/" disabled — no direct key yet, routed via OpenRouter
    # "google/" temporarily disabled — 429 rate limited on free tier
}

# Council members — 7 models, routed direct or via OpenRouter
#   openai/*      → direct OpenAI API
#   google/*      → direct Google API
#   deepseek/*    → OpenRouter (no direct key yet)
#   anthropic/*   → OpenRouter
#   nex-agi/*     → OpenRouter
COUNCIL_MODELS = [
    "openai/gpt-5.1",
    "openai/gpt-4o",
    "anthropic/claude-sonnet-4.5",
    "google/gemini-2.5-pro",
    "google/gemini-2.5-flash",
    "deepseek/deepseek-chat",
    "nex-agi/nex-n2-pro:free",
]

# Chairman model
CHAIRMAN_MODEL = "anthropic/claude-sonnet-4.5"

# Data directory
DATA_DIR = "data/conversations"
