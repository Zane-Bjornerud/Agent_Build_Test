import json, sys, importlib
from pathlib import Path
from statistics import mean

def report(task, run_dir):
    run_dir = Path(run_dir)
    rows = []
    for f in sorted(run_dir.glob("*.json")):
        records = json.loads(f.read_text())
        scores = [task.score(r["expected"], r["parsed"]) for r in records]
        calls = [r["call"] for r in records if r["call"]]
        row = {"provider": f.stem, "n": len(records)}
        for k in scores[0]:
            row[k] = mean(s[k] for s in scores)
        row["latency_s"] = mean(c["latency_s"] for c in calls) if calls else 0
        row["eur_per_task"] = mean(c["eur"] for c in calls) if calls else 0
        rows.append(row)

    cols = list(rows[0].keys())
    print(" | ".join(f"{c:>14}" for c in cols))
    for r in rows:
        print(" | ".join(
            f"{r[c]:>14.4f}" if isinstance(r[c], float) else f"{str(r[c]):>14}"
            for c in cols))

if __name__ == "__main__":
    mod = importlib.import_module(f"tasks.{sys.argv[1]}")
    report(mod.TASK, sys.argv[2])