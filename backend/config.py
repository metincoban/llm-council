"""Configuration for the LLM Council — Multi-Provider."""

import os
from dotenv import load_dotenv

load_dotenv()

# ═══ API KEYS & ENDPOINTS ═══
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Provider routing: model prefix → (api_key, api_url, use_key_as_query)
PROVIDERS = {
    "openai/":   (OPENAI_API_KEY,     "https://api.openai.com/v1/chat/completions",           False),
    "openrouter/":(OPENROUTER_API_KEY, "https://openrouter.ai/api/v1/chat/completions",       False),
    "google/":   (GOOGLE_API_KEY,     "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions", False),
}

# Council members — 6 models across 3 providers
COUNCIL_MODELS = [
    # OpenAI (direct API)
    "openai/gpt-5.1",
    "openai/gpt-4o",
    # Anthropic (via OpenRouter)
    "anthropic/claude-sonnet-4.5",
    "anthropic/claude-opus-4-8",
    # Google (via OpenRouter for Gemini — direct key available as fallback)
    "google/gemini-2.5-pro",
    "google/gemini-2.5-flash",
]

# Chairman model
CHAIRMAN_MODEL = "anthropic/claude-opus-4-8"

# Data directory
DATA_DIR = "data/conversations"
