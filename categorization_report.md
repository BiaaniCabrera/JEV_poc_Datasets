# Categorization Report

Run date: 2026-10-06
Model: `jev-1.13.0`, using the official `typesafe-sdk` 0.7.2 against the live TypeSafe API.

## Support tickets (`tickets_categorized.csv`)

- 491 tickets: 481 classified, 10 skipped (empty message), 0 errors
- Average confidence: 0.91
- 39 tickets below 0.6 confidence, listed in `review.csv` for a person to check

| Category | Tickets | Share | Avg confidence |
|---|---:|---:|---:|
| Interface error | 67 | 13.9% | 0.91 |
| Billing | 73 | 15.2% | 0.95 |
| Access and permission | 39 | 8.1% | 0.99 |
| Feature request | 69 | 14.3% | 0.94 |
| API | 23 | 4.8% | 0.94 |
| Data handling | 42 | 8.7% | 0.95 |
| Calendar synchronization | 31 | 6.4% | 0.83 |
| Notifications | 16 | 3.3% | 0.95 |
| Other | 121 | 25.2% | 0.85 |

"Other" is the largest group. It is mostly vague messages, questions about seat limits or plans, and setup questions. A few tickets in it are about features that have no category of their own (Slack integration, the mobile app, the collaboration workspace), and those tend to have low confidence.

## Customer feedback (`feedback_categorized.csv`)

- 218 rows: 214 classified, 4 skipped (empty text), 0 errors
- Average theme confidence: 0.95
- 55 rows (25.7%) flagged as complaints (`is_complaint` likelihood of 0.5 or more)
- 7 rows in `feedback_review.csv` (confidence below 0.6, or top two themes within 0.15 of each other)

| Theme | Rows |
|---|---:|
| Reporting Tool | 16 |
| Admin Console | 21 |
| Search | 16 |
| Dashboard | 16 |
| API | 16 |
| Data Export | 15 |
| Calendar Sync | 14 |
| Collaboration Workspace | 13 |
| Notifications | 12 |
| Support Response Time | 21 |
| Product Reliability | 7 |
| Slack Integration | 11 |
| Mobile App Experience | 6 |
| Subscriptions or Plans | 4 |
| Other | 26 |

## Notes

- Earlier results came from keyword rules, not the model. Those files are kept in `old_heuristic_outputs/` for reference only and should not be used.
- Two tickets (TCK-00044, TCK-00045) failed on the API side during the full run and were re-run successfully after retries were added.
- These numbers are not compared against the original `category` column or the star ratings, by decision.
