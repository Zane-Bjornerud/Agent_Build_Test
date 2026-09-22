import time
from dataclasses import dataclass, asdict
from tenacity import retry, stop_after_attempt, wait_exponential
from clients import MODELS, get_client

@dataclass
class Call:
    provider: str
    model: str
    text: str
    prompt_tokens: int
    completion_tokens: int
    latency_s: float
    eur: float

#change the euro in & euro out
@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
def complete(provider: str, messages: list[dict], **kwargs) -> Call:
    cfg = MODELS[provider]
    client = get_client(provider)
    t0 = time.perf_counter()
    r = client.chat.completions.create(model=cfg["id"], messages=messages, **kwargs)
    dt = time.perf_counter() - t0
    u = r.usage
    eur = (u.prompt_tokens * cfg["eur_in"]
           + u.completion_tokens * cfg["eur_out"]) / 1_000_000
    return Call(
        provider=provider, model=cfg["id"],
        text=r.choices[0].message.content,
        prompt_tokens=u.prompt_tokens,
        completion_tokens=u.completion_tokens,
        latency_s=dt, eur=eur,
    )