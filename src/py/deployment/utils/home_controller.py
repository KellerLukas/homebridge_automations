from typing import Dict
from phue import Bridge

CONFIGURABLE_PARAMETERS = ["on", "bri", "sat", "ct"]

class HomeController:
    def __init__(self, bridge_ip: str):
        self.bridge = Bridge(bridge_ip)
        self.bridge.connect()

    def get_state(self, light_id: str):
        state = self.bridge.get_light(light_id=light_id)['state']
        state = {key:val for key,val in state.items() if key in CONFIGURABLE_PARAMETERS}
        return state
        
    def set_state(self, light_id: str, state: Dict[str,str]):
        self.bridge.set_light(light_id=light_id, parameter=state)
