import sqlite3
from choreList import Chore, ChoreList
from resident import Resident

DB_PATH = "chores.db"

def get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def initialize_db(db_path: str = DB_PATH) -> None:
    with get_connection(db_path) as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS chores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                time TEXT NOT NULL,
                chore_list_name TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS residents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                age INTEGER,
                UNIQUE(first_name, last_name, age)
            );

            CREATE TABLE IF NOT EXISTS restrictions (
                resident_id INTEGER,
                chore_name TEXT,
                restricted INTEGER DEFAULT 0,
                FOREIGN KEY(resident_id) REFERENCES residents(id)
            );

            CREATE TABLE IF NOT EXISTS last_week_chores (
                resident_id INTEGER,
                chore_name TEXT,
                FOREIGN KEY(resident_id) REFERENCES residents(id)
            );
        """)

def increment_all_ages(db_path: str = DB_PATH) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute("UPDATE residents SET age = age + 1")


class ChoreListRepository:
    def __init__(self, db_path: str = DB_PATH) -> None:
        self.db_path = db_path

    def save(self, chore_list: ChoreList) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "DELETE FROM chores WHERE chore_list_name = ?",
                (chore_list.name,)
            )
            for chore in chore_list.getChores():
                conn.execute(
                    "INSERT INTO chores (name, time, chore_list_name) VALUES (?, ?, ?)",
                    (chore.get_name(), chore.get_time(), chore_list.name)
                )

    def load(self, name: str) -> ChoreList:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT name, time FROM chores WHERE chore_list_name = ?",
                (name,)
            )
            chores = cursor.fetchall()
        chore_list = ChoreList.__new__(ChoreList)
        chore_list.name = name
        chore_list.chores = [Chore(row[0], row[1]) for row in chores]
        return chore_list


class ResidentRepository:
    def __init__(self, db_path: str = DB_PATH) -> None:
        self.db_path = db_path

    def save(self, resident: Resident, age: int) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """INSERT OR IGNORE INTO residents (first_name, last_name, age)
                   VALUES (?, ?, ?)""",
                (resident.first_name, resident.last_name, age)
            )
            cursor = conn.execute(
                """SELECT id FROM residents
                   WHERE first_name = ? AND last_name = ? AND age = ?""",
                (resident.first_name, resident.last_name, age)
            )
            resident_id = cursor.fetchone()[0]

            conn.execute(
                "DELETE FROM restrictions WHERE resident_id = ?",
                (resident_id,)
            )
            for chore_name, restricted in resident.resident_restriction.items():
                conn.execute(
                    """INSERT INTO restrictions (resident_id, chore_name, restricted)
                       VALUES (?, ?, ?)""",
                    (resident_id, chore_name, int(restricted))
                )

            conn.execute(
                "DELETE FROM last_week_chores WHERE resident_id = ?",
                (resident_id,)
            )
            for chore in resident.get_last_week_chore_list():
                conn.execute(
                    """INSERT INTO last_week_chores (resident_id, chore_name)
                       VALUES (?, ?)""",
                    (resident_id, chore.get_name())
                )

    def load(self, first_name: str, last_name: str, age: int, chore_list: ChoreList) -> Resident | None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """SELECT id FROM residents
                   WHERE first_name = ? AND last_name = ? AND age = ?""",
                (first_name, last_name, age)
            )
            row = cursor.fetchone()
            if row is None:
                return None
            resident_id = row[0]

            restrictions_cursor = conn.execute(
                "SELECT chore_name, restricted FROM restrictions WHERE resident_id = ?",
                (resident_id,)
            )
            restrictions = {row[0]: bool(row[1]) for row in restrictions_cursor.fetchall()}

            last_week_cursor = conn.execute(
                "SELECT chore_name FROM last_week_chores WHERE resident_id = ?",
                (resident_id,)
            )
            last_week_names = {row[0] for row in last_week_cursor.fetchall()}

        resident = Resident(first_name, last_name, chore_list)
        resident.resident_restriction = restrictions
        last_week_chores = [c for c in chore_list.getChores() if c.get_name() in last_week_names]
        resident.set_last_week_chore_list(last_week_chores)
        return resident

    def get_or_create(
        self,
        first_name: str,
        last_name: str,
        age: int,
        chore_list: ChoreList
    ) -> Resident:
        resident = self.load(first_name, last_name, age, chore_list)
        if resident is None:
            resident = Resident(first_name, last_name, chore_list)
        return resident