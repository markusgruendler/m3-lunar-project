# M3: Lab to Targeted Conversion

import pandas as pd
from pathlib import Path
from collections import defaultdict

def findFolder(input_path, SEARCH_MSG):
    current_path = Path(input_path)
    if not current_path.exists(): return("Invalid Path")
    
    print(f"\nCurrent path: {current_path}")
    print(SEARCH_MSG)
    
    # list out folders with [#] as identifier
    folder_list = [f for f in current_path.iterdir() if f.is_dir()]
    print("> Folders in current folder:")
    if len(folder_list) == 0: print("[#] No folders found.")
    for c, i in enumerate(folder_list):
        print(f"[{c}] {i.name}")
    print("")

    choice = input().lower()
    while choice not in ["e", "s", "u"] + [str(i) for i in range(len(folder_list))]:
        choice = input("Couldn't read input, trying again. Target #: ").lower()

    if choice.lower() == "e": return("Exiting.")
    if choice.lower() == "s": return(current_path)
    if choice.lower() == "u": return(findFolder(current_path.parent, SEARCH_MSG))
    if choice.isnumeric() and int(choice) in range(len(folder_list)):
        current_path = current_path / folder_list[int(choice)]
        if current_path.is_dir():
            return(findFolder(current_path, SEARCH_MSG))

    return("Error reading choice, exiting.")

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

target_folder = findFolder(Path.cwd(), SEARCH_MSG_IN)
file_paths_list = [f for f in target_folder.iterdir() if f.is_file() and f.suffix == ".csv"] 
print(f"> {len(file_paths_list)} files found\n")

output_folder = findFolder(Path.cwd(), SEARCH_MSG_OUT)

# assumed step size between m3 points
STEPSIZE = 0.01

# initial boundaries for wavelengths, outside of which to ignore/truncate data
WL_MIN = 0.446
WL_MAX = 2.99

# define points around which to bin
m3_path = Path('../input files/Clark m3 target wavelengths.csv').resolve()
m3 = pd.read_csv(m3_path)
m3.columns = ['Wavelength (µm)']

x_m3 = (m3['Wavelength (µm)']).tolist()
x_m3 = [f"{wl:.5f}" for wl in x_m3]
print(f"> {len(x_m3)} m^3 wavelengths found")

# updated boundaries for wavelengths
WL_MIN = float(x_m3[0])-STEPSIZE/2
WL_MAX = float(x_m3[-1])+STEPSIZE/2
# print(f"# of m^3 wavelengths: {len(x_m3)}, first and last: {x_m3[0], x_m3[-1]}")

for file_counter, file_path in enumerate(file_paths_list):
    ### read, clean, establish raw lab data
    print(f"Loading '{file_path.name}' from folder '{target_folder.name}'")
    lab = pd.read_csv(file_path)

    FIRST_COLUMN = 'Wavelength (µm)'
    if FIRST_COLUMN not in list(lab.columns):
        lab[FIRST_COLUMN] = lab['Wavelength (nm)']/1000
        lab.drop('Wavelength (nm)', axis = 'columns', inplace=True)
    order = [FIRST_COLUMN] + [col for col in lab.columns if col != FIRST_COLUMN]
    lab = lab[order]
    lab.columns = lab.columns.str.replace(",","")
    lab.dropna(axis = 0, inplace=True)

    y_column_label = lab.columns[1]
    y_raw = list(lab[y_column_label])
    x_raw = list(lab[lab.columns[0]])
    x_raw = [float(f"{wl:.5f}") for wl in x_raw]


    ### bins stored as dictionaries of lists with numerical string keys
    binned_raw = defaultdict(list)
    for x in x_m3:
        binned_raw[x] = []
    len(binned_raw)

    # append points to bin with wavelength within half of stepsize
    # average points across bin
    # precondition: wavelengths are sorted in ascending order
    binCounter = 0
    for x,y in zip(x_raw, y_raw):
        if x < WL_MIN or x > WL_MAX: continue

        lbound = float(x_m3[binCounter]) - STEPSIZE/2
        rbound = float(x_m3[binCounter]) + STEPSIZE/2

        # while point doesn't fit into current bin, try next
        while x > rbound: 
            if binCounter + 1 < len(x_m3):
                binCounter += 1

                # update bin bounds
                lbound = float(x_m3[binCounter]) - STEPSIZE/2
                rbound = float(x_m3[binCounter]) + STEPSIZE/2
            else:
                print(f"Point {x, y} within WL MINMAX range {WL_MIN, WL_MAX} but no bin found, last bin: {lbound, rbound}")
                break
        binned_raw[x_m3[binCounter]].append((x,y))

    x_avg = []
    y_avg = []
    for count, bin in enumerate(binned_raw):
        if len(binned_raw[bin]) == 0: continue

        # avgx = 0
        avgy = 0
        for x,y in binned_raw[bin]:
            # avgx += x
            avgy += y
        # avgx /= len(binned_raw[bin])
        avgy /= len(binned_raw[bin])

        # band center as WL coordinate to match to target 10nm
        x_avg.append(float(bin))
        # x_avg.append(avgx)
        y_avg.append(avgy)


    ### df and save
    df_target = pd.DataFrame({"Wavelength (µm) target": x_avg, f"{lab.columns[1]} target": y_avg})
    df_target = pd.concat((lab, df_target), axis = 1)
    df_target.head()

    if (output_folder / file_path.name).exists():
        print(f"File '{file_path.name}' already exists in output folder, overwrite (Y/N)?")
        ans = input()
        while ans.lower() not in ["y", "n"]:
            ans = input()
        if ans.lower() == "y":
            df_target.to_csv(path_or_buf = output_folder/file_path.name, index = False, na_rep = "")
    else:
        df_target.to_csv(path_or_buf = output_folder/file_path.name, index = False, na_rep = "")
    
    print(f"[{file_counter+1}/{len(file_paths_list)}] Saved '{file_path.name}' to folder '{output_folder.name}'")
print("Process completed.")