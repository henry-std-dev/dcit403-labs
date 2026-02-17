import asyncio
import datetime

from fsm.fsm import RescueFSM


class BaseAgent:
    def __init__(self, jid, password):
        self.jid = jid
        self.password = password
        self.log_file = f"log_{self.jid.split('@')[0]}.txt"
        # Clear log file at start
        with open(self.log_file, "w") as f:
            f.write(f"--- Log Session Started: {datetime.datetime.now()} ---\n")

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] [{self.jid}] {message}"
        print(entry)
        with open(self.log_file, "a") as f:
            f.write(entry + "\n")


class SensorAgent(BaseAgent):
    async def sense_and_report(self, env, coordinator):
        self.log("Initializing sensors...")
        await asyncio.sleep(1)
        percept = env.generate_event()
        self.log(
            f"ENVIRONMENT ALERT: {percept['event_type']} detected at {percept['location']}. Urgency: {percept['urgency']}"
        )

        self.log(f"Communicating with Coordinator...")
        await asyncio.sleep(1.5)  # Simulate network delay
        return percept


class CoordinatorAgent(BaseAgent):
    async def receive_report(self, report, sender):
        self.log(f"Analyzing data received from {sender}...")
        await asyncio.sleep(2)  # Simulate deliberation time

        if report["urgency"] in ["High", "Immediate"]:
            self.log(
                f"DECISION: High Priority. Deploying Rescue Units to {report['location']}."
            )
            return report
        else:
            self.log(
                f"DECISION: Low Priority. Monitoring situation at {report['location']}."
            )
            return None


class RescueAgent(BaseAgent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.fsm = RescueFSM()

    async def react_to_disaster(self, disaster_data):
        self.log(f"Current State: {self.fsm.state}. Goal: STANDBY.")

        # Transition 1
        self.fsm.transition("DISASTER_REPORTED")
        self.log(f"EVENT TRIGGERED: Disaster Reported. New State: {self.fsm.state}")
        self.log(f"ACTION: Mobilizing team for {disaster_data['location']}...")
        await asyncio.sleep(3)  # Simulate travel time

        # Transition 2
        self.fsm.transition("RESOURCES_NEEDED")
        self.log(f"STATE CHANGE: {self.fsm.state}. Identifying resource gaps...")
        await asyncio.sleep(1.5)
        self.log("REQUEST: Sending broadcast for Medical Supplies.")

        # Transition 3: Simulate task completion
        await asyncio.sleep(2)
        self.fsm.transition("TASK_COMPLETE")
        self.log(
            f"FINAL STATE: {self.fsm.state}. Goal: RESCUE_SUCCESS. Returning to base."
        )
