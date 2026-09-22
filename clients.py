import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Fill eur_in / eur_out from the Token Factory price list and your
# frontier provider's pricing. Per 1M tokens.
MODELS = {
    "open": {
        "id": "REPLACE_WITH_A_MODEL_FROM_TOKEN_FACTORY",
        "eur_in": 0.0,
        "eur_out": 0.0,
    },
    "frontier": {
        "id": "gpt-4.1-mini",
        "eur_in": 0.0,
        "eur_out": 0.0,
    },
}

def get_client(provider: str) -> OpenAI:
    if provider == "open":
        return OpenAI(
            api_key=os.environ["NEBIUS_API_KEY"],
            base_url=os.environ["NEBIUS_BASE_URL"],
        )
    if provider == "frontier":
        return OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    raise ValueError(f"unknown provider: {provider}")