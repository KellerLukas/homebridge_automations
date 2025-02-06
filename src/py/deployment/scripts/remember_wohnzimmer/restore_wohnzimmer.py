import os
from src.py.deployment.utils.remember_states import RememberStates
from src.py.deployment.scripts.remember_wohnzimmer.config import memory_file

def main():
    rem_states = RememberStates.from_file(memory_file)
    rem_states.restore(transitiontime=50)
    os.remove(memory_file)

if __name__ == "__main__":
    main()
