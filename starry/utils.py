# /usr/bin/env python
# coding=utf-8


def write_file(file_name='', model='', content=''):
    """
    写把内容写入到指定文件方法

    :param file_name:  文件名称
    :param model:  文件读写模式
    :param content:  写入文件内容
    """
    if not file_name or not content:
        return

    with open(file_name, model) as file_temp:
        file_temp.writelines(content + "\n\n")


def schedule(block_num, bs, size):
    """
    下载进度

    :param block_num: 已经下载的数据块
    :param bs: 数据块的大小
    :param size: 远程文件的大小
    """
    per = 100.0 * block_num * bs / size
    if per > 100:
        per = 100

    print '%0.f%%' % per,
    if per == 100:
        print '\n'


if __name__ == '__main__':
    print "main"
