import os
import hashlib
import shutil
import ctypes, sys
from styling import style, clear_console

deleted = 0


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


if is_admin():

    def find_empty_directories(dir):
        dirtmp = []
        to_remove = []
        files_msg = ""

        def get_size(start_path):
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(start_path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if not os.path.islink(fp):
                        total_size += os.path.getsize(fp)
            return total_size

        for filename in os.listdir(dir):
            dirtmp.append(os.path.join(dir, filename))

        if len(dirtmp) > 0:
            for path_ in dirtmp:
                if os.path.isdir(path_):
                    size = get_size(path_)
                    if size == 0:
                        files_msg += "\n" + style.UNDERLINE + f"{path_}" + style.RESET + f"{style.YELLOW} - [Empty directory]{style.RESET}"
                        to_remove.append(path_)

        if len(to_remove) != 0:
            print(files_msg)
            cmd = input(f"\nDelete displayed data? type: [{style.GREEN}y{style.RESET}/{style.RED}n{style.RESET}] ")
            if cmd.lower() == "y":
                for file in to_remove:
                    try:
                        os.remove(file)
                    except PermissionError:
                        shutil.rmtree(file)
                print(f"\n{style.GREEN}Deleting\cleaning is finished!{style.RESET}")
                return 1
            else:
                print("\n" + style.RED + "Canceled." + style.RESET)
                return -1


    def find_duplicates(dir):

        dirtmp = []
        hashes = []
        to_remove = []
        files_msg = ""

        while True:
            if len(dirtmp) > 0:
                for path in dirtmp:
                    try:
                        for filename in os.listdir(path):
                            try:
                                if len(os.listdir(path)) == 0:
                                    files_msg += "\n" + style.UNDERLINE + f"{filename}" + style.RESET + f"{style.YELLOW} - [Empty directory]{style.RESET}"
                                    to_remove.append(os.path.join(path, filename))
                                else:
                                    dirtmp.append(os.path.join(path, filename))
                            except NotADirectoryError:
                                file = open(path, "rb")
                                content = file.read()
                                hash_object = hashlib.md5(content)
                                redy_hash = hash_object.hexdigest()
                                if redy_hash not in hashes:
                                    hashes.append(redy_hash)
                                else:
                                    files_msg += "\n" + style.UNDERLINE + f"{filename}" + style.RESET + f"{style.YELLOW} - [File]{style.RESET}"
                                    to_remove.append(os.path.join(path, filename))
                    except NotADirectoryError:
                        file = open(path, "rb")
                        content = file.read()
                        hash_object = hashlib.md5(content)
                        redy_hash = hash_object.hexdigest()
                        if redy_hash not in hashes:
                            hashes.append(redy_hash)
                        else:
                            files_msg += "\n" + style.UNDERLINE + f"{path}" + style.RESET + f"{style.YELLOW} - [File]{style.RESET}"
                            to_remove.append(path)
                break
            else:
                for filename in os.listdir(dir):
                    try:
                        if len(os.listdir(dir)) == 0:
                            files_msg += "\n" + style.UNDERLINE + f"{filename}" + style.RESET + f"{style.YELLOW} - [Empty directory]{style.RESET}"
                            to_remove.append(os.path.join(dir, filename))
                        else:
                            dirtmp.append(os.path.join(dir, filename))
                    except NotADirectoryError:
                        file = open(dir, "rb")
                        content = file.read()
                        hash_object = hashlib.md5(content)
                        redy_hash = hash_object.hexdigest()
                        if redy_hash not in hashes:
                            hashes.append(redy_hash)
                        else:
                            files_msg += "\n" + style.UNDERLINE + f"{filename}" + style.RESET + f"{style.YELLOW} - [File]{style.RESET}"
                            to_remove.append(os.path.join(dir, filename))

        if len(to_remove) != 0:
            print(files_msg)
            cmd = input(f"\nDelete displayed data? type: [{style.GREEN}y{style.RESET}/{style.RED}n{style.RESET}] ")
            if cmd.lower() == "y":
                for file in to_remove:
                    try:
                        os.remove(file)
                    except PermissionError:
                        shutil.rmtree(file)
                clear_console()
                print(f"\n{style.GREEN}Deleting\cleaning is finished!{style.RESET}")
                return 1

            else:
                clear_console()
                print("\n" + style.RED + "Canceled." + style.RESET)
                return 1

    print("""
    
░█████╗░░█████╗░██████╗░██╗░░░██╗  ░█████╗░██╗░░░░░███████╗░█████╗░███╗░░██╗███████╗██████╗░
██╔══██╗██╔══██╗██╔══██╗╚██╗░██╔╝  ██╔══██╗██║░░░░░██╔════╝██╔══██╗████╗░██║██╔════╝██╔══██╗
██║░░╚═╝██║░░██║██████╔╝░╚████╔╝░  ██║░░╚═╝██║░░░░░█████╗░░███████║██╔██╗██║█████╗░░██████╔╝
██║░░██╗██║░░██║██╔═══╝░░░╚██╔╝░░  ██║░░██╗██║░░░░░██╔══╝░░██╔══██║██║╚████║██╔══╝░░██╔══██╗
╚█████╔╝╚█████╔╝██║░░░░░░░░██║░░░  ╚█████╔╝███████╗███████╗██║░░██║██║░╚███║███████╗██║░░██║
░╚════╝░░╚════╝░╚═╝░░░░░░░░╚═╝░░░  ░╚════╝░╚══════╝╚══════╝╚═╝░░╚═╝╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝
""")
    while True:
        try:
            dir = input("\npath> ")
            if dir != "":
                clear_console()
                print(style.MAGENTA + "\nScanning provided directory for duplicate files..." + style.RESET)
                duplicates = find_duplicates(dir)
                if duplicates is None:
                    print("\n" + style.RED + "No duplicate files found!" + style.RESET)

                print(style.MAGENTA + "\nScanning provided directory for empty directories..." + style.RESET)
                empty = find_empty_directories(dir)
                if empty is None:
                    print("\n" + style.RED + "No empty directories found!" + style.RESET)
            else:
                clear_console()

        except FileNotFoundError:
            clear_console()
            print("\n" + style.RED + "The specified directory does not exist!" + style.RESET)
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)