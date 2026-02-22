# powerplant.py

import asyncio

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message


class PowerPlantAgent(Agent):

    async def setup(self):
        print("PowerPlantAgent starting...")
        self.add_behaviour(PowerPlantBehaviour())


class PowerPlantBehaviour(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=10)

        if not msg:
            await asyncio.sleep(1)
            return

        sender = str(msg.sender)
        body = msg.body.strip()

        # Ignore admin broadcasts
        if "xmpp.jp" in sender and "admin" in body.lower():
            return

        # Ignore acknowledgements
        if body.startswith("ack:"):
            return

        # Only accept commands from coordinator
        if "gridcoordinator@xmpp.jp" not in sender:
            return

        print(f"\nPowerPlant received command: {body}")

        valid_command = True

        if body == "increase_generation_minor":
            print("Action: Increasing generation slightly.")

        elif body == "increase_generation_moderate":
            print("Action: Increasing generation significantly.")

        elif body == "activate_backup":
            print("Action: Activating backup generators.")

        else:
            print("Unknown command received.")
            valid_command = False

        if valid_command:
            reply = Message(to="gridcoordinator@xmpp.jp")
            reply.body = "ack:command_executed"
            await self.send(reply)
