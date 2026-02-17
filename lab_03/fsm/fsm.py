class RescueFSM:
    def __init__(self):
        self.state = "IDLE"

    def transition(self, event):
        transitions = {
            ("IDLE", "DISASTER_REPORTED"): "RESCUE_IN_PROGRESS",
            ("RESCUE_IN_PROGRESS", "RESOURCES_NEEDED"): "WAITING_LOGISTICS",
            ("WAITING_LOGISTICS", "RESOURCES_RECEIVED"): "RESCUE_IN_PROGRESS",
            ("RESCUE_IN_PROGRESS", "TASK_COMPLETE"): "IDLE",
        }
        new_state = transitions.get((self.state, event))
        if new_state:
            self.state = new_state
        return self.state
