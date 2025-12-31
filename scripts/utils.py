from pathlib import Path

### messages
TASKS_MSG = \
    f"--- Tasks ---\n" \
    f"[I] Set Input Path\n" \
    f"[O] Set Output Path\n" \
    f"[T] Convert to Targeted\n" \
    f"[G] Convert to Global\n" \
    f"[E] Export file and exit"

PATHS_MSG = lambda i, o: \
    f"--- Paths ---\n" \
    f"Input Path\n" \
    f"- {i}\n" \
    f"Output Path\n" \
    f"- {o}"

SEARCH_MSG_IN = \
    f"--- Task: Set Input Path ---\n"\
    f"- Build the path to the INPUT folder.\n" \
    f"- Save the path to end the task.\n" \
    f"--- Commands ---\n" \
    f"[E] Exit task without saving\n" \
    f"[S] Save path and end task\n" \
    f"[U] Navigate up (parent folder)"

SEARCH_MSG_OUT = \
    f"--- Task: Set Output Path ---\n"\
    f"> Construct the path to the OUTPUT folder.\n" \
    f"> Save the path to end the task.\n" \
    f"--- Commands ---\n" \
    f"[E] Exit task without saving\n" \
    f"[S] Save path and end task\n" \
    f"[U] Navigate up (parent folder)"

def validate_path(path, verbose=False):
    if Path(path).exists(): 
        if verbose: print(f"--- Path ---" + "\n" + f"- {Path(path)}")
        return Path(path)
    else:
        ERROR_MSG_PATH = \
        f"- Error: Unrecognized Path" \
        f"\n\"{path}\"\n" \
        f"- Exiting task."
        print(ERROR_MSG_PATH)
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

### navigation
def findFolder(input_path, MSG):
    ### validate input path, exit if invalid
    current_path = validate_path(input_path, verbose=False)
    if not current_path: return None
    
    ### print directions
    print(MSG)
    
    ### list subfolders: [#] folder_name
    folder_list = list_subfolders(current_path, verbose=True)
    
    ### print path
    validate_path(current_path, verbose=True)

    ### prompt user for path choice
    print("--- To select option [#] enter # ---")
    choice_list = ["e", "s", "u"] + [str(i) for i in range(len(folder_list))]
    choice = prompt_user(choice_list)

    ### interpret choice
    if choice.lower() == "e": 
        return(None)
    if choice.lower() == "s": 
        return(current_path)
    if choice.lower() == "u": 
        return(findFolder(current_path.parent, MSG))
    if choice.isnumeric():
        return(findFolder(current_path/folder_list[int(choice)], MSG))

    ERROR_MSG_CHOICE = \
        f"- Error: Unrecognized Choice " \
        f"\n\"{choice}\"\n" \
        f"- Exiting Task."
    print(ERROR_MSG_CHOICE)

    return(None)