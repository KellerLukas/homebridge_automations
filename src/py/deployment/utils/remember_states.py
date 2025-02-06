import json
from typing import List, Optional

from src.py.deployment.utils.home_controller import HomeController
from src.py.deployment.utils.config import HUE_BRIDGE_IP

class RememberStates:
    def __init__(self, light_ids: List[str]):
        self.light_ids = light_ids
        self.states = {}
        self.controller = HomeController(HUE_BRIDGE_IP)
    
    @classmethod
    def from_file(cls, filename: str):
        with open(filename, "r") as f:
            states = json.load(f)
        ids = list(states.keys())
        rem_states = cls(ids)
        rem_states.states.update(states)
        return rem_states
    
    def to_file(self, filename: str):
        with open(filename, "w") as f:
            json.dump(self.states, f)
        
        
    def record(self):
        for id in self.light_ids:
            self.states[id] = self.controller.get_state(light_id=id)
    
    def restore(self, transitiontime: Optional[int]=None):
        for id in self.light_ids:
            self.controller.set_state(light_id=id, state=self.states[id], transitiontime=transitiontime)
            
    def set_states(self, states: {}, transitiontime: Optional[int]):
        for id in self.light_ids:
            self.controller.set_state(light_id=id, state=states[id], transitiontime=transitiontime)