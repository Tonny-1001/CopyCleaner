import os
import hashlib
import shutil
import ctypes, sys

os.system("")
deleted = 0


class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


if is_admin():

    def run2():
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
                return 1


    def run(dir):

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

        if len(to_remove) == 0:
            run2()
            return

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
                return 1

        run2()


    while True:
        try:
            dir = input("\npath> ")
            if run(dir) is None:
                print("\n" + style.RED + "No duplicate files found!" + style.RESET)
                continue
            run(dir)
        except FileNotFoundError:
             print("\n" + style.RED + "The specified directory does not exist!" + style.RESET)
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)