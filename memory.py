from collections import defaultdict

from config import MAX_HISTORY


class Memory:

    def __init__(self):

        self.histories = defaultdict(list)

    def get(self, user_id):

        return self.histories[user_id]

    def clear(self, user_id):

        self.histories[user_id] = []

    def add(self, user_id, role, content):

        self.histories[user_id].append(

            {

                "role": role,

                "content": content

            }

        )

        if len(self.histories[user_id]) > MAX_HISTORY:

            self.histories[user_id].pop(0)

    def export(self, user_id):

        return list(self.histories[user_id])


memory = Memory()