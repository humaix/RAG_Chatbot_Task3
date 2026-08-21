class Conversation:

    def __init__(self, max_history=5):
        self.history = []
        self.max_history = max_history

    def add_message(self, role, message):

        self.history.append({
            "role": role,
            "message": message
        })

        if len(self.history) > self.max_history * 2:
            self.history = self.history[-self.max_history * 2:]

    def get_history(self):
        return self.history

    def clear(self):
        self.history.clear()