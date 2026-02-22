import logging

from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message

logger = logging.getLogger("GridCoordinator")


class GridCoordinatorAgent(Agent):
    async def setup(self):
        logger.info("GridCoordinatorAgent starting...")

        self.imbalance = 0
        self.emergency_active = False

        fsm = CoordinatorFSM()

        # States
        fsm.add_state("MONITORING", MonitoringState(), initial=True)
        fsm.add_state("EVALUATING", EvaluatingState())
        fsm.add_state("MINOR_BALANCING", MinorBalancingState())
        fsm.add_state("MODERATE_BALANCING", ModerateBalancingState())
        fsm.add_state("SEVERE_BALANCING", SevereBalancingState())
        fsm.add_state("EMERGENCY", EmergencyState())
        fsm.add_state("RECOVERY", RecoveryState())

        # Transitions
        fsm.add_transition("MONITORING", "MONITORING")
        fsm.add_transition("MONITORING", "EVALUATING")
        fsm.add_transition("MONITORING", "EMERGENCY")

        fsm.add_transition("EVALUATING", "MINOR_BALANCING")
        fsm.add_transition("EVALUATING", "MODERATE_BALANCING")
        fsm.add_transition("EVALUATING", "SEVERE_BALANCING")

        fsm.add_transition("MINOR_BALANCING", "MONITORING")
        fsm.add_transition("MODERATE_BALANCING", "MONITORING")
        fsm.add_transition("SEVERE_BALANCING", "MONITORING")

        fsm.add_transition("EMERGENCY", "RECOVERY")
        fsm.add_transition("RECOVERY", "MONITORING")

        self.add_behaviour(fsm)


class CoordinatorFSM(FSMBehaviour):
    pass


# ---------------- STATES ---------------- #
class MonitoringState(State):
    async def run(self):
        logger.info("State: MONITORING - waiting for event")
        msg = await self.receive(timeout=10)

        if not msg:
            logger.info("No event received.")
            self.set_next_state("MONITORING")
            return

        sender = str(msg.sender)
        body = msg.body.strip()

        # Ignore admin
        if "xmpp.jp" in sender and "admin" in body.lower():
            self.set_next_state("MONITORING")
            return

        # ---- ACK HANDLING ----
        if body.startswith("ack:command_executed"):
            logger.info("Acknowledgement received from PowerPlant.")
            self.set_next_state("MONITORING")
            return
        if body.startswith("ack:storage_executed"):
            logger.info("Acknowledgement received from StorageAgent.")
            self.set_next_state("MONITORING")
            return
        if body.startswith("ack:load_shed_executed"):
            logger.info("Acknowledgement received from ConsumerAgent.")
            self.set_next_state("MONITORING")
            return

        # ---- DEMAND / FAILURE EVENTS ----
        if ":" not in body:
            self.set_next_state("MONITORING")
            return

        event_type, value = body.split(":", 1)
        if event_type == "demand":
            try:
                self.agent.imbalance = int(value)
                logger.info(f"Demand imbalance received: {self.agent.imbalance}")
                self.set_next_state("EVALUATING")
            except ValueError:
                self.set_next_state("MONITORING")
        elif event_type == "failure":
            logger.warning("Failure detected! Activating emergency.")
            self.set_next_state("EMERGENCY")
        else:
            self.set_next_state("MONITORING")


class EvaluatingState(State):
    async def run(self):
        logger.info("State: EVALUATING")
        imbalance = self.agent.imbalance
        T1, T2 = 10, 20
        if imbalance < T1:
            self.set_next_state("MINOR_BALANCING")
        elif T1 <= imbalance < T2:
            self.set_next_state("MODERATE_BALANCING")
        else:
            self.set_next_state("SEVERE_BALANCING")


class MinorBalancingState(State):
    async def run(self):
        logger.info("State: MINOR BALANCING")
        msg = Message(to="powerplant@xmpp.jp")
        msg.body = "increase_generation_minor"
        await self.send(msg)
        logger.info("Command sent to PowerPlant.")
        self.set_next_state("MONITORING")


class ModerateBalancingState(State):
    async def run(self):
        logger.info("State: MODERATE BALANCING")
        msg1 = Message(to="powerplant@xmpp.jp")
        msg1.body = "increase_generation_moderate"
        await self.send(msg1)
        msg2 = Message(to="storageagent@xmpp.jp")
        msg2.body = "discharge_moderate"
        await self.send(msg2)
        logger.info("Commands sent to PowerPlant and Storage.")
        self.set_next_state("MONITORING")


class SevereBalancingState(State):
    async def run(self):
        logger.info("State: SEVERE BALANCING")
        msg1 = Message(to="powerplant@xmpp.jp")
        msg1.body = "activate_backup"
        await self.send(msg1)
        msg2 = Message(to="storageagent@xmpp.jp")
        msg2.body = "discharge_severe"
        await self.send(msg2)
        msg3 = Message(to="consumeragent@xmpp.jp")
        msg3.body = "load_shed"
        await self.send(msg3)
        logger.info("Emergency commands sent to PowerPlant, Storage, and Consumer.")
        self.set_next_state("MONITORING")


class EmergencyState(State):
    async def run(self):
        logger.info("State: EMERGENCY - sending emergency signals")
        # Notify all agents
        for to_jid, body in [
            ("powerplant@xmpp.jp", "emergency_shutdown"),
            ("storageagent@xmpp.jp", "emergency_mode"),
            ("consumeragent@xmpp.jp", "critical_load_reduction"),
        ]:
            msg = Message(to=to_jid)
            msg.body = body
            await self.send(msg)
        logger.warning("Emergency protocol activated.")
        self.set_next_state("RECOVERY")


class RecoveryState(State):
    async def run(self):
        logger.info("State: RECOVERY - stabilizing system")
        self.agent.imbalance = 0
        logger.info("System stabilized. Returning to monitoring.")
        self.set_next_state("MONITORING")
