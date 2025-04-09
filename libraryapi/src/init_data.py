from datetime import date
from uuid import uuid4
from src.db import database
from src.infrastructure.utils.password import hash_password


async def init_data():
    """
    Inserts sample data into the database for users, publishers, books, and lendings.

    This function performs the following steps:
    1. Inserts a list of sample users into the database, with a hashed password.
    2. Inserts a list of sample publishers, each linked to a user.
    3. Inserts a list of sample books, each associated with a publisher.
    4. Inserts a list of sample lending records that represent books borrowed by users.

    This function is useful for initializing a development or test environment with mock data.

    Process:
    - Sample user data is created with `uuid4()` for unique user IDs and random user details (name, email, etc.).
    - Sample publisher data is created, linking each publisher to a user.
    - Sample book data is added with details like title, author, year, language, and publisher.
    - Sample lending data is generated with borrow and return details for each book borrowed by the users.

    The function prints progress messages to the console, indicating the addition of users, publishers, books, and lending data.
    """
    print("= = = = = = = = = = = = = = = = = = = =")
    users = [
        {
            "id": uuid4(),
            "name": "user1",
            "email": "user1@gmail.com",
            "phone": "111111111",
            "password": hash_password("pass1"),
        },
        {
            "id": uuid4(),
            "name": "user2",
            "email": "user2@gmail.com",
            "phone": "222222222",
            "password": hash_password("pass2"),
        },
        {
            "id": uuid4(),
            "name": "user3",
            "email": "user3@gmail.com",
            "phone": "333333333",
            "password": hash_password("pass3"),
        },
        {
            "id": uuid4(),
            "name": "user4",
            "email": "user4@gmail.com",
            "phone": "444444444",
            "password": hash_password("pass4"),
        },
    ]

    query = """
        INSERT INTO users (id, name, email, phone, password) VALUES (:id, :name, :email, :phone, :password)
    """
    await database.execute_many(query=query, values=users)
    print("Sample data: Users added.")

    publishers = [
        {
            "company_name": "publisher1",
            "contact_email": "publisher1@gmail.com",
            "user_id": users[0]["id"],
        },
        {
            "company_name": "publisher2",
            "contact_email": "publisher2@gmail.com",
            "user_id": users[1]["id"],
        },
        {
            "company_name": "publisher3",
            "contact_email": "publisher3@gmail.com",
            "user_id": users[2]["id"],
        },
    ]

    publisher_query = """
        INSERT INTO publishers (company_name, contact_email, user_id) VALUES (:company_name, :contact_email, :user_id)
    """
    await database.execute_many(query=publisher_query, values=publishers)
    print("Sample data: Publishers added.")

    publisher_data = await database.fetch_all("SELECT * FROM publishers")

    books = [
        {
            "title": "The Lost Expedition",
            "author": "John Smith",
            "publication_year": "2024",
            "language": "English",
            "publisher_id": publisher_data[0]["id"],
            "borrowed_count": 3,
            "quantity": 10,
            "rating": 4.8,
            "categories": "Adventure",
            "kind": "Novel",
            "epoch": "Modern",
            "genre": "Adventure",
            "is_deleted": False,
        },
        {
            "title": "Whispers of the Heart",
            "author": "Jane Doe",
            "publication_year": "2023",
            "language": "English",
            "publisher_id": publisher_data[0]["id"],
            "borrowed_count": 5,
            "quantity": 7,
            "rating": 4.2,
            "categories": "Drama",
            "kind": "Play",
            "epoch": "Contemporary",
            "genre": "Drama",
            "is_deleted": False,
        },
        {
            "title": "Legends of Eldoria",
            "author": "Arthur White",
            "publication_year": "2020",
            "language": "English",
            "publisher_id": publisher_data[1]["id"],
            "borrowed_count": 12,
            "quantity": 15,
            "rating": 4.9,
            "categories": "Fantasy",
            "kind": "Novel",
            "epoch": "Medieval",
            "genre": "Fantasy",
            "is_deleted": False,
        },
        {
            "title": "Tomorrow's Horizon",
            "author": "Emily Green",
            "publication_year": "2021",
            "language": "English",
            "publisher_id": publisher_data[1]["id"],
            "borrowed_count": 8,
            "quantity": 12,
            "rating": 4.6,
            "categories": "Science Fiction",
            "kind": "Novel",
            "epoch": "Future",
            "genre": "Sci-Fi",
            "is_deleted": False,
        },
        {
            "title": "The Infinite Journey",
            "author": "Liam Brown",
            "publication_year": "2022",
            "language": "English",
            "publisher_id": publisher_data[2]["id"],
            "borrowed_count": 4,
            "quantity": 9,
            "rating": 4.5,
            "categories": "Adventure",
            "kind": "Novel",
            "epoch": "Modern",
            "genre": "Adventure",
            "is_deleted": False,
        },
        {
            "title": "Echoes of the Past",
            "author": "Sophia Turner",
            "publication_year": "2023",
            "language": "English",
            "publisher_id": publisher_data[2]["id"],
            "borrowed_count": 6,
            "quantity": 11,
            "rating": 4.3,
            "categories": "Historical Fiction",
            "kind": "Novel",
            "epoch": "Ancient",
            "genre": "History",
            "is_deleted": False,
        },
        {
            "title": "The Cybernetic Rebellion",
            "author": "Maximus Lee",
            "publication_year": "2025",
            "language": "English",
            "publisher_id": publisher_data[0]["id"],
            "borrowed_count": 2,
            "quantity": 8,
            "rating": 4.7,
            "categories": "Science Fiction",
            "kind": "Novel",
            "epoch": "Future",
            "genre": "Sci-Fi",
            "is_deleted": False,
        },
        {
            "title": "Whispers from the Underworld",
            "author": "Olivia Clark",
            "publication_year": "2023",
            "language": "English",
            "publisher_id": publisher_data[1]["id"],
            "borrowed_count": 9,
            "quantity": 13,
            "rating": 4.6,
            "categories": "Fantasy",
            "kind": "Novel",
            "epoch": "Medieval",
            "genre": "Fantasy",
            "is_deleted": False,
        },
        {
            "title": "Starlight Chronicles",
            "author": "Benjamin King",
            "publication_year": "2024",
            "language": "English",
            "publisher_id": publisher_data[2]["id"],
            "borrowed_count": 7,
            "quantity": 10,
            "rating": 4.9,
            "categories": "Science Fiction",
            "kind": "Novel",
            "epoch": "Future",
            "genre": "Sci-Fi",
            "is_deleted": False,
        },
        {
            "title": "The Secret of Shadows",
            "author": "Nina Adams",
            "publication_year": "2022",
            "language": "English",
            "publisher_id": publisher_data[0]["id"],
            "borrowed_count": 3,
            "quantity": 6,
            "rating": 4.1,
            "categories": "Thriller",
            "kind": "Novel",
            "epoch": "Modern",
            "genre": "Thriller",
            "is_deleted": False,
        },
        {
            "title": "The Secret of Shadows - 2",
            "author": "Nina Adams - 2",
            "publication_year": "2022",
            "language": "English",
            "publisher_id": publisher_data[0]["id"],
            "borrowed_count": 3,
            "quantity": 6,
            "rating": 4.1,
            "categories": "Thriller",
            "kind": "Novel",
            "epoch": "Modern",
            "genre": "Thriller",
            "is_deleted": True,
        },
        {
            "title": "Starlight Chronicles",
            "author": "Edvard King",
            "publication_year": "2022",
            "language": "English",
            "publisher_id": publisher_data[0]["id"],
            "borrowed_count": 7,
            "quantity": 3,
            "rating": 2.4,
            "categories": "Science Fiction",
            "kind": "Novel",
            "epoch": "Future",
            "genre": "Sci-Fi",
            "is_deleted": False,
        },
    ]

    book_query = """
        INSERT INTO books (title, author, publication_year, language, publisher_id, borrowed_count, quantity, rating, categories, kind, epoch, genre, is_deleted) 
        VALUES (:title, :author, :publication_year, :language, :publisher_id, :borrowed_count, :quantity, :rating, :categories, :kind, :epoch, :genre, :is_deleted)
    """
    await database.execute_many(query=book_query, values=books)

    print("Sample data: Books added.")

    lendings = [
        {
            "book_id": 1,
            "user_id": users[0]["id"],
            "borrowed_date": date(2023, 11, 1),
            "returned_date": None,
            "status": "borrowed",
        },
        {
            "book_id": 1,
            "user_id": users[1]["id"],
            "borrowed_date": date(2022, 11, 15),
            "returned_date": date(2022, 12, 5),
            "status": "returned",
        },
        {
            "book_id": 1,
            "user_id": users[2]["id"],
            "borrowed_date": date(2023, 6, 8),
            "returned_date": None,
            "status": "borrowed",
        },
        {
            "book_id": 1,
            "user_id": users[1]["id"],
            "borrowed_date": date(2023, 10, 25),
            "returned_date": date(2023, 11, 10),
            "status": "returned",
        },
        {
            "book_id": 2,
            "user_id": users[2]["id"],
            "borrowed_date": date(2021, 8, 10),
            "returned_date": None,
            "status": "borrowed",
        },
        {
            "book_id": 2,
            "user_id": users[0]["id"],
            "borrowed_date": date(2023, 9, 13),
            "returned_date": date(2023, 9, 1),
            "status": "returned",
        },
        {
            "book_id": 2,
            "user_id": users[1]["id"],
            "borrowed_date": date(2023, 3, 5),
            "returned_date": None,
            "status": "borrowed",
        },
        {
            "book_id": 3,
            "user_id": users[0]["id"],
            "borrowed_date": date(2021, 3, 1),
            "returned_date": date(2021, 4, 20),
            "status": "returned",
        },
        {
            "book_id": 3,
            "user_id": users[1]["id"],
            "borrowed_date": date(2022, 11, 15),
            "returned_date": None,
            "status": "borrowed",
        },
        {
            "book_id": 3,
            "user_id": users[2]["id"],
            "borrowed_date": date(2023, 12, 12),
            "returned_date": None,
            "status": "borrowed",
        },
        {
            "book_id": 3,
            "user_id": users[0]["id"],
            "borrowed_date": date(2024, 11, 28),
            "returned_date": date(2024, 12, 8),
            "status": "returned",
        },
        {
            "book_id": 4,
            "user_id": users[1]["id"],
            "borrowed_date": date(2019, 12, 5),
            "returned_date": None,
            "status": "borrowed",
        },
        {
            "book_id": 4,
            "user_id": users[2]["id"],
            "borrowed_date": date(2019, 11, 10),
            "returned_date": date(2020, 1, 25),
            "status": "returned",
        },
        {
            "book_id": 5,
            "user_id": users[0]["id"],
            "borrowed_date": date(2023, 10, 1),
            "returned_date": date(2023, 11, 15),
            "status": "returned",
        },
        {
            "book_id": 5,
            "user_id": users[2]["id"],
            "borrowed_date": date(2023, 12, 1),
            "returned_date": None,
            "status": "borrowed",
        },
        {
            "book_id": 6,
            "user_id": users[1]["id"],
            "borrowed_date": date(2020, 7, 8),
            "returned_date": None,
            "status": "borrowed",
        },
        {
            "book_id": 6,
            "user_id": users[0]["id"],
            "borrowed_date": date(2021, 7, 15),
            "returned_date": date(2022, 11, 30),
            "status": "returned",
        },
        {
            "book_id": 7,
            "user_id": users[2]["id"],
            "borrowed_date": date(2023, 12, 10),
            "returned_date": date(2023, 12, 10),#None
            "status": "borrowed",
        },
        {
            "book_id": 7,
            "user_id": users[0]["id"],
            "borrowed_date": date(2024, 8, 5),
            "returned_date": date(2024, 11, 25),
            "status": "returned",
        },
        {
            "book_id": 8,
            "user_id": users[1]["id"],
            "borrowed_date": date(2023, 12, 2),
            "returned_date": None,
            "status": "borrowed",
        },
        {
            "book_id": 8,
            "user_id": users[2]["id"],
            "borrowed_date": date(2023, 11, 20),
            "returned_date": date(2023, 12, 1),
            "status": "returned",
        },
        {
            "book_id": 9,
            "user_id": users[0]["id"],
            "borrowed_date": date(2022, 1, 15),
            "returned_date": None,
            "status": "borrowed",
        }
    ]

    lend_query = """
        INSERT INTO lendings (book_id, user_id, borrowed_date, returned_date, status) VALUES (:book_id, :user_id, :borrowed_date, :returned_date, :status)
    """

    await database.execute_many(query=lend_query, values=lendings)

    print("Sample data: Lendings added.")
    print("= = = = = = = = = = = = = = = = = = = =")
