#! /usr/bin/env python
# coding=utf-8
import json
import os
import platform
import re
import sys
import time
import traceback
import urllib2


def write_file(file_name='', model='', content='', newline=False):
    """
    Writes content to the specified file

    :param file_name:  file name
    :param model:  file write mode
    :param content:  the content of the write file
    """
    if not file_name or not content:
        return

    with open(file_name, model) as file_temp:
        file_temp.writelines(content + ('\n' if newline else ''))


HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'}
CURRENT_DIR = sys.path[0]
SLEEP_TIME = 1

ART_ARTIST = 'https://www.artstation.com/artist/'
ART = 'https://www.artstation.com/'
ART_USERS = 'https://www.artstation.com/users/'


class Art:
    """
    author: starry
    """

    def __init__(self):
        self.pageIndex = 1
        self.authorName = ''
        self.root_dir = ''
        self.dir_path = ''
        self.url_author = ''
        self.get_dir()

    def get_dir(self):
        system_str = platform.system()
        if system_str == 'Windows':
            self.root_dir = 'D:\\%s\\'
        else:
            self.root_dir = os.path.expanduser(r'~') + '/%s/'

        self.root_dir = self.root_dir % 'ArtStation'
        self.dir_path = self.root_dir + '%s' + os.sep

        if not os.path.exists(self.root_dir):
            os.makedirs(self.root_dir)

        print "Platform system: %s" % system_str
        print "Current directory: %s" % CURRENT_DIR
        print "Download directory: %s\n" % self.root_dir

    def read_art(self):
        art_file_name = os.path.join(CURRENT_DIR, 'art.txt')
        with open(art_file_name, 'r') as art_file:
            lines = []
            for line in art_file:
                lines.append(line)
            for index, line in enumerate(lines):
                if str(line).startswith('finished'):
                    continue
                self.set_author(line.strip())
                self.get_author()
                # download finished add 'finished' flag
                lines[index] = 'finished ' + line
                update_str = ''
                for value in lines:
                    update_str += value.strip() + ('\n' if value != lines[-1] else '')
                write_file(art_file_name, 'w', update_str)

    def set_author(self, url_author=''):
        """
        set author index url

        """
        print 'Artist home page: %s' % url_author
        items = url_author.split("/")
        self.authorName = items[- 1]
        print "Artist: %s\n" % self.authorName
        if ART_ARTIST in url_author:
            url_author = url_author.replace(ART_ARTIST, ART_USERS)
        elif ART in url_author:
            url_author = url_author.replace(ART, ART_USERS)
        self.url_author = url_author

    def get_author(self):
        """
        get author work

        """
        target_url = '%s/projects.json?page=%d' % (self.url_author, self.pageIndex)
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
                target_request = urllib2.Request(url_target, headers=HEADERS)
                target_response = urllib2.urlopen(target_request, timeout=10)
                html_info = target_response.read()
                time.sleep(SLEEP_TIME)
                # print html_info
                break
            except Exception as why:
                print 'Connection failure, retrying......%d' % i
                if i >= 9:
                    write_file(self.root_dir + 'error.log', 'a+', traceback.format_exc(), True)
                else:
                    time.sleep(SLEEP_TIME)

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
        reg_target = '"image_url.*?https(.*?)\\\\'
        pattern_target = re.compile(reg_target, re.S)
        items = re.findall(pattern_target, html_info)
        for item in items:
            image_url = 'https' + item
            self.download_image_pre(image_url)

    def download_image_pre(self, image_url=''):
        """
        download image

        :param image_url: image url
        """
        print 'Image url: %s' % image_url
        image_url = image_url.replace('/small/', '/large/')
        image_url = image_url.replace('/medium/', '/large/')
        image_url = image_url.replace('/small_square/', '/large/')
        image_url = image_url.replace('/smaller_square/', 'large')
        image_url = image_url.replace('/micro_square/', '/large/')

        # split image name
        image_item = image_url.split("/")
        image_name = image_item[- 1]
        image_name_item = image_name.split("?")
        image_name = image_name_item[0]
        # print 'Image name: %s' % image_name

        # create local file directory
        dir_path = self.dir_path % self.authorName
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

        # file download
        file_local = dir_path + image_name
        if not os.path.exists(file_local):
            print 'Downloading: ',
            write_file(dir_path + 'image.txt', 'a+', image_url, True)
            self.download_image(image_url, file_local)
            time.sleep(SLEEP_TIME)
        else:
            print 'File exist, skip download\n'
        print file_local

    def download_image(self, image_url='', file_path=''):
        for i in range(10):
            try:
                # print image_url
                target_request = urllib2.Request(image_url, headers=HEADERS)
                result = urllib2.urlopen(target_request, timeout=10)
                data = result.read()
                with open(file_path, "wb") as code:
                    code.write(data)
                    print 'success...'
                    break
            except Exception as why:
                print 'Connection failure, retrying......%d' % i
                if i >= 9:
                    write_file(self.root_dir + 'error.log', 'a+', traceback.format_exc(), True)
                else:
                    time.sleep(SLEEP_TIME)


def main():
    art = Art()
    try:
        art.read_art()
    except:
        print 'Downloading failure'
        ex_info = traceback.format_exc()
        print ex_info
        write_file(art.root_dir + 'error.log', 'a+', str(ex_info), True)

    finally:
        raw_input('press [Enter]')


if __name__ == '__main__':
    main()
