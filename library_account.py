"""Object-oriented account model for the MIET Library."""

from library_utils import is_available


class LibraryAccount:
    library_name = "MIET Campus Library"

    def __init__(self, member_id, student_name, borrowed_books=None):
        self.member_id = member_id
        self.student_name = student_name
        self.borrowed_books = borrowed_books if borrowed_books is not None else []

    def borrow_book(self, book_title, catalogue):
        if not is_available(catalogue, book_title):
            return False

        # Match the supplied title to the catalogue's exact key.
        exact_title = next(
            (title for title in catalogue if title.lower() == book_title.strip().lower()),
            None,
        )
        if exact_title is None:
            return False

        catalogue[exact_title] -= 1
        self.borrowed_books.append(exact_title)
        return True

    def return_book(self, book_title, catalogue):
        exact_title = next(
            (title for title in self.borrowed_books
             if title.lower() == book_title.strip().lower()),
            None,
        )
        if exact_title is None:
            return False

        self.borrowed_books.remove(exact_title)
        catalogue[exact_title] += 1
        return True

    def display_account(self):
        print(f"Library: {LibraryAccount.library_name}")
        print(f"Member ID: {self.member_id}")
        print(f"Student: {self.student_name}")
        print(f"Borrowed Books: {', '.join(self.borrowed_books) if self.borrowed_books else 'None'}")

    def __str__(self):
        books = ", ".join(self.borrowed_books) if self.borrowed_books else "no borrowed books"
        return f"{self.member_id} - {self.student_name}: {books}"
