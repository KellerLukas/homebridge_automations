from src.py.deployment.utils.remember_states import RememberStates
from src.py.deployment.scripts.remember_wohnzimmer.config import light_ids, memory_file, target_states



def main():
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