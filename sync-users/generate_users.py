import sqlite3
from contextlib import closing
from faker import Faker


SEED = 0
FILENAME = "users.db"
COUNT = 3


def generate_user(faker):
    return {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "address": faker.address(),
        "email": faker.email(),
    }


def populate_database(db, faker, count):
    with closing(db.cursor()) as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                address TEXT,
                email TEXT
            )
        """
        )

        cursor.execute("DELETE FROM users")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='users'")

        for _ in range(count):
            user = generate_user(faker)

            cursor.execute(
                """
                INSERT INTO users (first_name, last_name, address, email)
                VALUES (?, ?, ?, ?)
            """,
                (user["first_name"], user["last_name"], user["address"], user["email"]),
            )


if __name__ == "__main__":
    faker = Faker()
    faker.seed_instance(SEED)
    db = sqlite3.connect(FILENAME)
    try:
        with db:
            populate_database(db, faker, COUNT)
    finally:
        db.close()
