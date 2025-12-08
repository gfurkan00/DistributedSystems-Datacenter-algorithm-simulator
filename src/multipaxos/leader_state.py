class LeaderState:
    def __init__(self):
        self.current_term = 0
        self.leader_id = None
        self.is_leader = False
        self.phase1_done = False

    def start_new_term(self, my_id: int):
        self.current_term += 1
        self.leader_id = my_id
        self.is_leader = False
        self.phase1_done = False

    def become_leader(self):
        self.is_leader = True
        self.phase1_done = True
