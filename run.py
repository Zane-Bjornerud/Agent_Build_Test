import json, sys, importlib
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict

def run_all(task, providers=("open", "frontier"), workers=4):
    out = Path("results") / task.name / datetime.now().strftime("%H%M%S")
    out.mkdir(parents=True, exist_ok=True)
    for provider in providers:
        def one(ex):
            try:
                parsed, call = task.run(provider, ex)
                return {"id": ex.id, "expected": ex.expected,
                        "parsed": parsed, "call": asdict(call), "error": None}
            except Exception as e:
                return {"id": ex.id, "expected": ex.expected,
                        "parsed": None, "call": None, "error": repr(e)}
        with ThreadPoolExecutor(max_workers=workers) as pool:
            records = list(pool.map(one, task.examples))
        (out / f"{provider}.json").write_text(json.dumps(records, indent=2))
        print(f"{provider}: {len(records)} records -> {out / f'{provider}.json'}")
    return out

if __name__ == "__main__":
    mod = importlib.import_module(f"tasks.{sys.argv[1]}")
    run_all(mod.TASK)