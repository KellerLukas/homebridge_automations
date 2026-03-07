import os
import time
from src.py.deployment.utils.remember_states import RememberStates
from src.py.deployment.scripts.remember_wohnzimmer.config import memory_file, transition_time_deciseconds


def main():
    if not RememberStates.file_exists(memory_file):
        return
    
    rem_states = RememberStates.from_file(memory_file)
    rem_states.restore(transition_time_deciseconds=transition_time_deciseconds)


if __name__ == "__main__":
    main()
