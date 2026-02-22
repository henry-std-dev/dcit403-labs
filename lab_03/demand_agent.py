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
    async def run(self):
        await asyncio.sleep(5)  # wait for all agents to connect

        # MINOR
        msg1 = Message(to="gridcoordinator@xmpp.jp")
        msg1.body = "demand:5"
        logger.info("Sending demand:5 (MINOR)")
        await self.send(msg1)

        await asyncio.sleep(8)

        # MODERATE
        msg2 = Message(to="gridcoordinator@xmpp.jp")
        msg2.body = "demand:15"
        logger.info("Sending demand:15 (MODERATE)")
        await self.send(msg2)

        await asyncio.sleep(8)

        # SEVERE
        msg3 = Message(to="gridcoordinator@xmpp.jp")
        msg3.body = "demand:30"
        logger.info("Sending demand:30 (SEVERE)")
        await self.send(msg3)

        await asyncio.sleep(8)

        # FAILURE EVENT
        msg4 = Message(to="gridcoordinator@xmpp.jp")
        msg4.body = "failure:powerplant"
        logger.warning("Sending failure:powerplant")
        await self.send(msg4)
