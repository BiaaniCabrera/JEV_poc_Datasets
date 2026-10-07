"""Classify customer feedback text into feedback_theme categories and is_complaint (Noul) using TypeSafe.

Usage:
    python3 classify_feedback.py [--input customer_feedback.csv] [--output feedback_categorized.csv]
                                 [--review feedback_review.csv] [--limit N] [--concurrency 8]
"""

import argparse
import asyncio
import csv
from collections import Counter, defaultdict

from typesafe_sdk import AsyncTypeSafeClient, Choice, Noul, Score, RetryPolicy

from categories import FEEDBACK_CATEGORIES, FEEDBACK_INSTRUCTIONS

OUTPUT_COLUMN = "feedback_theme"
LOW_CONFIDENCE = 0.6
CLOSE_CALL_GAP = 0.15

QUESTIONS = {
    OUTPUT_COLUMN: Choice(instructions=FEEDBACK_INSTRUCTIONS, criteria=FEEDBACK_CATEGORIES),
    "is_complaint": Noul(
        instructions="Is this customer feedback expressing a complaint, frustration, or negative issue?"
    ),
    "urgency": Score(
        instructions="How urgent is this feedback?",
        criteria=["can wait", "this week", "today"],
    ),
}

NEW_COLUMNS = [
    OUTPUT_COLUMN,
    f"{OUTPUT_COLUMN}_conf",
    "runner_up",
    "runner_up_conf",
    "is_complaint_prob",
    "is_complaint_noul",
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


async def classify_row(client: AsyncTypeSafeClient, sem: asyncio.Semaphore, row: dict) -> None:
    for col in NEW_COLUMNS:
        row[col] = ""
    text = (row.get("feedback_text") or "").strip()
    if not text:
        row["skipped"] = "empty_feedback"
        return

    async with sem:
        try:
            response = await client.system_one(state={"document": text}, questions=QUESTIONS)
        except Exception as exc:
            row["error"] = f"{type(exc).__name__}: {exc}"
            return

    # Process Choice answer for feedback_theme
    choice_ans = response.choices[OUTPUT_COLUMN]
    ranked = sorted(choice_ans.probabilities.items(), key=lambda kv: kv[1], reverse=True)
    row[OUTPUT_COLUMN] = choice_ans.choice
    row[f"{OUTPUT_COLUMN}_conf"] = round(choice_ans.confidence, 3)
    if len(ranked) > 1:
        row["runner_up"] = ranked[1][0]
        row["runner_up_conf"] = round(ranked[1][1], 3)

    # Process Noul answer for is_complaint
    # noul is the probability of "yes" (0-1), not a bool
    noul_prob = response.nouls["is_complaint"].noul
    row["is_complaint_prob"] = round(noul_prob, 3)
    row["is_complaint_noul"] = str(noul_prob >= 0.5)

    row["urgency_score"] = round(response.scores["urgency"].score, 3)


async def classify_all(rows: list[dict], concurrency: int) -> None:
    sem = asyncio.Semaphore(concurrency)
    retry = RetryPolicy(max_retries=4, backoff_max=20.0)
    done = 0
    async with AsyncTypeSafeClient(retry=retry) as client:

        async def run(row: dict) -> None:
            nonlocal done
            await classify_row(client, sem, row)
            done += 1
            if done % 25 == 0 or done == len(rows):
                print(f"  classified {done}/{len(rows)}", flush=True)

        await asyncio.gather(*(run(r) for r in rows))


def needs_review(row: dict) -> bool:
    if not row[OUTPUT_COLUMN]:
        return False
    conf = float(row[f"{OUTPUT_COLUMN}_conf"])
    runner = float(row["runner_up_conf"] or 0)
    return conf < LOW_CONFIDENCE or (conf - runner) < CLOSE_CALL_GAP


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
        print(f"  error {r.get('feedback_id')}: {r['error']}")
    if not done:
        return

    # Theme distribution
    counts = Counter(r[OUTPUT_COLUMN] for r in done)
    conf = defaultdict(list)
    for r in done:
        conf[r[OUTPUT_COLUMN]].append(float(r[f"{OUTPUT_COLUMN}_conf"]))
    print(f"\n{OUTPUT_COLUMN} distribution:")
    print(f"  {'category':26} {'n':>4} {'%':>6} {'avg conf':>9}")
    for cat in FEEDBACK_CATEGORIES:
        n = counts.get(cat, 0)
        avg = sum(conf[cat]) / n if n else 0
        print(f"  {cat:26} {n:4} {100 * n / len(done):5.1f}% {avg:9.2f}")

    # Complaint stats
    noul_complaints = sum(1 for r in done if r["is_complaint_noul"] == "True")
    print(f"\nComplaints (is_complaint >= 0.5): {noul_complaints} ({100*noul_complaints/len(done):.1f}%)")

    pairs = Counter((r[OUTPUT_COLUMN], r["runner_up"]) for r in done if needs_review(r))
    if pairs:
        print("\nMost common close calls (choice <- runner-up):")
        for (a, b), n in pairs.most_common(8):
            print(f"  {n:3}  {a} <- {b}")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--input", default="customer_feedback.csv")
    p.add_argument("--output", default="feedback_categorized.csv")
    p.add_argument("--review", default="feedback_review.csv")
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--concurrency", type=int, default=8)
    args = p.parse_args()

    rows, fieldnames = read_rows(args.input, args.limit)
    print(f"Classifying {len(rows)} customer feedback entries into {len(FEEDBACK_CATEGORIES)} themes...")
    asyncio.run(classify_all(rows, args.concurrency))

    out_fields = fieldnames + NEW_COLUMNS
    write_csv(args.output, rows, out_fields)
    review = sorted((r for r in rows if needs_review(r)), key=lambda r: float(r[f"{OUTPUT_COLUMN}_conf"] or 0))
    write_csv(args.review, review, out_fields)

    print_report(rows)
    print(f"\nWrote {args.output} ({len(rows)} rows) and {args.review} ({len(review)} rows to review)")


if __name__ == "__main__":
    main()
