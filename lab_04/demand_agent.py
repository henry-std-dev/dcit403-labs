import asyncio
import logging
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message

logger = logging.getLogger("DemandAgent")


class DemandAgent(Agent):
    async def setup(self):
        logger.info("DemandAgent starting...")
        self.add_behaviour(SendDemandBehaviour())


class SendDemandBehaviour(OneShotBehaviour):

    async def send_demand(self, value):
        msg = Message(to="gridcoordinator@xmpp.jp")
        msg.set_metadata("performative", "inform")
        msg.set_metadata("type", "demand")
        msg.body = str(value)
        await self.send(msg)
        logger.info(f"INFORM demand={value}")

    async def send_failure(self):
        msg = Message(to="gridcoordinator@xmpp.jp")
        msg.set_metadata("performative", "inform")
        msg.set_metadata("type", "failure")
        msg.body = "powerplant"
        await self.send(msg)
        logger.warning("INFORM failure=powerplant")

    async def run(self):
        await asyncio.sleep(5)

        await self.send_demand(5)
        await asyncio.sleep(8)

        await self.send_demand(15)
        await asyncio.sleep(8)

        await self.send_demand(30)
        await asyncio.sleep(8)

        await self.send_failure()