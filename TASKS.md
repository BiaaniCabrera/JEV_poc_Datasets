# Tasks

Crossed-out tasks are done. Details for each phase are in [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md).

## Phase 1: Make the POC real

- [x] ~~Find out why the API key wasn't used (a local copy of the SDK was hiding the real one)~~
- [x] ~~Move the local copy to `_typesafe_sdk_mock/`~~
- [x] ~~Set `TYPESAFE_API_KEY` in `~/.zshrc`~~
- [x] ~~Run `jev_test.py` against the live API~~
- [x] ~~Test messages the keyword rules got wrong~~
- [x] ~~Move the old keyword-rule outputs to `old_heuristic_outputs/`~~
- [x] ~~Fix the complaint flag (likelihood from 0 to 1, 0.5 or more counts as yes)~~
- [x] ~~Run a trial of 20 rows per file~~
- [x] ~~Set the 9 ticket categories~~
- [x] ~~Remove the comparisons against the original category column and the star ratings~~
- [x] ~~Run all 491 tickets~~
- [x] ~~Run all 218 feedback rows~~
- [x] ~~Add retries to the ticket script and re-run the 2 failed tickets~~
- [x] ~~Rewrite `categorization_report.md` and `tools_implemented.md`~~
- [x] ~~Write the implementation plan and this task list~~
- [x] ~~Push the project to GitHub~~
- [x] ~~Add urgency (`Score`) to tickets and feedback~~
- [x] ~~Restore outputs overwritten by a blocked run (403 "not allowed by policy")~~
- [x] ~~Re-run all tickets and feedback with all three question types (0 errors)~~

## Phase 2: Check result quality

- [ ] Review the 40 tickets in `review.csv`
- [ ] Review the 7 rows in `feedback_review.csv`
- [ ] Go through the 121 "Other" tickets and decide whether any topic needs its own category
- [ ] Check the Calendar synchronization description (lowest confidence, 0.82)
- [ ] Spot-check urgency scores, especially the 87 tickets rated "today"
- [ ] If descriptions change: run a trial with `--limit 40`, then re-run everything

## Phase 3: Make it repeatable

- [ ] Make `classify_tickets.py` send requests in parallel
- [ ] Save the model name on each output row
- [ ] Generate `categorization_report.md` from the scripts
- [ ] Delete `_typesafe_sdk_mock/`

## Phase 4: Hand-off

- [ ] Decide who works through the review lists, and how often
- [ ] Decide when to re-run
- [ ] Share the report and plan with the team
