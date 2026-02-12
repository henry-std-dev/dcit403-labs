import asyncio
import random
import json


class RescueAgent:
    def __init__(self, jid, password):
        self.jid = jid
        self.password = password
        self.rescue_log = []

    def process_event(self, event):
        """Process the event and simulate a rescue action."""
        print(f"[RESCUE {self.jid}] Processing event: {event}")
        rescue_info = {
            "event": event,
            "action_taken": "Rescue in progress",
            "rescued_victims": random.randint(0, 5),
        }
        self.rescue_log.append(rescue_info)
        return rescue_info

    async def start(self, sensor_agent):
        print(f"Rescue Agent {self.jid} starting...")
        for event in sensor_agent.event_log:
            await asyncio.sleep(3)  # Simulate some delay for rescue operations
            rescue_info = self.process_event(event)
            print(f"[RESCUE {self.jid}] Rescue Info: {rescue_info}")

    async def stop(self):
        print(f"Rescue Agent {self.jid} stopping...")
        with open(f"rescue_log_{self.jid}.json", "w") as f:
            json.dump(self.rescue_log, f, indent=2)
