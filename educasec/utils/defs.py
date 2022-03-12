import os
from functools import partial
from uuid import uuid4


def update_filename(instance, filename, model_name, path_name):
    extension = os.path.splitext(filename)[1][1:]
    path = model_name
    if path_name:
        path = os.path.join(model_name, path_name)
    filename = '{}.{}'.format(uuid4().hex, extension)
    return os.path.join(path, filename)


''' upload_to:
    - Rename file to unique uuid4
'''
def upload_to(model, path=None):
    return partial(update_filename, model_name=model, path_name=path)
