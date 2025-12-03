class Oracle:
    _LEADER_ID = None

    @classmethod
    def set_leader_id(cls, new_leader_id: int) -> None:
        cls._LEADER_ID = new_leader_id

    @classmethod
    def get_leader_id(cls) -> int:
        return cls._LEADER_ID