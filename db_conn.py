from pathlib import Path
from sqlite3 import Connection
import sqlite3

DB_FILEPATH = Path().joinpath("./school.db")
DB_CONN: Connection = sqlite3.connect(DB_FILEPATH)