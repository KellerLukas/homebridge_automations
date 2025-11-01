import json
import time
from typing import List, Optional

from src.py.deployment.utils.home_controller import HomeController
from src.py.deployment.utils.config import HUE_BRIDGE_IP

TIMESTAMP_KEY = "timestamp"

class RememberStates:
    def __init__(self, light_ids: List[str]):
        self.light_ids = light_ids
        self.states = {}
        self.timestamp = None
        self.controller = HomeController(HUE_BRIDGE_IP)
        
    @property
    def age(self) -> Optional[float]:
        if self.timestamp is None:
            return None
        return time.time() - self.timestamp
    
    @classmethod
    def from_file(cls, filename: str):
        with open(filename, "r") as f:
            states = json.load(f)
        timestamp = states.pop(TIMESTAMP_KEY, None)
        ids = list(states.keys())
        rem_states = cls(ids)
        rem_states.timestamp = timestamp
        rem_states.states.update(states)
        return rem_states
    
    def to_file(self, filename: str):
        with open(filename, "w") as f:
            dump = self.states.copy()
            dump[TIMESTAMP_KEY] = self.timestamp
            json.dump(dump, f)
    
    @staticmethod
    def file_exists(filename: str) -> bool:
        try:
            with open(filename, "r"):
                return True
        except FileNotFoundError:
            return False
        
    def record(self):
        for id in self.light_ids:
            self.states[id] = self.controller.get_state(light_id=id)
            self.timestamp = time.time()
    
    def restore(self, transitiontime: Optional[int]=None):
        for id in self.light_ids:
            self.controller.set_state(light_id=id, state=self.states[id], transitiontime=transitiontime)
            
    def set_states(self, states: {}, transitiontime: Optional[int]):
        for id in self.light_ids:
            self.controller.set_state(light_id=id, state=states[id], transitiontime=transitiontime)