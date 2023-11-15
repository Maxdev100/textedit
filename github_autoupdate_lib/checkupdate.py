from ppupdater.updater import Updater

# updater = Updater(repository="https://github.com/Maxdev100/synergyfinalproject/", current_version=0.99,
#                   target_path="./test_update", archive_name="Final.Project.zip", printlog=False, ignore_folders=[r'classes/__pycache__/', "classes/"])
#
# if updater.check_update():
#     updater.update()

updater = Updater(repository="https://github.com/Maxdev100/textedit", tag="textedit", current_version=0.0, target_path="./test_update")

updater.update()