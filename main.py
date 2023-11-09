from main_window import MainWindow
import sys

argv = sys.argv
if len(argv) < 2:
    argv.append(None)

window = MainWindow("Новый файл", 750, 550, True, argv[1])
