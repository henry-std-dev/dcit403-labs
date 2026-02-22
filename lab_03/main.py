import asyncio
import logging

from config import (
    CONSUMER_JID,
    CONSUMER_PASSWORD,
    COORDINATOR_JID,
    COORDINATOR_PASSWORD,
    DEMAND_JID,
    DEMAND_PASSWORD,
    POWERPLANT_JID,
    POWERPLANT_PASSWORD,
    STORAGE_JID,
    STORAGE_PASSWORD,
)
from consumer_agent import ConsumerAgent
from coordinator import GridCoordinatorAgent
from demand_agent import DemandAgent
from logger_config import setup_logger
from powerplant import PowerPlantAgent
from storage_agent import StorageAgent


async def main():
    setup_logger()

    coordinator = GridCoordinatorAgent(COORDINATOR_JID, COORDINATOR_PASSWORD)
    powerplant = PowerPlantAgent(POWERPLANT_JID, POWERPLANT_PASSWORD)
    storage = StorageAgent(STORAGE_JID, STORAGE_PASSWORD)
    consumer = ConsumerAgent(CONSUMER_JID, CONSUMER_PASSWORD)
    demand = DemandAgent(DEMAND_JID, DEMAND_PASSWORD)

    await coordinator.start()
    await powerplant.start()
    await storage.start()
    await consumer.start()
    await demand.start()

    logging.info("All agents started.")
    await asyncio.sleep(90)  # Allow time for all events including failure

    await coordinator.stop()
    await powerplant.stop()
    await storage.stop()
    await consumer.stop()
    await demand.stop()


if __name__ == "__main__":
    asyncio.run(main())
