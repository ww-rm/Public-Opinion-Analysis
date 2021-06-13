import os


def scan_file(file_dir):
    files = []
    for roo, dirs, file in os.walk(file_dir):
        files.append(file)
    return files[0]
