#THIS IS ONYX PACKAGE MANAGER ITS PREINSTALLED WITH ONYX.PY FILE SO ITS DONT MEAN YOU HAVE TO DOWNLOAD IT YOU CAN MAKE YOUR OWN PACKAGE MANAGER FROM THIS SCRIPT
#!/usr/bin/env python3
import sys
import os
import difflib

MODULES_DIR = os.path.expanduser("~/.ox_modules")
INSTALLED_DIR = os.path.expanduser("~/.ox_installed")

if not os.path.exists(MODULES_DIR):
    os.makedirs(MODULES_DIR, exist_ok=True)
if not os.path.exists(INSTALLED_DIR):
    os.makedirs(INSTALLED_DIR, exist_ok=True)

def main():
    args = sys.argv[1:]
    if not args:
        print("opm: missing command. Use 'opm install <module_name>'")
        return
    
    cmd = args[0].lower()
    if cmd == "install":
        if len(args) < 2:
            print("opm error: please specify a module name to install.")
            return
        mod_name = args[1].lower()
        
        available_modules = [f.replace(".oxm", "") for f in os.listdir(MODULES_DIR)]
        installed_modules = [f.replace(".oxm", "") for f in os.listdir(INSTALLED_DIR)]
        
        target_file = os.path.join(MODULES_DIR, f"{mod_name}.oxm")
        installed_file = os.path.join(INSTALLED_DIR, f"{mod_name}.oxm")
        
        if os.path.exists(target_file):
            if mod_name in installed_modules:
                print(f"Module '{mod_name}' is already installed.")
            else:
                with open(target_file, 'r', encoding='utf-8') as src, open(installed_file, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
                print(f"Successfully installed module: {mod_name}")
        else:
            matches = difflib.get_close_matches(mod_name, available_modules, n=1, cutoff=0.6)
            if matches:
                nearest = matches[0]
                print(f"ERROR NO MODULE FOUND NAMED {mod_name}")
                choice = input(f"the nearest module to its name {nearest}\ndo you want to update your code to it y/n: ").strip().lower()
                if choice == 'y':
                    nearest_target = os.path.join(MODULES_DIR, f"{nearest}.oxm")
                    nearest_installed = os.path.join(INSTALLED_DIR, f"{nearest}.oxm")
                    if os.path.exists(nearest_target):
                        with open(nearest_target, 'r', encoding='utf-8') as src, open(nearest_installed, 'w', encoding='utf-8') as dst:
                            dst.write(src.read())
                    print(f"Successfully installed nearest module: {nearest}")
                else:
                    print("Installation cancelled.")
            else:
                print(f"ERROR NO MODULE FOUND NAMED {mod_name}")
    else:
        print(f"opm: unknown command '{cmd}'")

if __name__ == "__main__":
    main()
