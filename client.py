import os
from typing import Optional, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class ProviderConfigurationError(ValueError):
    pass


PROVIDERS: Dict[str, Dict[str, Any]] = {
    "openrouter": {
        "env_var": "OPENROUTER_API_KEY",
        "base_url": "https://openrouter.ai/api/v1",
    },
    "groq": {
        "env_var": "GROQ_API_KEY",
        "base_url": "https://api.groq.com/openai/v1",
    },
    "cerebras": {
        "env_var": "CEREBRAS_API_KEY",
        "base_url": "https://api.cerebras.ai/v1",
    },
}


def get_client(provider: Optional[str] = None) -> OpenAI:
    if provider:
        provider_key = provider.lower()
        if provider_key not in PROVIDERS:
            supported = ", ".join(PROVIDERS.keys())
            raise ProviderConfigurationError(
                f"Unknown provider '{provider}'. Supported providers are: {supported}."
            )
        
        config = PROVIDERS[provider_key]
        api_key = os.getenv(config["env_var"])
        if not api_key:
            raise ProviderConfigurationError(
                f"API key for provider '{provider}' ({config['env_var']}) is not set."
            )
        
        return OpenAI(base_url=config["base_url"], api_key=api_key)

    for name, config in PROVIDERS.items():
        api_key = os.getenv(config["env_var"])
        if api_key:
            return OpenAI(base_url=config["base_url"], api_key=api_key)

    required_vars = ", ".join(cfg["env_var"] for cfg in PROVIDERS.values())
    raise ProviderConfigurationError(
        f"No active provider API keys found. Please set one of the following environment variables: {required_vars}"
    )
