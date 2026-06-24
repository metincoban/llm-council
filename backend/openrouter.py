"""Multi-Provider API client — routes models to their native APIs, falls back to OpenRouter."""

import httpx
from typing import List, Dict, Any, Optional
from .config import OPENROUTER_API_KEY, PROVIDERS

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def _resolve_provider(model: str):
    """Find matching provider config by model prefix. Returns (api_key, api_url) or None."""
    for prefix, (api_key, api_url, _use_query) in PROVIDERS.items():
        if model.startswith(prefix) and api_key:
            return api_key, api_url
    return None


async def query_model(
    model: str,
    messages: List[Dict[str, str]],
    timeout: float = 120.0
) -> Optional[Dict[str, Any]]:
    """
    Query a single model via its native API when available, falling back to OpenRouter.

    Args:
        model: Model identifier (e.g., "openai/gpt-4o", "deepseek/deepseek-chat")
        messages: List of message dicts with 'role' and 'content'
        timeout: Request timeout in seconds

    Returns:
        Response dict with 'content' and optional 'reasoning_details', or None if failed
    """
    provider = _resolve_provider(model)
    if provider:
        api_key, api_url = provider
    else:
        api_key, api_url = OPENROUTER_API_KEY, OPENROUTER_URL

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    # DeepSeek and OpenAI use the same payload format (no prefix needed)
    # OpenRouter needs the full model id including prefix
    payload_model = model if api_url == OPENROUTER_URL else model.split("/", 1)[1]
    payload = {
        "model": payload_model,
        "messages": messages,
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(api_url, headers=headers, json=payload)
            response.raise_for_status()

            data = response.json()
            message = data['choices'][0]['message']

            return {
                'content': message.get('content'),
                'reasoning_details': message.get('reasoning_details')
            }

    except Exception as e:
        print(f"Error querying model {model}: {e}")
        return None


async def query_models_parallel(
    models: List[str],
    messages: List[Dict[str, str]]
) -> Dict[str, Optional[Dict[str, Any]]]:
    """
    Query multiple models in parallel.

    Args:
        models: List of OpenRouter model identifiers
        messages: List of message dicts to send to each model

    Returns:
        Dict mapping model identifier to response dict (or None if failed)
    """
    import asyncio

    # Create tasks for all models
    tasks = [query_model(model, messages) for model in models]

    # Wait for all to complete
    responses = await asyncio.gather(*tasks)

    # Map models to their responses
    return {model: response for model, response in zip(models, responses)}
