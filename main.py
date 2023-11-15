from main_window import MainWindow
import sys
from github_autoupdate_lib.ppupdater.updater import *


filever = open("version.txt")

current_version = float(filever.read())
filever.close()

# Checking updates
updater = Updater(current_version=current_version, repository="https://github.com/Maxdev100/textedit",
                  target_path="./", tag="textedit")
update_avail = updater.check_update()


argv = sys.argv
if len(argv) < 2:
    argv.append(None)

window = MainWindow("Новый файл", 750, 550, True, file=argv[1], new_ver_av=update_avail, current_version=current_version)
