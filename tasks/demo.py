import json
from llm import complete
from tasks.base import Example, Task

SYSTEM = (
    "Extract fields from the Dutch receipt line. "
    'Reply with JSON only: {"vendor": str, "amount": float, "vat_rate": int}. '
    "No markdown, no explanation."
)

EXAMPLES = [
    Example("1", "Albert Heijn 12,45 EUR incl. 9% BTW",
            {"vendor": "Albert Heijn", "amount": 12.45, "vat_rate": 9}),
    Example("2", "NS Reizigers treinticket 28,00 EUR 9% BTW",
            {"vendor": "NS Reizigers", "amount": 28.00, "vat_rate": 9}),
    Example("3", "Coolblue laptopstandaard 59,99 incl 21% btw",
            {"vendor": "Coolblue", "amount": 59.99, "vat_rate": 21}),
]

def parse(text: str) -> dict:
    t = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```")
    return json.loads(t)

def run(provider: str, ex: Example):
    call = complete(provider, [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": ex.input},
    ], temperature=0)
    try:
        parsed = parse(call.text)
    except Exception:
        parsed = None            # parse failure is a result, not a crash
    return parsed, call

def score(expected: dict, parsed: dict | None) -> dict:
    if parsed is None:
        return {"parsed": 0.0, "vendor": 0.0, "amount": 0.0, "vat_rate": 0.0}
    return {
        "parsed": 1.0,
        "vendor": float(str(parsed.get("vendor", "")).strip().lower()
                        == expected["vendor"].lower()),
        "amount": float(abs(float(parsed.get("amount", -1)) - expected["amount"]) < 0.01),
        "vat_rate": float(parsed.get("vat_rate") == expected["vat_rate"]),
    }

TASK = Task(name="demo", examples=EXAMPLES, run=run, score=score)