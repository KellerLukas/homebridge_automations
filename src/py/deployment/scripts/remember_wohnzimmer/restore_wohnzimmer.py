import os
import time
from src.py.deployment.utils.remember_states import RememberStates
from src.py.deployment.scripts.remember_wohnzimmer.config import memory_file, transition_time_s


def main():
    rem_states = RememberStates.from_file(memory_file)
    rem_states.restore(transition_time=transition_time_s)
    
    # in case of rapid pausing/unpausing we want to prevent recapturing the state until the previous one was fully restored
    time.sleep(transition_time_s) 
    os.remove(memory_file)


if __name__ == "__main__":
    main()
