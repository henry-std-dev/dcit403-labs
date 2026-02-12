import asyncio
import json

from environment import DisasterEnvironment
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour


class SensorAgent(Agent):
    class SensingBehaviour(PeriodicBehaviour):
        async def run(self):
            # Generate and perceive event
            event = self.agent.environment.generate_event()

            # Log the percept
            self.agent.log_event(event)

            print(f"[SENSOR {self.agent.jid}] Perceived: {event}")

    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.environment = DisasterEnvironment()
        self.event_log = []

    def log_event(self, event):
        """Store perceived events"""
        self.event_log.append(event)
        # Save to file
        with open(f"sensor_log_{self.jid.user}.json", "w") as f:
            json.dump(self.event_log, f, indent=2)

    async def setup(self):
        print(f"Sensor Agent {self.jid} starting...")

        # Sense period
        self.add_behaviour(self.SensingBehaviour(period=3))
