import asyncio
import json
import random


class CoordinatorAgent:
    def __init__(self, jid, password):
        self.jid = jid
        self.password = password
        self.coordination_log = []

    def coordinate_rescue(self, rescue_agent, logistics_agent):
        """Simulate the coordination of rescue operations."""
        print(f"[COORDINATOR {self.jid}] Coordinating rescue operations.")
        for rescue_info in rescue_agent.rescue_log:
            logistics_agent.handle_request("Medical Supplies", random.randint(5, 20))
            coordination = {
                "rescue_event": rescue_info["event"],
                "coordinated_with": "Logistics Agent",
                "action": "Coordinated rescue and resources",
            }
            self.coordination_log.append(coordination)
        return self.coordination_log

    async def start(self, rescue_agent, logistics_agent):
        print(f"Coordinator Agent {self.jid} starting...")
        await asyncio.sleep(2)
        coordination = self.coordinate_rescue(rescue_agent, logistics_agent)
        print(f"[COORDINATOR {self.jid}] Coordination Log: {coordination}")

    async def stop(self):
        print(f"Coordinator Agent {self.jid} stopping...")
        with open(f"coordination_log_{self.jid}.json", "w") as f:
            json.dump(self.coordination_log, f, indent=2)
