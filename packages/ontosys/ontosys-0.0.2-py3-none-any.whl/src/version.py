import subprocess
import os

def get_git_describe():
    try:
        setup_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return subprocess.check_output(["git", "describe", "--tags"], cwd=setup_dir).decode("utf-8").strip()
    except:
        return None

__version__ = get_git_describe() or "0.1.0"
