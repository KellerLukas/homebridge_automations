import time

from src.py.deployment.utils.gagguino_client import GaggiuinoClient
from src.py.deployment.utils.home_controller import HomeController
from src.py.deployment.utils.config import HUE_BRIDGE_IP
from src.py.deployment.utils.pushcut import Pushcut

SHUT_OFF_AFTER_SECONDS = 1  # testing

def main():
    home_controller = HomeController(HUE_BRIDGE_IP)
    for i in range(2):
        if not turned_on_has_exceeded_runtime_and_not_brewing(home_controller):
            return
        home_controller.blink_light("Esstisch", count=3, delay=0.5)
        time.sleep(5)
    if turned_on_has_exceeded_runtime_and_not_brewing(home_controller):
        home_controller.set_state("Kaffeemaschine", {"on": False})
        Pushcut().send_notification(
            title="Kaffeemaschine",
            message="Kaffeemaschine ausgeschaltet",
        )
    
def turned_on_has_exceeded_runtime_and_not_brewing(home_controller: HomeController) -> bool:
    client = GaggiuinoClient()
    if not home_controller.get_state("Kaffeemaschine")["on"]:
        return False
    status = safely_get_status(client)
    uptime = client.get_uptime(status)
    
    if uptime < SHUT_OFF_AFTER_SECONDS:
        return False
    if client.is_brewing(status):
        return False
    return True
    
    
def safely_get_status(client: GaggiuinoClient):
    for iteration in range(2):
        try:
            return client.get_status()
        except ConnectionError as e:
            if iteration == 1:
                raise e
            # possibly still booting, wait and retry
            time.sleep(8)

if __name__ == "__main__":
    main()