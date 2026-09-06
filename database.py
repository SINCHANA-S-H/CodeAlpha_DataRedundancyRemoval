import sqlite3

DATABASE = "data.db"


def get_connection():
    """Create and return a database connection."""
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """Create the records table if it does not already exist."""
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL,
            data_hash TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def add_record(name, email, phone, data_hash):
    """Add a unique record to the database."""
    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO records (name, email, phone, data_hash)
            VALUES (?, ?, ?, ?)
            """,
            (name, email, phone, data_hash)
        )
        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()


def get_all_records():
    """Return all stored records."""
    connection = get_connection()

    records = connection.execute(
        """
        SELECT id, name, email, phone, created_at
        FROM records
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()
    return records


def record_exists(email, data_hash):
    """Check whether a record already exists."""
    connection = get_connection()

    record = connection.execute(
        """
        SELECT id
        FROM records
        WHERE email = ? OR data_hash = ?
        """,
        (email, data_hash)
    ).fetchone()

    connection.close()

    return record is not None