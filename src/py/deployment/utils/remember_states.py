from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union
import json
import time

from src.py.deployment.utils.home_controller import HomeController
from src.py.deployment.utils.config import HUE_BRIDGE_IP

@dataclass
class RememberStates:
    light_ids: List[str]
    states: Dict[str, Dict[str, Union[bool, int, float]]] = field(default_factory=dict)
    recorded_at: Optional[float] = None
    valid_until: Optional[float] = None
    controller: HomeController = HomeController(HUE_BRIDGE_IP)
        
    @property
    def age_of_recording(self) -> Optional[float]:
        if self.recorded_at is None:
            return None
        return time.time() - self.recorded_at
    
    @property
    def is_valid(self) -> bool:
        if self.recorded_at is None:
            return False
        if self.valid_until is None:
            return True
        return time.time() < self.valid_until

    def to_file(self, filename: str):
        with open(filename, "w") as f:
            # Exclude non-serializable controller field
            data = {k: v for k, v in self.__dict__.items() if k != "controller"}
            json.dump(data, f)
    
    @classmethod
    def from_file(cls, filename: str) -> "RememberStates":
        with open(filename, "r") as f:
            data = json.load(f)
        return cls(**data)
    
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
            self.recorded_at = time.time()

    def restore(self, transition_time_deciseconds: Optional[int] = None):
        for id in self.light_ids:
            self.controller.set_state(
                light_id=id, state=self.states[id], transition_time_deciseconds=transition_time_deciseconds
            )
        self.valid_until = time.time() + transition_time_deciseconds/10 if transition_time_deciseconds else time.time()

    def set_states(self, states: {}, transition_time_decisenconds: Optional[int]):
        for id in self.light_ids:
            self.controller.set_state(
                light_id=id, state=states[id], transition_time_deciseconds=transition_time_decisenconds
            )
