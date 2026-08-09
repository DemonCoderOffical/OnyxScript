#!/usr/bin/env python3
import sys
import os
import sqlite3
import subprocess
import difflib
import tkinter as tk
import arabic_reshaper
from bidi.algorithm import get_display

# =====================================================================
# 1. Ø¥Ø¹Ø¯Ø§Ø¯Ø§Øª Ù…Ø³Ø§Ø±Ø§Øª Ø§Ù„Ø¨ÙŠØ¦Ø© ÙˆÙ…Ø¯ÙŠØ± Ø§Ù„Ø­Ø²Ù… (OPM)
# =====================================================================
MODULES_DIR = os.path.expanduser("~/.ox_modules")
INSTALLED_DIR = os.path.expanduser("~/.ox_installed")

if not os.path.exists(MODULES_DIR):
    os.makedirs(MODULES_DIR, exist_ok=True)
if not os.path.exists(INSTALLED_DIR):
    os.makedirs(INSTALLED_DIR, exist_ok=True)

memory = {}
functions = {}
loaded_modules = set()

def fix_arabic(text):
    try:
        reshaped_text = arabic_reshaper.reshape(text)
        return get_display(reshaped_text)
    except:
        return text

# =====================================================================
# 2. Ù…Ø­Ø±Ùƒ Ù‚ÙˆØ§Ø¹Ø¯ Ø§Ù„Ø¨ÙŠØ§Ù†Ø§Øª Ø§Ù„Ù…Ø¯Ù…Ø¬ (.odb Core)
# =====================================================================
class OnyxDatabase:
    def __init__(self, db_path):
        if not db_path.endswith('.odb'):
            db_path += '.odb'
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def execute(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.fetchall()
        except Exception as e:
            return f"ODB Error: {str(e)}"

    def close(self):
        self.conn.close()

# =====================================================================
# 3. Ù…Ø¹Ø§Ù„Ø¬ Ø§Ù„ØªØ¹Ø¨ÙŠØ±Ø§Øª ÙˆØ§Ù„Ø°Ø§ÙƒØ±Ø©
# =====================================================================
def evaluate_expression(expr):
    expr = expr.strip()
    
    if expr.lower() == "true":
        return True
    if expr.lower() == "false":
        return False

    if (expr.startswith('"') and expr.endswith('"')) or (expr.startswith("'") and expr.endswith("'")):
        return expr[1:-1]
    
    if expr in memory:
        return memory[expr]
    
    if expr.upper() == "PUT()" or expr.startswith("PUT("):
        return input("Input > ")

    try:
        if "." in expr and all(c.isdigit() or c in ".-+*/" for c in expr):
            return float(expr)
        elif expr.isdigit():
            return int(expr)
        return eval(expr, {"__builtins__": None, "True": True, "False": False}, memory)
    except:
        return expr

# =====================================================================
# 4. Ù…Ø¹Ø§Ù„Ø¬ Ø§Ù„Ø£ÙˆØ§Ù…Ø± ÙˆØ³ÙŠØ§Ù‚ Ø§Ù„ØªÙ†ÙÙŠØ°
# =====================================================================
def execute_command_string(cmd_str, app_widgets=None):
    cmd_str = cmd_str.strip()
    if not cmd_str:
        return None

    if cmd_str.startswith("PRINT(") and cmd_str.endswith(")"):
        content = cmd_str[6:-1].strip()
        val = evaluate_expression(content)
        print(val)
        return val

    elif cmd_str.upper() == "VARS":
        print("--- Onyx Memory Dump ---")
        for k, v in memory.items():
            print(f"{k} = {v}")
        print("------------------------")
        return None

    elif cmd_str.startswith("var "):
        parts = cmd_str[4:].split("=")
        if len(parts) == 2:
            var_name = parts[0].strip()
            var_val = evaluate_expression(parts[1].strip())
            memory[var_name] = var_val

    elif cmd_str.startswith("SET "):
        parts = cmd_str[4:].split("=")
        if len(parts) == 2:
            var_name = parts[0].strip()
            var_val = evaluate_expression(parts[1].strip())
            memory[var_name] = var_val

    elif cmd_str.startswith("CHANGE_BTN_COLOR"):
        if "colors" not in loaded_modules:
            print("\033[91mOnyxRuntimeError: You must add 'ADD COLORS.' before using color commands.\033[0m")
            return
        try:
            color_val = cmd_str.split("TO")[1].replace("=", "").strip().strip('"').strip("'")
            if app_widgets and "last_btn" in app_widgets:
                app_widgets["last_btn"].config(bg=color_val)
                print(f"Button color changed to {color_val}")
        except Exception:
            print("OnyxError: Invalid CHANGE_BTN_COLOR syntax.")

    elif cmd_str.startswith("CHANGE_BG_COLOR"):
        if "colors" not in loaded_modules:
            print("\033[91mOnyxRuntimeError: You must add 'ADD COLORS.' before using color commands.\033[0m")
            return
        try:
            color_val = cmd_str.split("TO")[1].replace("=", "").strip().strip('"').strip("'")
            if app_widgets and "root" in app_widgets:
                app_widgets["root"].config(bg=color_val)
                print(f"Background color changed to {color_val}")
        except Exception:
            print("OnyxError: Invalid CHANGE_BG_COLOR syntax.")

    return None

# =====================================================================
# 5. Ø§Ù„Ù…ÙØ³Ø± Ø§Ù„Ø±Ø¦ÙŠØ³ÙŠ Ù„ØªØ´ØºÙŠÙ„ Ù…Ù„ÙØ§Øª .os / .ox
# =====================================================================
def run_onyx_file(file_path):
    if not os.path.exists(file_path):
        print(f"OnyxError: File '{file_path}' not found.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for idx, line in enumerate(lines):
        stripped = line.strip()
        if not stripped or stripped.startswith("//") or stripped.startswith("#"):
            continue
        
        if stripped.startswith("ONYX CONNECT TO") or stripped.startswith("WINDOW(") or stripped.startswith("FUNC ") or stripped.startswith("IF ") or stripped.startswith("ADD ") or stripped.startswith("GET ") or stripped.startswith("CREATE MODULE") or stripped.startswith("PUBLISH") or stripped.startswith("LOOP("):
            if stripped.startswith("ADD ") and not stripped.endswith("."):
                col_num = len(line) - len(line.lstrip()) + len(stripped)
                print(f"\033[91mOnyxSyntaxError: Missing dot (.) at line {idx + 1}:{col_num}\033[0m")
                return
            continue

        if not stripped.endswith("."):
            col_num = len(line) - len(line.lstrip()) + len(stripped)
            print(f"\033[91mOnyxSyntaxError: Missing dot (.) at line {idx + 1}:{col_num}\033[0m")
            return

    has_window = any(line.strip().startswith("WINDOW(") for line in lines)
    app_root = None
    app_widgets = {}

    if has_window:
        for line in lines:
            raw_line = line.strip()
            if raw_line.startswith("WINDOW("):
                title = raw_line.split("WINDOW(")[1].split(")")[0].strip('"').strip("'")
                app_root = tk.Tk(className='Onyx')
                app_root.title(fix_arabic(title))
                app_root.geometry("450x400")
                app_widgets["root"] = app_root
                break

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        i += 1

        if not stripped or stripped.startswith("//") or stripped.startswith("#") or stripped.startswith("WINDOW("):
            continue

        if stripped.startswith("GET "):
            try:
                clean_cmd = stripped[:-1].strip() if stripped.endswith(".") else stripped
                parts = clean_cmd.split(" ADD ")
                module_source = parts[0].replace("GET", "").strip()
                feature_name = parts[1].strip()
                print(f"Imported '{feature_name}' from '{module_source}' successfully.")
            except:
                print("OnyxError: Invalid GET syntax.")
            continue

        if stripped.startswith("ADD "):
            mod_cmd = stripped[:-1].strip() if stripped.endswith(".") else stripped
            mod_name = mod_cmd.replace("ADD", "").strip().lower()
            if mod_name == "colors":
                loaded_modules.add("colors")
                print("Module 'Colors' loaded successfully.")
            continue

        if stripped.endswith("."):
            stripped = stripped[:-1].strip()

        if has_window and app_root:
            if stripped.startswith("LABEL("):
                content = stripped.split("LABEL(")[1].split(")")[0].strip('"').strip("'")
                tk.Label(app_root, text=fix_arabic(content), font=("Sans", 13)).pack(pady=10)
                continue
            elif stripped.startswith("BUTTON("):
                btn_text = stripped.split("BUTTON(")[1].split(")")[0].strip('"').strip("'")
                btn = tk.Button(app_root, text=fix_arabic(btn_text), font=("Sans", 11))
                btn.pack(pady=10)
                app_widgets["last_btn"] = btn
                continue

        if " AFTER " in stripped or " BEFORE " in stripped or " THEN " in stripped:
            if " AFTER " in stripped:
                parts = stripped.split(" AFTER ")
                execute_command_string(parts[0].strip(), app_widgets)
                execute_command_string(parts[1].strip(), app_widgets)
            elif " BEFORE " in stripped:
                parts = stripped.split(" BEFORE ")
                execute_command_string(parts[1].strip(), app_widgets)
                execute_command_string(parts[0].strip(), app_widgets)
            elif " THEN " in stripped:
                parts = stripped.split(" THEN ")
                execute_command_string(parts[0].strip(), app_widgets)
                execute_command_string(parts[1].strip(), app_widgets)
            continue

        execute_command_string(stripped, app_widgets)

    if has_window and app_root:
        app_root.mainloop()

# =====================================================================
# 6. Ù…ÙˆØ¬Ù‡ Ø§Ù„Ø£ÙˆØ§Ù…Ø± ÙˆØ§Ù„Ù†Ø¸Ø§Ù… Ø§Ù„Ø´Ø§Ù…Ù„ (Main Entry)
# =====================================================================
def main():
    args = sys.argv[1:]
    if not args:
        print("OnyxScript All-in-One Engine Active.")
        print("Usage: python3 onyx.py <filename.os>  OR  python3 onyx.py install <module>")
        return
    
    if args[0].lower() == "install":
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
        run_onyx_file(args[0])

if __name__ == "__main__":
    main()