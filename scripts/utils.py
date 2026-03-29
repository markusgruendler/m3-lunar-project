from pathlib import Path

### messages
INTRO_MSG = \
    f"--- Introduction ---\n" \
    f"This python script lets you convert delimited text data to Targeted and Global formats.\n" \
    f"Input and output paths default to the included \"input files\" and \"output files\" folders and can be modified below.\n" \
    f"To select the menu option beginning with [#], enter # (i.e. enter I for [I] Set Input Path)."

MENU_MSG = lambda i,o: \
    f"\n--- Menu ---\n" \
    f"[I] Set Input Path: {i}\n" \
    f"[O] Set Output Path: {o}\n" \
    f"[T] Convert to Targeted\n" \
    f"[G] Convert to Global\n" \
    f"[E] Export file and exit"

# SEARCH_MSG_OUT = \
#     f"--- Set Output Path ---\n" \
#     f"> Construct the path to the OUTPUT folder (where the files will be exported to).\n" \
#     f"> Save or exit to return to the menu.\n" \
#     f"--- Menu ---\n" \
#     f"[E] Exit task without saving\n" \
#     f"[S] Save path and end task\n" \
#     f"[U] Navigate up (parent folder)"

SEARCH_MSG = lambda t,p: \
    f"\n--- Set {t} Path ---\n" \
    f"- Current path: {p}\n" \
    f"- Modify the above path to match the desired {t.upper()} folder location.\n" \
    f"- Exit or save to return to the main menu. Navigate up to remove the last folder and add a folder by entering its corresponding number from the list below.\n" \
    f"--- Path Menu ---\n" \
    f"[E] Exit without saving\n" \
    f"[S] Save path\n" \
    f"[U] Navigate up (parent folder)"

ERROR_MSG_PATH = lambda p:\
        f"- Error: Unrecognized Path" \
        f"\n\"{p}\"\n" \
        f"- Exiting."

### methods
def validate_path(path, verbose=False):
    if Path(path).exists(): 
        if verbose: print(f"--- Path ---" + "\n" + f"- {Path(path)}")
        return Path(path)
    else:
        return None

def list_subfolders(path, verbose=False):
    folder_list = [f for f in path.iterdir() if f.is_dir()]
    if verbose:
        print("--- Folders ---")
        if len(folder_list) == 0: print("[#] No folders found in path.")
        for c, i in enumerate(folder_list): print(f"[{c}] {i.name}")
    return folder_list

def prompt_user(choice_list, prompt_msg="> ", error_msg=""):
    choice = input(prompt_msg).lower()
    while choice not in choice_list:
        print(error_msg)
        choice = input(prompt_msg).lower()
    return choice

def findFolder(input_path, type):
    ### validate input path and exit if invalid
    current_path = validate_path(input_path, verbose=False)
    if not current_path:
        print(ERROR_MSG_PATH(input_path))
        return None
    
    ### print search message
    print(SEARCH_MSG(type, input_path))
    
    ### list subfolders: [#] folder_name
    folder_list = list_subfolders(current_path, verbose=True)

    ### prompt user for path choice
    # print("--- To select option [#] enter # ---")
    choice_list = ["e", "s", "u"] + [str(i) for i in range(len(folder_list))]
    choice = prompt_user(choice_list)

    ### interpret choice
    if choice.lower() == "e": 
        return(input_path)
    if choice.lower() == "s": 
        return(current_path)
    if choice.lower() == "u":
        return(findFolder(current_path.parent, type))
    if choice.isnumeric():
        return(findFolder(current_path/folder_list[int(choice)], type))

    ERROR_MSG_CHOICE = \
        f"- Error: Unrecognized Choice " \
        f"\n\"{choice}\"\n" \
        f"- Exiting Task."
    print(ERROR_MSG_CHOICE)

    return(None)