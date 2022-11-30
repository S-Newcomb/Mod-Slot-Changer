import sys, os

def find_all_files(output: list[str], root: str):
    for root, dirs, files in os.walk(root):
        for dir in dirs:
            find_all_files(output, dir)
        for file in files:
            output.append(os.path.join(root, file))

def do_it(mod_path: str, fighter_name: str, slot: str):
    if not os.path.isdir(mod_path):
        print("Path '" + mod_path + "' is not a directory")
        exit()

    effect_folder = os.path.join(mod_path, "effect", "fighter", fighter_name)

    if not os.path.isdir(effect_folder):
        print("Path '" + effect_folder + "' is not a directory, does this mod contain an effect folder?")
        exit()

    added_files: list[str] = list()
    eff_file_name = "ef_" + fighter_name + ".eff"
    if os.path.isfile(os.path.join(effect_folder, eff_file_name)):
        new_eff_file_name = "ef_" + fighter_name + "_c" + str(slot).zfill(2) + ".eff"
        os.rename(os.path.join(effect_folder, eff_file_name), os.path.join(effect_folder, new_eff_file_name))
        added_files.append(os.path.join(effect_folder, new_eff_file_name))

    if os.path.isdir(os.path.join(effect_folder, "trail")):
        new_trail_name = "trail_c" + str(slot).zfill(2)
        os.rename(os.path.join(effect_folder, "trail"), os.path.join(effect_folder, new_trail_name))
        find_all_files(added_files, os.path.join(effect_folder, new_trail_name))

    if os.path.isdir(os.path.join(effect_folder, "model")):
        for root, dirs, files in os.walk(os.path.join(effect_folder, "model")):
            for dir in dirs:
                new_model_name = dir + "_c" + str(slot).zfill(2)
                os.rename(os.path.join(root, dir), os.path.join(root, new_model_name))
                find_all_files(added_files, os.path.join(root, new_model_name))
                
    file = open(os.path.join(mod_path, "config.json"), "w")
# Change this to preserve other config
    file.write("{\n    \"new-dir-files\": {\n")
    file.write("        \"fighter/" + fighter_name + "/c" + str(slot).zfill(2) + "\": [\n")
    for filepath in added_files:
        file.write("            \"" + filepath.removeprefix(mod_path + os.path.sep).replace(os.path.sep, "/") + "\"")
        if filepath == added_files[len(added_files) - 1]:
            file.write("\n")
        else:
            file.write(",\n")

    file.write("        ]\n    }\n}")

    file.close()

if __name__ == '__main__':
    USAGE = "Usage: ./eff_slotter.py path/to/mod/root <fighter_name> <slot_number>"

    if len(sys.argv) != 4:
        print(USAGE)
        exit()

    mod_path = sys.argv[1]
    fighter_name = sys.argv[2]
    slot = sys.argv[3]
    do_it(mod_path, fighter_name, slot)