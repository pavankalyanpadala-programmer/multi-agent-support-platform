import json
from collections import Counter, defaultdict
from pathlib import Path
from src.router.intent_router import route_query


LOG_FILE = Path(__file__).resolve().parents[2] / "logs" / "interactions.jsonl"


def load_logs():
    records = []
    if not LOG_FILE.exists():
        print(f"No log file found at {LOG_FILE}")
        return records

    with LOG_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records


def summarize(records):
    if not records:
        print("No records to summarize.")
        return

    intent_counts = Counter(r["intent"] for r in records)
    confidence_by_intent = defaultdict(list)
    latency_by_intent = defaultdict(list)
    length_by_intent = defaultdict(list)

    fallback_total = 0

    for r in records:
        intent = r["intent"]
        confidence_by_intent[intent].append(float(r.get("confidence", 0.0)))
        latency_by_intent[intent].append(int(r.get("latency_ms", 0)))
        length_by_intent[intent].append(int(r.get("response_length", 0)))
        if r.get("fallback"):
            fallback_total += 1

    print("=== Interaction Summary ===")
    print(f"Total interactions: {len(records)}\n")

    print("Counts by intent:")
    for intent, count in intent_counts.items():
        print(f"  {intent}: {count}")

    print("\nAverage confidence by intent:")
    for intent, vals in confidence_by_intent.items():
        avg_conf = sum(vals) / len(vals)
        print(f"  {intent}: {avg_conf:.2f}")

    print("\nAverage latency (ms) by intent:")
    for intent, vals in latency_by_intent.items():
        avg_lat = sum(vals) / len(vals)
        print(f"  {intent}: {avg_lat:.1f} ms")

    print("\nAverage response length by intent:")
    for intent, vals in length_by_intent.items():
        avg_len = sum(vals) / len(vals)
        print(f"  {intent}: {avg_len:.1f} chars")

    fallback_rate = (fallback_total / len(records)) * 100 if records else 0.0
    print(f"\nFallbacks: {fallback_total} ({fallback_rate:.1f}% of interactions)")


EVAL_FILE = Path(__file__).resolve().parents[2] / "data" / "eval" / "router_eval.json"


def evaluate_router():
    if not EVAL_FILE.exists():
        print(f"No router eval file found at {EVAL_FILE}")
        return

    with EVAL_FILE.open("r", encoding="utf-8") as f:
        examples = json.load(f)

    if not examples:
        print("Router eval set is empty.")
        return

    total = 0
    correct = 0
    per_intent_total = Counter()
    per_intent_correct = Counter()
    misclassified = Counter()

    for ex in examples:
        text = ex["text"]
        expected = ex["expected_intent"]
        routed = route_query(text)
        predicted = routed.intent

        total += 1
        per_intent_total[expected] += 1
        if predicted == expected:
            correct += 1
            per_intent_correct[expected] += 1
        else:
            misclassified[(expected, predicted)] += 1

    overall_acc = correct / total
    print("\n=== Router Evaluation ===")
    print(f"Total eval examples: {total}")
    print(f"Overall accuracy: {overall_acc:.2f}")

    print("\nPer-intent accuracy:")
    for intent, n in per_intent_total.items():
        acc = per_intent_correct[intent] / n if n else 0.0
        print(f"  {intent}: {acc:.2f} ({per_intent_correct[intent]}/{n})")

    if misclassified:
        print("\nMisclassifications:")
        for (exp, pred), n in misclassified.items():
            print(f"  expected={exp}, predicted={pred}: {n}")


if __name__ == "__main__":
    logs = load_logs()
    summarize(logs)
    evaluate_router()
