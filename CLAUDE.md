# CLAUDE.md

Proof of concept: the JEV model (`jev-1.13.0`) categorizes support tickets and customer feedback through the TypeSafe API. Overview and run commands are in `README.md`, how the pieces fit in `tools_implemented.md`, status and next steps in `IMPLEMENTATION_PLAN.md` and `TASKS.md`. Read those before starting work.

## Ground rules

- **The project works as it is. Do not change scripts, categories or outputs unless asked.** Propose changes first.
- Ask before any full run (491 tickets + 218 feedback rows). Each row is a paid API call. Test with `--limit 5` or `--limit 20` first.
- After a full run, check that every classified row has all its answers and that `error` is empty.
- Keep `TASKS.md` and `IMPLEMENTATION_PLAN.md` up to date when work is done. Cross out finished tasks, don't delete them.
- Commit and push to GitHub (`origin`, branch `main`) only when asked.

## Decisions already made

- **Ticket categories (9, tickets only):** Interface error, Billing, Access and permission, Feature request, API, Data handling, Calendar synchronization, Notifications, Other (fallback). Defined in `categories.py`.
- **Feedback** keeps its own 15 themes (`FEEDBACK_CATEGORIES`).
- **Do not compare results** against the original `category` column in the tickets or the star `rating` in the feedback.
- **Question types in use:** `Choice` (category/theme), `Noul` (complaint, feedback only), `Score` (urgency, both files, 0 = can wait, 1 = this week, 2 = today).

## Things that will bite you

- **Never create a folder named `typesafe_sdk` in this project.** It hides the real installed SDK (`typesafe-sdk` 0.7.2). That happened before, and every result came from keyword rules instead of the model. The old copy lives in `_typesafe_sdk_mock/` and is not used.
- **`Noul` returns a likelihood (0–1), not True/False.** `bool(0.02)` is `True`. The scripts use 0.5 or more as yes.
- **`Score` returns a number between levels** (e.g. 1.99), not the label.
- **API key** is read from `TYPESAFE_API_KEY`, set in `~/.zshrc`. Never print it, write it to a file or commit it.
- **`403 … not allowed by policy`** means a network block (VPN, company network or sandboxed terminal), not a bad key. A bad key gives an authentication error. A failed run overwrites the output CSVs. Restore them with `git checkout -- <file>`.
- `old_heuristic_outputs/` holds results from the keyword-rule version. Reference only, never use them as results.

## How the user likes to work

- Plain explanations, no jargon.
- A small trial and a summary before anything costly or hard to undo.
- Keep a backup instead of deleting.
