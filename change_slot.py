import sys, os, shutil
import tkinter as tk
import eff_slotter
from tkinter import filedialog

def switchSlot(mod_folder, slot):
    oldslot = ""
    new_slot = "c0" + slot
    found_universal_effect = False
    fighter = ""    

    for root, dirs, files in os.walk(mod_folder):
        for dir in dirs:
            #Check if this is the fighter name folder and assign it
            subDirs = os.listdir(root + "//" + dir)
            if (root.find("fighter") and subDirs.count("model") > 0):
                fighter = dir

            #if directory contains slot indicator rename it
            if (dir.find("c0") > -1):
                if (oldslot == "" or oldslot == new_slot):
                    oldslot = dir[dir.find("c0"): dir.find("c0") +3]
                os.rename((root + "//" + dir), (root + "//" + new_slot))

        for file in files:
            idx = file.find("c0")
            uiIdx = file.find(".bntx")
            
            #if filename contains slot indicator rename it (sound, eff)
            if (idx > -1):
                newName = file[0:idx] + new_slot + file[idx + 3:]
                newPath = root + "//" + newName
                os.rename((root + "//" + file), newPath)

            #flag non oneslotted effects
            elif(file.find(".eff") > -1):
                found_universal_effect = True

            #if this is a ui file rename it to new slot
            elif (uiIdx > -1):
                newName = file[0:uiIdx-2] + "0" + slot + ".bntx"
                newPath = root + "//" + newName
                os.rename((root + "//" + file), newPath)

            #configure config.json if it exists
            elif (file == "config.json"):
                with open(root + "//" + file, 'r+') as r:
                    content = r.read()
                    r.seek(0)
                    oldslot = content[content.find("c0"):content.find("c0")+3]
                    newContent = content.replace(oldslot, new_slot)
                    r.write(newContent)

    print("Successfully moved " + mod_folder + " from slot " + oldslot + " to " + new_slot)
    return found_universal_effect, fighter

#deletes all folders not of the designated slot
def pruneSlots(modFolder, slot):
    slotToKeep = "c0" + slot
    for root, dirs, files in os.walk(modFolder):
            for dir in dirs:
                #delete dirs for a different char slot
                if (dir.find("c0") > -1 and dir.find(slotToKeep) == -1):
                    shutil.rmtree(root + "//" + dir)

            for file in files:
                keep = file.find(slotToKeep) > -1
                idx = file.find("c0")
                uiIdx = file.find(".bntx")

                #delete files for a different char slot
                if (idx > -1 and not keep):
                    os.remove(root + "//" + file)

                #delete UI files for diffeent char slots
                elif (uiIdx > -1 and file[uiIdx-1].isnumeric()):
                    uiSlot = int(file[uiIdx-1])
                    if (uiSlot != int(slot)): 
                        os.remove(root + "//" + file)


def main():
    prune = False
    commandArgs = sys.argv[1:]
    if commandArgs.count("-p") > 0:
        prune = True

    root = tk.Tk()
    folder_path = filedialog.askdirectory(initialdir="./", title="Open the root directory for your mod")
    if (os.path.isdir(folder_path) == False):
        assert("Could not find path" + folder_path)
    if prune:
        slotToKeep = input("You selected to prune char slots for this file \nWhich slot would you like to keep? ")
        pruneSlots(folder_path, slotToKeep)
        print("Pruning completed (This does not affect config.json files)")

    else:
        slot = input("What costume slot do you want to move the effect to? ")
        found_universal_effect, fighter= switchSlot(folder_path, slot)

        if (found_universal_effect):
            modify = input("We detected an effects folder that has not been attatched to a single slot, would you like to do so? Y/N (MUST have blujay one slot effect plugin) ")
            if (modify == "Y" or modify == "y"):
                eff_slotter.do_it(folder_path, fighter, slot)
                print("Changing effect to one slot completed")

again = True
while again:
    try:
        main()
    except Exception as error:
        print(Exception, error)
        sys.exit(1)

    again = False
    string = input("Press Y to move another slot or press any other key to exit ")
    if (string == "Y" or string == "y"):
        again = True


