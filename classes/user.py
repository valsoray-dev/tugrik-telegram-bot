"""User related classes"""

from dataclasses import dataclass


@dataclass
class User:
    """User class"""

    db_id: int
    user_id: int
    username: str
    reg_date: str
    schedules: int
