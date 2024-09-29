import os
def import_files_and_dirs(directory):
    items = {}
    for root, dirs, files in os.walk(directory):
        rel_path = os.path.relpath(root, directory)
        if rel_path == '.':
            rel_path = ''
        for dir_name in dirs:
            if not dir_name.startswith('__'):
                full_path = os.path.join(root, dir_name)
                rel_name = os.path.join(rel_path, dir_name).replace(os.sep, '.')
                items[rel_name] = full_path
        for file_name in files:
            if not file_name.startswith('__'):
                full_path = os.path.join(root, file_name)
                file_name_without_ext = os.path.splitext(file_name)[0]
                rel_name = os.path.join(rel_path, file_name_without_ext).replace(os.sep, '.')
                items[rel_name] = full_path
    return items
current_dir = os.path.dirname(os.path.abspath(__file__))
imported_items = import_files_and_dirs(current_dir)
globals().update(imported_items)
__all__ = list(imported_items.keys())
