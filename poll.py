import uuid

class Poll:
    def __init__(self, questions, options):
        self.id=str(uuid.uuid4)
        self.questions = questions
        self.options = {option: 0 for option in options}
        self.active = True

    def vote(self, option):
        if not self.active:
            raise ValueError("Poll is Closed")
        if option not in self.options:
            raise ValueError("Invalid Option")
        self.options[option] += 1

    def update_poll(self, new_question=None, new_options=None):
        if new_question:
            self.questions=new_question
        if new_options:
            self.options={option: 0 for option in new_options}

    def close_poll(self):
        self.active = False
    
    def get_results(self):
        return {"question": self.questions, "options": self.options, "active": self.active}

class PollManager:
    def __init__(self):
        self.polls = {}

    def create_poll(self, question, options):
        poll = Poll(question, options)
        self.polls[poll.id] = poll
        return poll.id

    def delete_poll(self, poll_id):
        if poll_id in self.polls:
            del self.polls[poll_id]
        else:
            raise ValueError("Poll ID not found.")

    def update_poll(self, poll_id, new_question=None, new_options=None):
        if poll_id not in self.polls:
            raise ValueError("Poll ID not found.")
        self.polls[poll_id].update_poll(new_question, new_options)

    def vote(self, poll_id, option):
        if poll_id not in self.polls:
            raise ValueError("Poll ID not found.")
        self.polls[poll_id].vote(option)

    def get_results(self, poll_id):
        if poll_id not in self.polls:
            raise ValueError("Poll ID not found.")
        return self.polls[poll_id].get_results()
    

if __name__ == "__main__":
    manager = PollManager()
    poll_id = manager.create_poll("Best programming language?", ["Python", "Go", "Java", "JavaScript"])
    
    manager.vote(poll_id, "Python")
    manager.vote(poll_id, "Go")
    manager.vote(poll_id, "Python")
    
    print(manager.get_results(poll_id))
