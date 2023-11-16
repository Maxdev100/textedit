from main_window import MainWindow
import sys
import threading

filever = open("version.txt")

current_version = float(filever.read())
filever.close()

argv = sys.argv
if len(argv) < 2:
    argv.append(None)


def start_app():
    window = MainWindow("Новый файл", 750, 550, True, file=argv[1],
                        current_version=current_version)


main_thread = threading.Thread(target=start_app)
main_thread.start()
main_thread.join()
