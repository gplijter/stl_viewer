import sys

sys.path.append("..")
import os
import subprocess
from shutil import rmtree


def build_exe():
    print("> running pyinstaller")
    # try:
    #     rmtree(".\\dist")
    #     rmtree(".\\build")
    # except Exception as e:
    #     print(e)

    subprocess.call([".\\..\\.venv\\Scripts\\pyinstaller.exe", ".\\..\\build_stl_viewer.spec"])
    print("> Done!")


if __name__ == "__main__":
    os.chdir(".\\builds\\")
    build_exe()

