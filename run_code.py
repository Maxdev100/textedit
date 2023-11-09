# IN-TEXTEDITOR CODE RUNNING FUNCTIONS
import os

supported_extensions = ["py", "pyw", "bat", "vbs"]

# Run application. pause - don't close console when fihish
def run(file, pause=False):
    os.system("chcp 1251 >nul")
    if file is not None:
        if get_extension(file) in supported_extensions:
            print(file)
            os.system(f"start {file}")
            

def get_extension(file: str):
    extension = file.split(".")[1]
    return extension
