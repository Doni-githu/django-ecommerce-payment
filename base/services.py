import os
def delete_old_file(path):
    if os.path.exists(path):
        os.remove(path)