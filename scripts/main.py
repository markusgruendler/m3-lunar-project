import numpy as np
import pandas as pd
from pathlib import Path

import utils

### choose from
# input path
# output path
# anything -> targeted
# targeted -> global
# export file

input_path = None
output_path = None

choice = None
while choice != "e":
    print(utils.PATHS_MSG(input_path, output_path))
    print(utils.TASKS_MSG)
    choice_list = ["i", "o", "t", "g", "e"]
    choice = utils.prompt_user(choice_list)

    if choice == "i": 
        input_path = utils.findFolder(Path.cwd(), utils.SEARCH_MSG_IN)
    if choice == "o": 
        output_path = utils.findFolder(Path.cwd(), utils.SEARCH_MSG_OUT)
    if choice == "t": break #utils.targeted
    if choice == "g": break #utils.global
    if choice == "e": break #utils.save_csv