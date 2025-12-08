import random
from typing import List, Optional


class Oracle:
    _LEADERS: List[int] = []

    @classmethod
    def register_leader(cls, leader_id: int) -> None:
        if leader_id not in cls._LEADERS:
            cls._LEADERS.append(leader_id)

    @classmethod
    def remove_leader(cls, leader_id: int) -> None:
        if leader_id in cls._LEADERS:
            cls._LEADERS.remove(leader_id)

    @classmethod
    def is_leader(cls, leader_id: int) -> bool:
        return leader_id in cls._LEADERS

    @classmethod
    def set_leader_id(cls, new_leader_id: int) -> None:
        cls._LEADERS = [new_leader_id]

    @classmethod
    def get_leader_id(cls) -> Optional[int]:
        if not cls._LEADERS:
            return None
        return random.choice(cls._LEADERS)

    @classmethod
    def reset(cls) -> None:
        cls._LEADERS = []