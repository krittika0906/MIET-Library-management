"""Reusable utility functions for the MIET Library application."""


def calculate_fine(days_kept, allowed_days=14, rate=5):
    """Calculate overdue days and fine. Invalid values raise ValueError."""
    days_kept = int(days_kept)
    allowed_days = int(allowed_days)
    rate = float(rate)

    if days_kept < 0 or allowed_days < 0 or rate < 0:
        raise ValueError("Days and fine rate cannot be negative")

    overdue_days = max(0, days_kept - allowed_days)
    total_fine = overdue_days * rate
    return overdue_days, total_fine


def is_available(catalogue, book_title):
    """Return True when the book exists and has at least one available copy."""
    normalized = book_title.strip().lower()
    for title, copies in catalogue.items():
        if title.lower() == normalized:
            return copies > 0
    return False


def prepare_summary(catalogue, borrowed_books):
    """Produce a summary for a catalogue and an account's borrowed books."""
    return (
        f"Borrowed: {', '.join(borrowed_books) if borrowed_books else 'None'}\n"
        f"Catalogue: {catalogue}"
    )
