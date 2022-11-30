import sys, os
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
            #if directory contains slot indicator rename it
            if (dir.find("c0") > -1):
                if (oldslot == ""):
                    oldslot = dir[dir.find("c0"): dir.find("c0") +3]
                os.rename((root + "//" + dir), (root + "//" + new_slot))
                
            if (dir == "fighter"):
                fighter = os.listdir(root + "//" + dir)

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
    
def main():
    root = tk.Tk()
    folder_path = filedialog.askdirectory(initialdir="./", title="Open the root directory for your mod")
    if (os.path.isdir(folder_path) == False):
        assert("Could not find path" + folder_path)

    slot = input("What costume slot do you want to move the effect to? ")

    found_universal_effect, fighter= switchSlot(folder_path, slot)

    if (found_universal_effect):
        modify = input("We detected an effects folder that has not been attatched to a single slot, would you like to do so? Y/N (MUST have blujay one slot effect plugin? ")
        if (modify == "Y" or modify == "y"):
            eff_slotter.do_it(folder_path, fighter[0], slot)
            print("Changing effect to one slot completed")

again = True
while again:
    main()
    again = False
    string = input("Press Y to move another slot or press any other key to exit ")
    if (string == "Y" or string == "y"):
        again = True


