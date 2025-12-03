import random
from typing import Set

class NodeIDGenerator:
    _generated_ids: Set[int] = set()

    MIN_ID = 1
    MAX_ID = 9_999_999

    @classmethod
    def generate(cls) -> int:
        while True:
            new_id = random.randint(cls.MIN_ID, cls.MAX_ID)
            if new_id not in cls._generated_ids:
                cls._generated_ids.add(new_id)
                return new_id

    @classmethod
    def generate_many(cls, count: int) -> list[int]:
        population = range(cls.MIN_ID, cls.MAX_ID)
        new_ids = random.sample(population, count)

        cls._generated_ids.update(new_ids)
        return new_ids

    @classmethod
    def reset(cls):
        cls._generated_ids.clear()