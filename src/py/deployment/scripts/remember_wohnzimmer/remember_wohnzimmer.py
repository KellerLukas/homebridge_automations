from src.py.deployment.utils.remember_states import RememberStates
from src.py.deployment.scripts.remember_wohnzimmer.config import (
    light_ids,
    memory_file,
    target_states,
    transition_time_deciseconds,
)


def main():
    if RememberStates.file_exists(memory_file):
        rem_states = RememberStates.from_file(memory_file)
    else:
        rem_states = RememberStates(light_ids=light_ids)

    if not rem_states.is_valid:
        # we don't want to overwrite a valid recording (probably we are still transitioning back to the previous state)
        rem_states.record()

    if not all_turned_off(rem_states.states):
        rem_states.set_states(
            states=target_states,
            transition_time_decisenconds=transition_time_deciseconds,
        )

    rem_states.to_file(memory_file)


def all_turned_off(states: dict) -> bool:
    for state in states.values():
        if state["on"]:
            return False
    return True


if __name__ == "__main__":
    main()
