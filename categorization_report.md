# Categorization Report

Run date: 2026-10-07
Model: `jev-1.13.0`, using the official `typesafe-sdk` 0.7.2 against the live TypeSafe API.
All three JEV question types are used: `Choice` (category or theme), `Noul` (complaint, feedback only) and `Score` (urgency).

## Support tickets (`tickets_categorized.csv`)

- 491 tickets: 481 classified, 10 skipped (empty message), 0 errors
- Average category confidence: 0.92
- 40 tickets below 0.6 confidence, listed in `review.csv` for a person to check

| Category | Tickets | Share | Avg confidence | Avg urgency (0–2) |
|---|---:|---:|---:|---:|
| Interface error | 67 | 13.9% | 0.91 | 1.56 |
| Billing | 73 | 15.2% | 0.95 | 0.93 |
| Access and permission | 39 | 8.1% | 0.99 | 1.37 |
| Feature request | 69 | 14.3% | 0.94 | 0.03 |
| API | 23 | 4.8% | 0.95 | 1.34 |
| Data handling | 42 | 8.7% | 0.96 | 0.57 |
| Calendar synchronization | 31 | 6.4% | 0.82 | 1.11 |
| Notifications | 16 | 3.3% | 0.95 | 0.47 |
| Other | 121 | 25.2% | 0.85 | 0.30 |

**Urgency** (`urgency_score`, 0 = can wait, 1 = this week, 2 = today):

| Band | Tickets |
|---|---:|
| Can wait (below 0.5) | 241 |
| This week (0.5 to 1.5) | 153 |
| Today (1.5 or more) | 87 |

The most urgent tickets are outages reported "this morning", mostly about the API. Feature requests come out as the least urgent (average 0.03).

"Other" is the largest category. It is mostly vague messages, questions about seat limits or plans, and setup questions. A few tickets in it are about features that have no category of their own (Slack integration, the mobile app, the collaboration workspace), and those tend to have low confidence.

## Customer feedback (`feedback_categorized.csv`)

- 218 rows: 214 classified, 4 skipped (empty text), 0 errors
- Average theme confidence: 0.96
- 55 rows (25.7%) flagged as complaints (`is_complaint` likelihood of 0.5 or more)
- Urgency: 168 can wait, 39 this week, 7 today
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

- Urgency is the model's own estimate from the text alone. It doesn't take customer, plan or ticket history into account.
- Earlier results came from keyword rules, not the model. Those files are kept in `old_heuristic_outputs/` for reference only and should not be used.
- These numbers are not compared against the original `category` column or the star ratings, by decision.
