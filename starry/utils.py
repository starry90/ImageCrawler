# /usr/bin/env python
# coding=utf-8


def write_file(file_name='', model='', content=''):
    """
    Writes content to the specified file

    :param file_name:  file name
    :param model:  file write mode
    :param content:  the content of the write file
    """
    if not file_name or not content:
        return

    with open(file_name, model) as file_temp:
        file_temp.writelines(content + "\n\n")


def schedule(block_num, bs, size):
    """
    Download progress

    :param block_num: downloaded data block
    :param bs: size of data block
    :param size: file size
    """
    per = 100.0 * block_num * bs / size
    if per > 100:
        per = 100

    print '%0.f%%' % per,
    if per == 100:
        print '\n'


if __name__ == '__main__':
    print "main"
