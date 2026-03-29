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

input_path = Path.cwd() / "input files"
output_path = Path.cwd() / "output files"

choice = None
print(utils.INTRO_MSG)
while choice != "e":
    print(utils.MENU_MSG(input_path, output_path))
    choice_list = ["i", "o", "t", "g", "e"]
    choice = utils.prompt_user(choice_list)

    if choice == "i": 
        input_path = utils.findFolder(input_path, "Input")
    if choice == "o": 
        output_path = utils.findFolder(output_path, "Output")
    if choice == "t": break #utils.targeted
    if choice == "g": break #utils.global
    if choice == "e": break #utils.save_csv