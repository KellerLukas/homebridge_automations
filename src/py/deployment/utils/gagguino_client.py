import requests
from enum import Enum
from typing import Dict, Optional

# https://gaggiuino.github.io/#/rest-api/rest-api

URL = "http://gaggiuino.local"

class GaggiuinoStatusKeys(Enum):
    uptime = "upTime"
    profile_id = "profileId"
    profile_name = "profileName"
    target_temperature = "targetTemperature"
    temperature = "temperature"
    pressure = "pressure"
    water_level = "waterLevel"
    weight = "weight"
    brew_switch_state = "brewSwitchState"
    steam_switch_state = "steamSwitchState"

class GaggiuinoClient:
    def get_status(self) -> Dict[str, str]:
        response = requests.get(f"{URL}/api/system/status")
        res = response.json()
        if isinstance(res, list):
            return res[0]
        return res
    
    def is_brewing(self, status: Optional[dict] = None) -> bool:
        status = status or self.get_status()
        return status[GaggiuinoStatusKeys.brew_switch_state.value] == "true"
    
    def get_uptime(self, status: Optional[dict] = None) -> int:
        status = status or self.get_status()
        return int(status[GaggiuinoStatusKeys.uptime.value])
    