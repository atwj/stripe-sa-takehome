from model import Book

# define books
_books_db = {
    "1" : Book(1, "The Art of Doing Science and Engineering", 
            "Richard Hamming", 
            "The Art of Doing Science and Engineering is a reminder that a childlike capacity for learning and creativity are accessible to everyone",
            2300,
            "/images/art-science-eng.jpg"
        ),
    "2": Book(2, "The Making of Prince of Persia: Journals 1985-1993", 
            "Jordan Mechner", 
            "In The Making of Prince of Persia, on the 30th anniversary of the game’s release, Mechner looks back at the journals he kept from 1985 to 1993..",
            2500,
            "/images/prince-of-persia.jpg"
        ),
    "3": Book(3, "Working in Public: The Making and Maintenance of Open Source", 
            "Nadia Eghbal", 
            "Nadia Eghbal takes an inside look at modern open source and offers a model through which to understand the challenges faced by online creators.",
            2800,
            "/images/working-in-public.jpg"
        )
}

def get_all_books():
    return _books_db

def get_book_by_id(id):
    return _books_db.get(id, None)