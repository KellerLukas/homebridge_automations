from src.py.deployment.utils.remember_states import RememberStates
from src.py.deployment.scripts.remember_wohnzimmer.config import (light_ids, memory_file,
    target_states, transition_time_s)


def main():
    rem_states = RememberStates(light_ids=light_ids)
    
    # don't overwrite a recording if there already is one
    if not RememberStates.file_exists(memory_file):
        rem_states.record()
        rem_states.to_file(memory_file)
        
    if not all_turned_off(rem_states.states):
        rem_states.set_states(states=target_states, transition_time=transition_time_s)


def all_turned_off(states: dict) -> bool:
    for state in states.values():
        if state["on"]:
            return False
    return True


if __name__ == "__main__":
    main()
