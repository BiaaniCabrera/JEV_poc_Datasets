"""Classify support ticket messages into problem_impact categories using TypeSafe.

Usage:
    python3 classify_tickets.py [--input support_tickets.csv] [--output tickets_categorized.csv]
                                [--review review.csv] [--limit N] [--concurrency 8]
"""

import argparse
import csv
from collections import Counter, defaultdict

from typesafe_sdk import TypeSafeClient, Choice, Score, RetryPolicy

from categories import CATEGORIES, INSTRUCTIONS, OUTPUT_COLUMN

LOW_CONFIDENCE = 0.6   # below this -> review
CLOSE_CALL_GAP = 0.15  # top minus runner-up below this -> review

QUESTIONS = {
    OUTPUT_COLUMN: Choice(instructions=INSTRUCTIONS, criteria=CATEGORIES),
    "urgency": Score(
        instructions="How urgent is this ticket?",
        criteria=["can wait", "this week", "today"],
    ),
}
NEW_COLUMNS = [
    OUTPUT_COLUMN,
    f"{OUTPUT_COLUMN}_conf",
    "urgency_score",
    "skipped",
    "error",
]


def read_rows(path: str, limit: int | None) -> tuple[list[dict], list[str]]:
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = list(reader.fieldnames or [])
    if limit:
        rows = rows[:limit]
    return rows, fieldnames


def classify_row(client: TypeSafeClient, row: dict) -> None:
    for col in NEW_COLUMNS:
        row[col] = ""
    message = (row.get("message") or "").strip()
    if not message:
        row["skipped"] = "empty_message"
        return
    try:
        response = client.system_one(state={"document": message}, questions=QUESTIONS)
    except Exception as exc:  # keep going; record the failure on the row
        row["error"] = f"{type(exc).__name__}: {exc}"
        return
    ans = response.choices[OUTPUT_COLUMN]
    row[OUTPUT_COLUMN] = ans.choice
    row[f"{OUTPUT_COLUMN}_conf"] = round(ans.confidence, 3)
    row["urgency_score"] = round(response.scores["urgency"].score, 3)


def classify_all(rows: list[dict]) -> None:
    done = 0
    with TypeSafeClient(retry=RetryPolicy(max_retries=4, backoff_max=20.0)) as client:
        for row in rows:
            classify_row(client, row)
            done += 1
            if done % 25 == 0 or done == len(rows):
                print(f"  classified {done}/{len(rows)}", flush=True)


def needs_review(row: dict) -> bool:
    if not row[OUTPUT_COLUMN]:
        return False
    conf = float(row[f"{OUTPUT_COLUMN}_conf"])
    return conf < LOW_CONFIDENCE


def write_csv(path: str, rows: list[dict], fieldnames: list[str]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def print_report(rows: list[dict]) -> None:
    done = [r for r in rows if r[OUTPUT_COLUMN]]
    skipped = sum(1 for r in rows if r["skipped"])
    errors = [r for r in rows if r["error"]]
    print(f"\nRows: {len(rows)} | classified: {len(done)} | skipped: {skipped} | errors: {len(errors)}")
    for r in errors[:5]:
        print(f"  error {r.get('ticket_id')}: {r['error']}")
    if not done:
        return

    counts = Counter(r[OUTPUT_COLUMN] for r in done)
    conf = defaultdict(list)
    for r in done:
        conf[r[OUTPUT_COLUMN]].append(float(r[f"{OUTPUT_COLUMN}_conf"]))
    print(f"\n{OUTPUT_COLUMN} distribution:")
    print(f"  {'category':26} {'n':>4} {'%':>6} {'avg conf':>9}")
    for cat in CATEGORIES:
        n = counts.get(cat, 0)
        avg = sum(conf[cat]) / n if n else 0
        print(f"  {cat:26} {n:4} {100 * n / len(done):5.1f}% {avg:9.2f}")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--input", default="support_tickets.csv")
    p.add_argument("--output", default="tickets_categorized.csv")
    p.add_argument("--review", default="review.csv")
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--concurrency", type=int, default=8)
    args = p.parse_args()

    rows, fieldnames = read_rows(args.input, args.limit)
    print(f"Classifying {len(rows)} tickets into {len(CATEGORIES)} categories...")
    classify_all(rows)

    out_fields = fieldnames + NEW_COLUMNS
    write_csv(args.output, rows, out_fields)
    review = sorted((r for r in rows if needs_review(r)), key=lambda r: float(r[f"{OUTPUT_COLUMN}_conf"]))
    write_csv(args.review, review, out_fields)

    print_report(rows)
    print(f"\nWrote {args.output} ({len(rows)} rows) and {args.review} ({len(review)} rows to review)")


if __name__ == "__main__":
    main()

