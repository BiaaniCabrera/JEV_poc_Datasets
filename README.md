# JEV POC: Ticket and Feedback Categorization

Proof of concept that uses the JEV model (`jev-1.13.0`, via the TypeSafe API) to sort support tickets and customer feedback into categories.

## Setup

```sh
pip install typesafe-sdk
export TYPESAFE_API_KEY="your-key"   # e.g. in ~/.zshrc; never commit it
```

## Run

```sh
python3 jev_test.py                      # quick check that the SDK and key work
python3 classify_tickets.py --limit 20   # trial run; drop --limit for the full file
python3 classify_feedback.py --limit 20
```

## Docs

- [categorization_report.md](categorization_report.md): results of the latest run
- [tools_implemented.md](tools_implemented.md): how the pieces fit together
- [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md): status and next phases
- [TASKS.md](TASKS.md): checklist

Question types used so far: `Choice` (ticket categories and feedback themes) and `Noul` (feedback complaints). `Score` (urgency) has only been tried in `jev_test.py`.

`old_heuristic_outputs/` and `_typesafe_sdk_mock/` are kept for reference only. They come from an earlier version that used keyword rules instead of the model.
