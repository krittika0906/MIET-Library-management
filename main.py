"""MIET Campus Library borrowing and fine management system."""

from datetime import datetime
from library_utils import calculate_fine, is_available, prepare_summary
from library_account import LibraryAccount


RECORD_FILE = "library_records.txt"


def append_transaction(member_id, action, book_title):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp} | {member_id} | {action} | {book_title}\n"
    with open(RECORD_FILE, "a", encoding="utf-8") as record_file:
        record_file.write(line)


def read_records(filename=RECORD_FILE):
    try:
        with open(filename, "r", encoding="utf-8") as record_file:
            return record_file.read()
    except FileNotFoundError:
        print(f"[HANDLED FileNotFoundError] Records file '{filename}' was not found.")
        print("Correction: Create the file or use an existing records file, then retry.")
        return ""


def input_number(prompt, number_type):
    while True:
        try:
            value = input(prompt)
            return number_type(value)
        except ValueError:
            print("[HANDLED ValueError] Invalid number.")
            print("Cause: Non-numeric text was entered where a number is required.")
            print("Correction: Enter an integer or decimal number, depending on the prompt.")


def find_catalogue_title(catalogue, book_title):
    normalized = book_title.strip().lower()
    return next((title for title in catalogue if title.lower() == normalized), None)


def main():
    print("=== MILESTONE 1: BASIC DATA HANDLING ===")
    student_name = input("Student name: ").strip() or "Riya Sharma"
    roll_number = input("Roll number: ").strip() or "2023A1R015"
    book_title = input("Book title: ").strip() or "Learning Python"
    days_kept = input_number("Days kept: ", int)
    allowed_days = input_number("Allowed days: ", int)
    fine_rate = input_number("Daily fine rate (Rs.): ", float)

    student_name = " ".join(student_name.title().split())
    book_title = " ".join(book_title.title().split())
    overdue_days, total_fine = calculate_fine(days_kept, allowed_days, fine_rate)

    print(f"Student: {student_name}")
    print(f"Roll Number: {roll_number}")
    print(f"Book: {book_title}")
    print(f"Type of days kept: {type(days_kept).__name__}")
    print(f"Type of fine rate: {type(fine_rate).__name__}")
    print(f"Overdue days: {overdue_days}")
    print(f"Total fine: Rs. {total_fine:.2f}")

    print("\n=== MILESTONE 2: CATALOGUE, DECISIONS AND LOOPS ===")
    catalogue = {
        "Python Basics": 2,
        "Data Structures": 1,
        "Computer Networks": 2,
        "Operating Systems": 0,
    }
    borrowed_books = []

    print("Catalogue:", catalogue)
    while len(borrowed_books) < 3:
        choice = input("Enter a book choice (or DONE): ").strip()
        if choice.upper() == "DONE":
            print("Borrowing stopped by user.")
            break

        exact_title = find_catalogue_title(catalogue, choice)
        if exact_title is None:
            print(f"[Rejected] '{choice}' is unknown. Choose a listed catalogue book.")
            continue

        if not is_available(catalogue, exact_title):
            print(f"[Rejected] '{exact_title}' is unavailable (0 copies).")
            continue

        catalogue[exact_title] -= 1
        borrowed_books.append(exact_title)
        append_transaction(roll_number, "BORROW", exact_title)
        print(f"[SUCCESS] Borrowed '{exact_title}'.")

    print("Borrowed-book list:", borrowed_books)
    print("Updated catalogue:", catalogue)

    print("\n=== MILESTONE 3: OOP MODEL ===")
    riya = LibraryAccount("2023A1R015", "Riya Sharma")
    aarav = LibraryAccount("2023A1R016", "Aarav Kumar")

    print("Before operations:")
    print(riya)
    print(aarav)

    if riya.borrow_book("Python Basics", catalogue):
        append_transaction(riya.member_id, "BORROW", "Python Basics")
        print("Riya borrowed 'Python Basics'.")
    if aarav.borrow_book("Data Structures", catalogue):
        append_transaction(aarav.member_id, "BORROW", "Data Structures")
        print("Aarav borrowed 'Data Structures'.")
    if riya.return_book("Python Basics", catalogue):
        append_transaction(riya.member_id, "RETURN", "Python Basics")
        print("Riya returned 'Python Basics'.")

    print("After operations:")
    riya.display_account()
    aarav.display_account()

    print("\n=== MILESTONE 4: FUNCTIONS, MODULES AND TIME ===")
    overdue, fine = calculate_fine(days_kept=18, allowed_days=14, rate=5)
    print(f"Transaction time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Sample fine check: overdue={overdue}, fine=Rs. {fine:.2f}")
    print(prepare_summary(catalogue, riya.borrowed_books))

    print("\n=== MILESTONE 5: FILE AND EXCEPTION HANDLING ===")
    saved_records = read_records()
    print("Saved records:")
    print(saved_records if saved_records.strip() else "(No saved records)")

    print("\nMissing-file demonstration:")
    read_records("missing_records.txt")


if __name__ == "__main__":
    main()
