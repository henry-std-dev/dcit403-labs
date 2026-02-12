class FSM:
    def __init__(self):
        self.state = "Idle"

    def transition(self, event):
        if self.state == "Idle" and event == "start_task":
            self.state = "Active"
        elif self.state == "Active" and event == "waiting_for_resources":
            self.state = "Waiting"
        elif self.state == "Active" and event == "task_complete":
            self.state = "Completed"
        elif self.state == "Waiting" and event == "resources_received":
            self.state = "Active"
        elif self.state == "Completed" and event == "reset":
            self.state = "Idle"

    def get_state(self):
        return self.state
