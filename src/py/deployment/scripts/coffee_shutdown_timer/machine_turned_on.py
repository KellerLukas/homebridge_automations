import time

from src.py.deployment.utils.gaggiuino_client import GaggiuinoClient
from src.py.deployment.utils.home_controller import HomeController
from src.py.deployment.utils.config import HUE_BRIDGE_IP
from src.py.deployment.utils.pushcut import Pushcut

# THIS RUNS AS A CRON JOB EVERY 5 MINUTES AND NOT THROUGH HOMEBRIDGE

SHUT_OFF_AFTER_SECONDS = 30 * 60  # 30 minutes


def main():
    home_controller = HomeController(HUE_BRIDGE_IP)
    blink_loops = 2
    for i in range(blink_loops + 1):
        if not (
            has_exceeded_runtime_and_not_brewing(home_controller)
            or has_exceeded_runtime_by_very_much(home_controller)
        ):
            return
        if i == blink_loops:
            home_controller.set_state("Kaffeemaschine", {"on": False})
            Pushcut().send_notification(
                title="Kaffeemaschine",
                message="Kaffeemaschine ausgeschaltet",
            )
        home_controller.blink_light("Esstisch", count=3, delay=0.5)
        time.sleep(5)


def has_exceeded_runtime_and_not_brewing(
    home_controller: HomeController,
) -> bool:
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


def has_exceeded_runtime_by_very_much(
    home_controller: HomeController,
) -> bool:
    # if the machine is on for a very long time, we want to shut it off even if it is brewing, we might have forgotten to turn off the brew switch
    client = GaggiuinoClient()
    if not home_controller.get_state("Kaffeemaschine")["on"]:
        return False
    status = safely_get_status(client)
    uptime = client.get_uptime(status)

    if uptime < SHUT_OFF_AFTER_SECONDS * 2:
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
