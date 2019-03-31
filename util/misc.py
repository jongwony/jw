import os


def relative_path(path):
    project_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # TODO: wrong path
    print(project_dir, path, path[:len(project_dir)])
    if path[:len(project_dir)] == project_dir:
        return path[len(project_dir) + 1:]
    return path
