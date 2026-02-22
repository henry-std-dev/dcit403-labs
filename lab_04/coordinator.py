import logging
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message

logger = logging.getLogger("GridCoordinator")


class GridCoordinatorAgent(Agent):
    async def setup(self):
        logger.info("GridCoordinatorAgent starting...")

        self.imbalance = 0

        fsm = CoordinatorFSM()

        fsm.add_state("MONITORING", MonitoringState(), initial=True)
        fsm.add_state("EVALUATING", EvaluatingState())
        fsm.add_state("MINOR_BALANCING", MinorBalancingState())
        fsm.add_state("MODERATE_BALANCING", ModerateBalancingState())
        fsm.add_state("SEVERE_BALANCING", SevereBalancingState())
        fsm.add_state("EMERGENCY", EmergencyState())
        fsm.add_state("RECOVERY", RecoveryState())

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


# ================= STATES ================= #

class MonitoringState(State):
    async def run(self):
        logger.info("State: MONITORING - waiting for event")
        msg = await self.receive(timeout=10)

        if not msg:
            logger.info("No event received.")
            self.set_next_state("MONITORING")
            return

        performative = msg.get_metadata("performative")
        msg_type = msg.get_metadata("type")

        if performative == "inform":

            if msg_type == "ack":
                logger.info(f"ACK received from {msg.sender}: {msg.body}")
                self.set_next_state("MONITORING")
                return

            if msg_type == "demand":
                try:
                    self.agent.imbalance = int(msg.body)
                    logger.info(f"Demand received: {self.agent.imbalance}")
                    self.set_next_state("EVALUATING")
                    return
                except ValueError:
                    self.set_next_state("MONITORING")
                    return

            if msg_type == "failure":
                logger.warning("Failure detected! Activating EMERGENCY.")
                self.set_next_state("EMERGENCY")
                return

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
        logger.info("State: MINOR_BALANCING")

        msg = Message(to="powerplant@xmpp.jp")
        msg.set_metadata("performative", "request")
        msg.set_metadata("type", "action")
        msg.body = "increase_generation_minor"

        await self.send(msg)

        self.set_next_state("MONITORING")


class ModerateBalancingState(State):
    async def run(self):
        logger.info("State: MODERATE_BALANCING")

        commands = [
            ("powerplant@xmpp.jp", "increase_generation_moderate"),
            ("storageagent@xmpp.jp", "discharge_moderate"),
        ]

        for to_jid, command in commands:
            msg = Message(to=to_jid)
            msg.set_metadata("performative", "request")
            msg.set_metadata("type", "action")
            msg.body = command
            await self.send(msg)

        self.set_next_state("MONITORING")


class SevereBalancingState(State):
    async def run(self):
        logger.info("State: SEVERE_BALANCING")

        commands = [
            ("powerplant@xmpp.jp", "activate_backup"),
            ("storageagent@xmpp.jp", "discharge_severe"),
            ("consumeragent@xmpp.jp", "load_shed"),
        ]

        for to_jid, command in commands:
            msg = Message(to=to_jid)
            msg.set_metadata("performative", "request")
            msg.set_metadata("type", "action")
            msg.body = command
            await self.send(msg)

        self.set_next_state("MONITORING")


class EmergencyState(State):
    async def run(self):
        logger.warning("State: EMERGENCY")

        commands = [
            ("powerplant@xmpp.jp", "emergency_shutdown"),
            ("storageagent@xmpp.jp", "emergency_mode"),
            ("consumeragent@xmpp.jp", "critical_load_reduction"),
        ]

        for to_jid, command in commands:
            msg = Message(to=to_jid)
            msg.set_metadata("performative", "request")
            msg.set_metadata("type", "emergency")
            msg.body = command
            await self.send(msg)

        self.set_next_state("RECOVERY")


class RecoveryState(State):
    async def run(self):
        logger.info("State: RECOVERY")
        self.agent.imbalance = 0
        logger.info("System stabilized.")
        self.set_next_state("MONITORING")