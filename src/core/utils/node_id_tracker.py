import random
from typing import Set, List


class NodeIDConflictError(Exception):
    pass

class NodeIDTracker:
    _claimed_ids: Set[int] = set()

    MIN_ID = 0
    MAX_ID = 9_999_999

    @classmethod
    def claim_range(cls, start: int, count: int) -> List[int]:
        if count <= 0:
            raise ValueError("count must be > 0")

        end_id = start + count - 1
        if start < cls.MIN_ID or end_id > cls.MAX_ID:
            raise ValueError(f"Requested range [{start}, {end_id}] out of bounds ({cls.MIN_ID}-{cls.MAX_ID})")

        requested = list(range(start, end_id + 1))
        overlap = cls._claimed_ids.intersection(requested)
        if overlap:
            raise NodeIDConflictError(f"Cannot claim IDs: already in use {sorted(overlap)}")

        cls._claimed_ids.update(requested)
        return requested

    @classmethod
    def generate_many_random(cls, count: int) -> List[int]:
        if count <= 0:
            raise ValueError("count must be > 0")

        available_count = cls.MAX_ID - cls.MIN_ID + 1 - len(cls._claimed_ids)
        if available_count < count:
            raise ValueError("Not enough available IDs to generate requested amount")

        population = [i for i in range(cls.MIN_ID, cls.MAX_ID + 1) if i not in cls._claimed_ids]
        new_ids = random.sample(population, count)
        cls._claimed_ids.update(new_ids)
        return new_ids

    @classmethod
    def reset(cls) -> None:
        cls._claimed_ids.clear()