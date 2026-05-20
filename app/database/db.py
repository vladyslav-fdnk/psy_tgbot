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
                client_id INTEGER,
                service TEXT,
                date TEXT,
                time TEXT,
                status TEXT
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


def add_booking(
    client_id: int, service: str, date: str, time: str, status="pending"
) -> None:
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO bookings (client_id, service, date, time, status)
            VALUES (?, ?, ?, ?, ?)
            """,
            (client_id, service, date, time, status),
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


def get_client_id(user_id: int) -> int | None:
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM clients WHERE user_id = ?", (user_id,))

        result = cursor.fetchone()

        if result:
            return result[0]

        return None


def approve_booking_in_db(booking_id: int):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
        UPDATE bookings
        SET status = 'approved'
        WHERE id = ?
        """,
            (booking_id,),
        )
    conn.commit()


def reject_booking_in_db(booking_id: int):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE bookings
        SET status = 'rejected'
        WHERE id = ?
        """,
        (booking_id,),
    )
    conn.commit()
