"""problem_impact categories.

Edit labels/descriptions here; classify_tickets.py imports this file.
The model only sees each label + its description, so clear, non-overlapping
descriptions matter more than the label names.
"""

OUTPUT_COLUMN = "problem_impact"

INSTRUCTIONS = (
    "Which category best describes the problem or impact in this customer support message? "
    "Pick the single best fit. If the message is about the API, notifications or the calendar "
    "synchronization feature, choose that category even if the problem is wrong data, errors or sync "
    "failures. Use 'Other' only if none of the other categories apply."
)

CATEGORIES: dict[str, str] = {
    "Interface error": (
        "Problems in the app's user interface: screens or tools not loading, timing out, "
        "showing errors, behaving incorrectly, showing wrong numbers or producing corrupted "
        "results."
    ),
    "Billing": (
        "Invoices, charges, double or unexpected charges, refunds, payment issues, "
        "or the amount billed."
    ),
    "Access and permission": (
        "Logging in, locked-out accounts, two-factor authentication, resetting access, "
        "users missing access or having the wrong permissions."
    ),
    "Feature request": (
        "Suggestions for new functionality or improvements, e.g. dark mode, keyboard shortcuts, "
        "bulk actions, more customization, new export options."
    ),
    "API": (
        "The public API itself: API errors, failures, limits, or questions about using the API."
    ),
    "Data handling": (
        "Data export, data import, and handling of large data sets."
    ),
    "Calendar synchronization": (
        "Only the calendar synchronization feature: calendar sync failing, not loading, disconnecting, "
        "wrong results or questions about it."
    ),
    "Notifications": (
        "Notifications not arriving, not loading, arriving incorrectly, or questions about "
        "how notifications work."
    ),
    "Other": (
        "General questions, onboarding or setup guidance, or messages too vague to tell "
        "what the customer needs."
    ),
}

FEEDBACK_INSTRUCTIONS = (
    "Which feedback theme best describes what this customer is commenting on? "
    "Pick the single best fit. Use 'Other' only if none of the other categories apply."
)

FEEDBACK_CATEGORIES: dict[str, str] = {
    "Reporting Tool": "Feedback regarding the reporting tool feature, reports, or reporting UI.",
    "Admin Console": "Feedback regarding the admin console, administrative settings, or admin user permissions.",
    "Search": "Feedback regarding search functionality, search results, or search performance.",
    "Dashboard": "Feedback regarding the main dashboard UI, overview metrics, or dashboard widgets.",
    "API": "Feedback regarding the public API, API endpoints, developer documentation, or API behavior.",
    "Data Export": "Feedback regarding data export, downloading data files, CSV exports, or data handling.",
    "Calendar Sync": "Feedback regarding calendar synchronization feature.",
    "Collaboration Workspace": "Feedback regarding the collaboration workspace feature.",
    "Notifications": "Feedback regarding notifications, email alerts, or system notifications.",
    "Support Response Time": "Feedback regarding customer support team speed, response times, or issue resolution.",
    "Product Reliability": "General feedback regarding overall system stability, frequent crashes, unreliability, or widespread bugs.",
    "Slack Integration": "Feedback regarding the Slack integration.",
    "Mobile App Experience": "Feedback regarding the mobile application, mobile interface, or mobile responsiveness.",
    "Subscriptions or Plans": "Feedback regarding plan pricing, billing, seat limits, invoices, or subscription upgrades/downgrades.",
    "Other": "Feedback that does not fit any of the above specific themes.",
}


