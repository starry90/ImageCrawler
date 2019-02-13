#!/usr/bin/env python3
# coding=utf-8

import os

ENV_NAME = ['ANDROID_HOME', 'ANDROID_NDK_HOME']
LOCAL_NAME = 'temp'
project_path = os.getcwd()
git_clone = 'git clone %s %s'
git_branch = 'git branch %s origin/%s'
git_checkout = 'git checkout %s' % LOCAL_NAME
git_pull = 'git pull origin %s'


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
    print(">> git.txt")
    with open('git.txt', 'r') as file_lines:
        for index, line in enumerate(file_lines):
            value = str(line).strip()
            git_map[str(index)] = value
            print("## %s" % value)

    print(">> git clone")
    print(">> git clone code %d" % os.system(git_clone % (git_map['0'], git_map['1'])))

    os.chdir(os.path.join(project_path, git_map['1']))

    print(">> git branch")
    print(">> git branch code %d" % os.system(git_branch % (LOCAL_NAME, git_map['2'])))

    print(">> git checkout")
    print(">> git checkout code %d" % os.system(git_checkout))

    print(">> git pull")
    print(">> git pull code %d" % os.system(git_pull))

    os.system('python build.py')

    print(">> python end\n")


if __name__ == '__main__':
    main()
