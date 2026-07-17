import subprocess
import sys


def run():
    subprocess.call([sys.executable, "-m", "jupyter", "notebook"])
