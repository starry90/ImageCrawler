#! /usr/bin/env python3
# coding=utf-8

import os

root_path = os.getcwd()
target_file = "code.txt"


def for_list_dir(dirs, dir_name=''):
    print("%s ==> %s" % (dir_name, str(dirs)))
    for dir in dirs:
        path = os.path.join(dir_name, dir)
        if not os.path.isfile(path):
            for_list_dir(os.listdir(path), path)
        elif dir != target_file and dir != "copy_code.py":
            with open(target_file, "a+") as f:
                f.writelines("\n================================================================\n")
                f.writelines("==> %s \n" % dir)
                with open(path, "r") as source:
                    for line in source:
                        f.writelines(line)


def main():
    dirs = os.listdir(root_path)
    for_list_dir(dirs, root_path)


if __name__ == '__main__':
    main()
