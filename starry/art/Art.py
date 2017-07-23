# /usr/bin/env python
# coding=utf-8
import json
import os
import platform
import re
import sys
import time
import traceback
import urllib
import urllib2


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


class Art:
    """
    author: starry
    """

    def __init__(self):
        self.pageIndex = 1
        self.authorName = ''
        self.root_dir = 'D:\ArtStation\\'
        self.wait_time = 1
        self.dir_path = ''
        self.current_dir = sys.path[0]
        self.url_author = ''
        self.userAgent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'
        self.headers = {'User-Agent': self.userAgent}
        self.get_dir()

    def get_dir(self):
        system_str = platform.system()
        if system_str == 'Linux':
            self.root_dir = os.environ['HOME'] + '/ArtStation/'
        elif system_str == 'Windows':
            self.root_dir = 'D:\ArtStation\\'
        else:
            self.root_dir = os.path.expanduser(r'~/Desktop/') + 'ArtStation/'

        self.dir_path = self.root_dir + '%s' + os.sep

        if not os.path.exists(self.root_dir):
            os.makedirs(self.root_dir)

        print "Platform system: " + system_str
        print "Current directory: " + self.current_dir
        print "Download directory: " + self.root_dir

    def read_art(self):
        with open(os.path.join(self.current_dir, 'art.txt'), 'r') as art_file:
            for line in art_file:
                print line
                self.set_author(line.strip())

    def set_author(self, url_author=''):
        """
        set author index url

        """
        if not url_author or r'artstation' not in url_author:
            print 'Invalid url'
            return
        items = url_author.split("/")
        self.authorName = items[- 1]
        print "Artist: %s" % self.authorName
        self.url_author = url_author.replace(r'/artist/', r'/users/')
        self.get_author()

    def get_author(self):
        """
        get author work

        """
        target_url = self.url_author + '/projects.json?page=' + str(self.pageIndex)
        json_info = self.get_html(target_url)
        if json_info:
            self.parse_json(json_info)

    def get_html(self, url_target=''):
        """
        get html content

        :param url_target: url
        """
        html_info = ''
        for i in range(10):
            try:
                # print url_target
                target_request = urllib2.Request(url_target, headers=self.headers)
                target_response = urllib2.urlopen(target_request, timeout=10)
                html_info = target_response.read()
                time.sleep(self.wait_time)
                # print html_info
                break
            except Exception as why:
                print 'Connection failure, retrying......%d' % i
                if i >= 9:
                    write_file(self.root_dir + 'error.log', 'a+', traceback.format_exc())
                else:
                    time.sleep(self.wait_time)

        return html_info

    def parse_json(self, json_info):
        """
        parse json

        :param json_info: json content
        """
        target_model = json.loads(json_info)
        # print target_model
        # print target_model.keys()

        size = target_model["total_count"] / 50 + 1
        print 'Current page: %d/%d' % (self.pageIndex, size)
        data_list = target_model["data"]
        for index, value in enumerate(data_list):
            print "The %d work: %s" % (index + 1 + (self.pageIndex - 1) * 50, str(value["permalink"]))
            html_info = self.get_html(value["permalink"])
            if html_info:
                self.parse_html(html_info)

        self.pageIndex += 1
        if self.pageIndex != size:
            self.get_author()

    def parse_html(self, html_info):
        """
        parse html

        :param html_info: html info
        """
        reg_target = 'image_url.*?http(.*?)\\\\'
        pattern_target = re.compile(reg_target, re.S)
        items = re.findall(pattern_target, html_info)
        for item in items:
            image_url = 'http' + item
            print 'Image url: ' + image_url
            self.download_image_pre(image_url)

    def download_image_pre(self, image_url=''):
        """
        download image

        :param image_url: image url
        """
        image_url = image_url.replace('small', 'large')
        image_url = image_url.replace('medium', 'large')
        image_url = image_url.replace('small_square', 'large')
        image_url = image_url.replace('smaller_square', 'large')
        image_url = image_url.replace('micro_square', 'large')

        # split image name
        image_item = image_url.split("/")
        image_name = image_item[- 1]
        image_name_item = image_name.split("?")
        image_name = image_name_item[0]
        print 'Image name: ' + image_name

        # create local file directory
        dir_path = self.dir_path % self.authorName
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

        # file download
        file_local = dir_path + image_name
        if not os.path.exists(file_local):
            print 'Downloading: ',
            write_file(dir_path + 'image.txt', 'a+', image_url)
            self.download_image(image_url, file_local)
            time.sleep(self.wait_time)
        else:
            print 'File exist, skip download\n'

    def download_image(self, image_url='', file_local=''):
        for i in range(10):
            try:
                urllib.urlretrieve(image_url, file_local, reporthook=schedule)
                break
            except Exception as why:
                print 'Connection failure, retrying......%d' % i
                if i >= 9:
                    write_file(self.root_dir + 'error.log', 'a+', traceback.format_exc())
                else:
                    time.sleep(self.wait_time)


def main():
    art = Art()
    try:
        art.read_art()
    except:
        print 'Downloading failure'
        ex_info = traceback.format_exc()
        print ex_info
        write_file(art.root_dir + 'error.log', 'a+', str(ex_info))

    finally:
        raw_input('press [Enter]')


if __name__ == '__main__':
    main()
