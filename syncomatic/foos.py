import os
import datetime

from syncomatic import app, lm
from syncomatic.models import User

def get_filelist(path):
    """
        Returns a list of dictionaries;
        Each dictionary contains the following keys:
        'name', 'size', 'creation_date', 'is_dir'
    """
    filenames = os.listdir(path)
    files = []
    for name in filenames:
        # os.stat returns a 10-tuple
        stats = os.stat(os.path.join(path, name))
        size = stats[6]
        creation_date = datetime.datetime.fromtimestamp(stats[-2]).strftime("%H:%M %d.%m.%Y")
        is_dir = os.path.isdir(path)
        f = {'name': name, 'size': size, 'creation_date': creation_date,
            'is_dir': is_dir}
        files.append(f)

    return files
