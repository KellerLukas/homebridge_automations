import os
from src.py.deployment.utils.remember_states import RememberStates
from src.py.deployment.scripts.remember_wohnzimmer.config import light_ids, memory_file



def main():
    rem_states = RememberStates(light_ids=light_ids)
    rem_states.record()
    rem_states.to_file(memory_file)
    os.remove(memory_file)
    
if __name__ == "__main__":
    main()