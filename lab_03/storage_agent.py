# storage_agent.py

import asyncio

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message


class StorageAgent(Agent):

    async def setup(self):
        print("StorageAgent starting...")
        self.energy_level = 100  # initial battery level
        self.add_behaviour(StorageBehaviour())


class StorageBehaviour(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=10)

        if not msg:
            await asyncio.sleep(1)
            return

        sender = str(msg.sender)
        body = msg.body.strip()

        # Ignore admin messages
        if "xmpp.jp" in sender and "admin" in body.lower():
            return

        # Ignore ACK loops
        if body.startswith("ack:"):
            return

        # Only accept commands from coordinator
        if "gridcoordinator@xmpp.jp" not in sender:
            return

        print(f"\nStorageAgent received command: {body}")

        valid_command = True

        if body == "discharge_moderate":
            if self.agent.energy_level >= 20:
                self.agent.energy_level -= 20
                print("Action: Moderate discharge (20 units).")
            else:
                print("Insufficient energy for moderate discharge.")

        elif body == "discharge_severe":
            if self.agent.energy_level >= 40:
                self.agent.energy_level -= 40
                print("Action: Severe discharge (40 units).")
            else:
                print("Insufficient energy for severe discharge.")

        else:
            print("Unknown command.")
            valid_command = False

        if valid_command:
            reply = Message(to="gridcoordinator@xmpp.jp")
            reply.body = "ack:storage_executed"
            await self.send(reply)
