import time
from typing import Dict, Optional
from phue import Bridge

CONFIGURABLE_PARAMETERS = ["on", "bri", "sat", "ct"]


class HomeController:
    def __init__(self, bridge_ip: str):
        self.bridge = Bridge(bridge_ip)
        self.bridge.connect()

    def get_state(self, light_id: str):
        state = self.bridge.get_light(light_id=light_id)["state"]
        state = {
            key: val for key, val in state.items() if key in CONFIGURABLE_PARAMETERS
        }
        return state

    def set_state(
        self, light_id: str, state: Dict[str, str], transitiontime: Optional[int] = None
    ):
        self.bridge.set_light(
            light_id=light_id, parameter=state, transitiontime=transitiontime
        )

    def blink_light(self, light_id: str, count: int, delay: int):
        previous_state = self.get_state(light_id)
        state_on = {"on": True, "bri": 100}
        state_off = {"on": False}

        self.set_state(light_id, state_off)
        for _ in range(count):
            time.sleep(delay)
            self.set_state(light_id, state=state_on, transitiontime=0)
            time.sleep(delay)
            self.set_state(light_id, state=state_off, transitiontime=0)
        time.sleep(delay)
        self.set_state(light_id, previous_state)
