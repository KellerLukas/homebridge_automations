from src.py.deployment.utils.remember_states import RememberStates
from src.py.deployment.scripts.remember_wohnzimmer.config import (
    light_ids,
    memory_file,
    target_states,
)


def main():
    if RememberStates.file_exists(memory_file):
        # apparently some bug in the homebridge script running plugin causes this script to be run twice in a row
        # so we just exit if the memory file already exists, to avoid overwriting the previous state with the current one
        if RememberStates.from_file(memory_file).age < 2:
            # to prevent locking in the on state, only skip if the file is very recent
            return
    rem_states = RememberStates(light_ids=light_ids)
    rem_states.record()
    rem_states.to_file(memory_file)
    if not all_turned_off(rem_states.states):
        rem_states.set_states(states=target_states, transitiontime=60)


def all_turned_off(states: dict) -> bool:
    for state in states.values():
        if state["on"]:
            return False
    return True


if __name__ == "__main__":
    main()
