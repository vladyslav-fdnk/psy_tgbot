import sqlite3
from typing import TypedDict

DB_NAME = "bot.db"


class ClientData(TypedDict):
    user_id: int
    name: str
    age: int
    timezone: str
    request: str
    therapy_experience: str
    anxiety_level: str
    contact_method: str


def init_db() -> None:
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                date TEXT,
                time TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                name TEXT,
                age INTEGER,
                timezone TEXT,
                request TEXT,
                therapy_experience TEXT,
                anxiety_level TEXT,
                contact_method TEXT
            )
        """)

        conn.commit()


def add_booking(user_id: int, username: str, date: str, time: str) -> None:
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO bookings (user_id, username, date, time)
            VALUES (?, ?, ?, ?)
        """,
            (user_id, username, date, time),
        )

        conn.commit()


def save_client(data: ClientData) -> None:
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO clients (
                user_id,
                name,
                age,
                timezone,
                request,
                therapy_experience,
                anxiety_level,
                contact_method
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                name=excluded.name,
                age=excluded.age,
                timezone=excluded.timezone,
                request=excluded.request,
                therapy_experience=excluded.therapy_experience,
                anxiety_level=excluded.anxiety_level,
                contact_method=excluded.contact_method
        """,
            (
                data["user_id"],
                data["name"],
                data["age"],
                data["timezone"],
                data["request"],
                data["therapy_experience"],
                data["anxiety_level"],
                data["contact_method"],
            ),
        )

        conn.commit()
