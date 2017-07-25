#!/usr/bin/env python
# coding=utf-8

import json
import os
import platform
import time
import traceback
import urllib
import urllib2
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


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
        (file_temp.writelines(content + "\n\n"))


def download_image(image_url='', file_local='', error_dir=''):
    for i in range(10):
        try:
            urllib.urlretrieve(image_url, file_local, reporthook=schedule)
            break
        except Exception as why:
            print 'Connection failure, retrying......%d' % i
            if i >= 9:
                write_file(error_dir + 'error.log', 'a+', traceback.format_exc())
            else:
                time.sleep(SLEEP_TIME)


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


HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
           'X-Request': 'JSON', 'X-Requested-With': 'XMLHttpRequest'}
CURRENT_DIR = sys.path[0]
SLEEP_TIME = 1


class HuaBan:
    def __init__(self):
        self.pageIndex = 1
        self.search_key = ''
        self.image_name = ''
        self.root_dir = ''
        self.dir_path = ''
        self.get_dir()

    def get_dir(self):
        system_str = platform.system()
        if system_str == 'Windows':
            self.root_dir = 'D:\\%s\\'
        else:
            self.root_dir = os.path.expanduser(r'~') + '/%s/'

        self.root_dir = self.root_dir % 'HuaBan'
        self.dir_path = self.root_dir + '%s' + os.sep

        if not os.path.exists(self.root_dir):
            os.makedirs(self.root_dir)

        print "Platform system: %s" % system_str
        print "Current directory: %s" % CURRENT_DIR
        print "Download directory: %s\n" % self.root_dir

    def read_file(self):
        with open(os.path.join(CURRENT_DIR, 'search.txt'), 'r') as file_lines:
            for line in file_lines:
                self.get_search_key(line.strip())

    def get_search_key(self, search_key=''):
        """
        set author index url

        """
        print 'Search key: %s' % search_key
        self.search_key = search_key
        url_format = "https://huaban.com/search/?q=%s&j5jqve8y&page=%d&per_page=20&wfl=1"
        for index in range(1, 10):
            print 'current page index: ', index
            url_search = url_format % (search_key, index)
            json_result = self.get_html(url_search)
            self.parse_json(json_result, index)

    def get_html(self, url_target=''):
        """
        get html content

        :param url_target: url
        """
        html_info = ''
        for i in range(10):
            try:
                # print url_target
                target_request = urllib2.Request(url_target, headers=HEADERS)
                target_response = urllib2.urlopen(target_request, timeout=10)
                html_info = target_response.read()
                time.sleep(SLEEP_TIME)
                print html_info
                break
            except Exception as why:
                print 'Connection failure, retrying......%d' % i
                if i >= 9:
                    write_file(self.root_dir + 'error.log', 'a+', traceback.format_exc())
                else:
                    time.sleep(SLEEP_TIME)

        return html_info

    def parse_json(self, json_result, page_index):
        json_model = json.loads(json_result)
        image_format = 'http://img.hb.aicdn.com/%s'
        items = json_model['pins']
        for index, value in enumerate(items):
            image_key = value['file']['key']
            image_url = image_format % str(image_key)
            self.image_name = image_key
            print "The %d work: %s" % (index + 1 + (page_index - 1) * 20, image_url)
            self.download_pre(image_url)

    def download_pre(self, image_url):
        # create local file directory
        print self.search_key.encode('gbk')
        dir_path = self.dir_path % self.search_key
        print dir_path
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

        # file download
        image_file = dir_path + self.image_name + '.jpeg'
        if not os.path.exists(image_file):
            print 'Downloading: ',
            # write_file(dir_path + 'image.txt', 'a+', image_url)
            download_image(image_url, image_file, self.root_dir)
            time.sleep(SLEEP_TIME)
        else:
            print 'File exist, skip download\n'


def main():
    hb = HuaBan()
    try:
        hb.read_file()
    except:
        print 'Downloading failure'
        ex_info = traceback.format_exc()
        print ex_info
        write_file(hb.root_dir + 'error.log', 'a+', str(ex_info))

    finally:
        raw_input('press [Enter]')


if __name__ == '__main__':
    main()
