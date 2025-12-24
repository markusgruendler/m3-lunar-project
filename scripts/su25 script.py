# M3: Targeted to Global Conversion


### imports
import numpy as np
import pandas as pd
from pathlib import Path


### methods/statics
def targeted_to_global(wavelengths, values, verbose = False):
    # average 4 at a time
    # set step size to last breakpoint
    # increment by step size
    # round to 4 decimals

    WIDTH = 7
    if verbose: print(f"{'wl':>{WIDTH}}: step, index change")

    i = 0 # input index
    bp_idx = 0
    output = {"wavelengths": [], "values": []}
    while i+3 < len(wavelengths):
        # average over next 4
        avg_wl = np.round(np.mean(wavelengths[i:i+4]),4)
        avg_values = np.round(np.mean(values[i:i+4]),4)

        # if next step exists
        # and current wl > bp_idx wl
        while bp_idx + 1 < len(breakpoints["step"]) and wavelengths[i] > breakpoints["wl"][bp_idx]:
            bp_idx += 1
            if verbose: print(f"{wavelengths[i]:{WIDTH}.{WIDTH-2}f}: {breakpoints['step'][bp_idx-1]}->{breakpoints['step'][bp_idx]}, {bp_idx-1}->{bp_idx}")

        # save and increment by values consumed
        output["wavelengths"].append(avg_wl)
        output["values"].append(avg_values)
        i += breakpoints["step"][bp_idx]
    
    output["wavelengths"] = np.array(output["wavelengths"])
    output["values"] = np.array(output["values"])
    return output

def findFolder(input_path, SEARCH_MSG):
    current_path = Path(input_path)
    if not current_path.exists(): return("Invalid Path")
    
    print(f"Current path: {current_path}")
    print(SEARCH_MSG)
    
    # list out folders with [#] as identifier
    folder_list = [f for f in current_path.iterdir() if f.is_dir()]
    print("> Folders in current folder:")
    if len(folder_list) == 0: print("[#] No folders found.")
    for c, i in enumerate(folder_list):
        print(f"[{c}] {i.name}")
    # print("")

    choice = input(f"> To select option [#], enter #: ").lower()
    while choice not in ["e", "s", "u"] + [str(i) for i in range(len(folder_list))]:
        choice = input("Couldn't read input, trying again. Target #: ").lower()

    if choice.lower() == "e": return("Exiting.")
    if choice.lower() == "s": return(current_path)
    if choice.lower() == "u": return(findFolder(current_path.parent, SEARCH_MSG))
    if choice.isnumeric() and int(choice) in range(len(folder_list)):
        current_path = current_path / folder_list[int(choice)]
        if current_path.is_dir():
            return(findFolder(current_path, SEARCH_MSG))

    return("Error reading path, exiting.")

SEARCH_MSG_IN = \
    f"> Construct the path to the INPUT folder with the csv files to be converted.\n" \
    f"> Save the current path to end search.\n" \
    f"> To select option [#], enter #.\n" \
    f"[E] Exit without saving\n" \
    f"[S] Save current path\n" \
    f"[U] Search up one level"

SEARCH_MSG_OUT = \
    f"> Construct the path to the OUTPUT folder where the csv files will be saved.\n" \
    f"> Save the current path to end search.\n" \
    f"> To select option [#], enter #.\n" \
    f"[E] Exit without saving\n" \
    f"[S] Save current path\n" \
    f"[U] Search up one level"

ERROR_MSG_CONT = \
    f"> Error, continuing to next file."

ERROR_MSG_EXIT = \
    f"> Error, exiting."


### io paths
print(f"[1/2] Declare input folder path.")
input_folder = findFolder(Path.cwd(), SEARCH_MSG_IN)
if type(input_folder) == str:
    print(f"Exiting program.")
    exit()
file_paths_list = [f for f in input_folder.iterdir() if f.is_file() and f.suffix == ".csv"]
print(f"[1/2] Saved input folder path, {len(file_paths_list)} files found.\n")

print(f"[2/2] Declare output folder path.")
output_folder = findFolder(Path.cwd(), SEARCH_MSG_OUT)
if type(output_folder) == str:
    print(f"Exiting program.")
    exit()
print(f"[2/2] Saved output folder path.\n")


### init constants
# process:
# change step size if past a breakpoint
# format:
# current wl, step to transition to
breakpoints = {
    "wl"   : [0, 0.44, 0.68, 0.71, 1.53, 1.56, 1.60], # 9999],
    "step" : [0,    4,    4,    3,    2,    3,    4]  #    4]
}


### file processing loop
for file_counter, file_path in enumerate(file_paths_list):
    ### load data
    print(f"[{file_counter+1}/{len(file_paths_list)}] Loading '{file_path.name}' from folder '{input_folder.name}'")
    df = pd.read_csv(file_path).dropna()

    WL_COL = -1
    REFL_COL = -1

    try:
        if len(df.columns) < 2: raise ValueError(f"{len(df.columns)} of minimum 2 columns found")
    except Exception as e:
        print(f"> Insufficient columns, {e}")
        print(ERROR_MSG_CONT)
        continue
    print(f"[#] column name")
    for i in range(len(df.columns)):
        print(f"[{i}] {df.columns[i]}")

    try:
        ans = input('Select wavelength column #: ')
        WL_COL = int(ans)
        if WL_COL not in range(len(df.columns)):
            raise ValueError(f"{ans} out of column range")
        else:
            print(f"> Selected [{ans}] {df.columns[WL_COL]} for wavelength column")
    except Exception as e:
        print(f"> Unrecognized #, {e}")
        print(ERROR_MSG_CONT)
        continue

    try:
        ans = input('Select reflectance column #: ')
        REFL_COL = int(ans)
        if REFL_COL not in range(len(df.columns)):
            raise ValueError(f"{ans} out of column range")
        else:
            print(f"> Selected [{ans}] {df.columns[REFL_COL]} for reflectance column")
    except Exception as e:
        print(f"> Unrecognized #, {e}")

    try:
        wavelengths = np.array(df[df.columns[WL_COL]])
    except:
        print(f"Error assigning wavelength column.")
        exit()
    wl_nans = np.isnan(wavelengths).sum()
    if wl_nans > 0:
        print(f"wl shape: {wavelengths.shape}")
        print(f"wavelength nans: {np.isnan(wavelengths).sum()}")
        print(f"wavelength nan indices: {np.where(np.isnan(wavelengths))[0]}")

    try:
        reflectance = np.array(df[df.columns[REFL_COL]])
    except:
        print(f"Error assigning reflectance column.")
        exit()
    reflectance_nans = np.isnan(reflectance).sum()
    if reflectance_nans > 0:
        print(f"reflectance shape: {reflectance.shape}")
        print(f"reflectance nans: {np.isnan(reflectance).sum()}")
        print(f"reflectance nan indices: {np.where(np.isnan(reflectance))[0]}")

    ### concatenate and save
    output_dict = targeted_to_global(wavelengths, reflectance, verbose = False)
    df_global = pd.DataFrame(output_dict)
    df_global = df_global.rename(columns={"wavelengths": "Wavelength (µm) global", "values": f"{df.columns[1]} global"})
    df_global = pd.concat((df, df_global), axis = 1)

    if (output_folder/file_path.name).exists():
        print(f"[{file_counter+1}/{len(file_paths_list)}] File '{file_path.name}' already exists in output folder, overwrite (Y/N)?")
        ans = input()
        while ans.lower() not in ["y", "n"]:
            ans = input()
        if ans.lower() == "y":
            df_global.to_csv(path_or_buf = output_folder/file_path.name, index = False, na_rep = "")
    else:
        df_global.to_csv(path_or_buf = output_folder/file_path.name, index = False, na_rep = "")
        print(f"[{file_counter+1}/{len(file_paths_list)}] Saved '{file_path.name}' to folder '{output_folder.name}'")
print("Process completed.")