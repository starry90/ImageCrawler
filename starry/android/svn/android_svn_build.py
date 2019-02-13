#!/usr/bin/env python3
# coding=utf-8

import os

ENV_NAME = ['ANDROID_HOME', 'ANDROID_NDK_HOME']
LOCAL_NAME = 'temp'
project_path = os.getcwd()
svn_checkout = 'svn checkout %s %s'
svn_update = 'svn update'


def put_env():
    print(">> env.txt")
    with open('env.txt', 'r') as file_lines:
        for index, line in enumerate(file_lines):
            name = ENV_NAME[index]
            value = str(line).strip()
            print("## %s" % value)
            os.putenv(name, value)


def main():
    print(">> python start")

    put_env()

    git_map = {}
    print(">> svn.txt")
    with open('svn.txt', 'r') as file_lines:
        for index, line in enumerate(file_lines):
            value = str(line).strip()
            git_map[str(index)] = value
            print("## %s" % value)

    print(">> svn checkout")
    print(">> svn checkout code %d" % os.system(svn_checkout % (git_map['0'], git_map['1'])))

    os.chdir(os.path.join(project_path, git_map['1']))
    print(">> svn update")
    print(">> svn update code %d" % os.system(svn_update))

    os.chdir(project_path)
    os.chdir(os.path.join(project_path, git_map['2']))
    os.system('python build.py')

    print(">> python end\n")


if __name__ == '__main__':
    main()
