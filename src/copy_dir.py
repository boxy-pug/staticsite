import os
import shutil

def copy_directory(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)

    os.makedirs(destination)

    for item in os.listdir(source):
        s = os.path.join(source, item)
        d = os.path.join(destination, item)
        if os.path.isdir(s):
            copy_directory(s, d)
        else:
            shutil.copy2(s, d)
            print(f"Copied {s} to {d}")

