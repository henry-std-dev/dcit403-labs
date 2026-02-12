import asyncio
import random
from datetime import datetime
from fsm.fsm import FSM
import json


class SensorAgent:
    def __init__(self, jid, password, environment):
        self.jid = jid
        self.password = password
        self.event_log = []
        self.environment = environment
        self.fsm = FSM()

    def generate_event(self):
        """Generate a random disaster event from the environment."""
        return self.environment.generate_event()

    async def start(self):
        print(f"Sensor Agent {self.jid} starting...")
        for _ in range(5):  # Simulate 5 events over 30 seconds
            await asyncio.sleep(6)  # Simulate event every 6 seconds
            event = self.generate_event()
            print(f"[SENSOR {self.jid}] Generated event: {event}")
            self.event_log.append(event)
            # Send the event to other agents (simulated here as print statements)
            # e.g., send to rescue and coordinator agents

    async def stop(self):
        print(f"Sensor Agent {self.jid} stopping...")
        # Optionally, save the event log to a file
        with open(f"sensor_log_{self.jid}.json", "w") as f:
            json.dump(self.event_log, f, indent=2)
