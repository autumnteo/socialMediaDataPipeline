import sqlite3
from contextlib import contextmanager
from typing import Iterator


class DatabaseConnection:
    def __init__(
        self, db_type: str = 'sqlite3', db_file: str = 'data/socialetl.db'
    ) -> None:
        self._db_type = db_type
        self._db_file = db_file

    @contextmanager
    def managed_cursor(self) -> Iterator[sqlite3.Cursor]:
        if self._db_type == 'sqlite3':
            _conn = sqlite3.connect(self._db_file)
            cur = _conn.cursor()
            try:
                yield cur
            finally:
                _conn.commit()
                cur.close()
                _conn.close()

    def __str__(self) -> str:
        return f'{self._db_type}://{self._db_file}'


def db_factory(
    db_type: str = 'sqlite3', db_file: str = 'data/socialetl.db'
) -> DatabaseConnection:
    return DatabaseConnection(db_type=db_type, db_file=db_file)
