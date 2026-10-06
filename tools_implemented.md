# Tools Implemented

What is used to categorize support tickets and customer feedback, and how it fits together.

## 1. TypeSafe SDK (`typesafe-sdk`, installed package)

The official SDK, version 0.7.2, installed in the Python environment. It sends a message plus a set of questions to the TypeSafe API, and the JEV model (`jev-1.13.0`) answers them.

- **API key:** read from the `TYPESAFE_API_KEY` environment variable, which is set in `~/.zshrc`. If the key is missing or invalid, the SDK raises an error. It never makes up an answer.
- **Question types:**
  - `Choice` picks one label and returns `choice`, `confidence` and `probabilities` for every label.
  - `Noul` is a yes/no question. It returns `noul`, the **likelihood of yes, from 0 to 1** (not True/False). The scripts count 0.5 or more as yes.
  - `Score` rates against an ordered scale and returns `score`, an average that can fall between levels (e.g. 1.99 on a 0–2 scale).

## 2. JEV test script (`jev_test.py`)

A small check that the SDK and key work. It asks a billing yes/no, a tone choice and an urgency score about one sample message.

## 3. Ticket classification (`classify_tickets.py`)

- Reads `support_tickets.csv` and puts each `message` into one of the categories in `categories.py`.
- Writes `tickets_categorized.csv`, which adds the `problem_impact`, `problem_impact_conf`, `skipped` and `error` columns.
- Writes `review.csv`, listing tickets with confidence below 0.6.
- Retries failed calls up to 4 times. A row that still fails is recorded in the `error` column and the run carries on.
- Options: `--limit N` for a trial run, plus `--input`, `--output` and `--review`.

## 4. Feedback classification (`classify_feedback.py`)

- Reads `customer_feedback.csv`, puts each `feedback_text` into one of 15 themes, and asks whether it is a complaint.
- Writes `feedback_categorized.csv`, which adds the theme, its confidence, the second-best theme, `is_complaint_prob` and `is_complaint_noul`.
- Writes `feedback_review.csv`, listing rows with confidence below 0.6 or where the top two themes are within 0.15 of each other.
- Sends 8 requests at a time, with retries.

## 5. Categories (`categories.py`)

- `CATEGORIES` holds the 9 ticket categories: Interface error, Billing, Access and permission, Feature request, API, Data handling, Calendar synchronization, Notifications, plus Other as a fallback.
- `FEEDBACK_CATEGORIES` holds the 15 feedback themes.
- Each category has a description, and the model sees only the label and that description. Clear descriptions that don't overlap matter more than the label names.

## 6. Outputs

- `tickets_categorized.csv`, `review.csv`, `feedback_categorized.csv` and `feedback_review.csv`: current results from the live model.
- `categorization_report.md`: a summary of the latest run.
- `old_heuristic_outputs/`: earlier results from keyword rules. Kept for reference only, do not use.
- `_typesafe_sdk_mock/`: the old local stand-in for the SDK. It isn't used any more and can be deleted.
