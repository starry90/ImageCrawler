# /usr/bin/env python
# coding=utf-8
import urllib2
import urllib
import json
import re
import time
import os
import platform
import sys
import traceback


class ArtDetail:
    """
    author: starry lau
    """

    def __init__(self):
        """
        构造方法
        """
        self.pageIndex = 1
        self.authorName = ''
        self.root_dir = 'D:\ArtStation\\'
        self.wait_time = 1
        self.system_str = ''
        self.dir_path = ''
        self.current_dir = ''
        self.url_author = ''
        self.userAgent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'
        self.headers = {'User-Agent': self.userAgent}
        self.get_dir()

    def get_dir(self):
        self.current_dir = sys.path[0]
        system_str = platform.system()
        self.system_str = system_str
        if system_str == 'Linux':
            self.root_dir = os.environ['HOME'] + '/ArtStation/'
            self.dir_path = self.root_dir + 'image/'
        elif system_str == 'Windows':
            self.root_dir = 'D:\ArtStation\\'
            self.dir_path = self.root_dir + 'image\\'
        else:
            self.root_dir = os.path.expanduser(r'~/Desktop/') + 'ArtStation/'
            self.dir_path = self.root_dir + 'image/'

        if not os.path.exists(self.root_dir):
            os.makedirs(self.root_dir)

        print "当前系统：" + self.system_str
        print "当前目录：" + self.current_dir
        print "下载目录：" + self.root_dir

    def read_art(self):
        with open(os.path.join(self.current_dir, 'art.txt'), 'r') as art_file:
            for line in art_file:
                print line
                self.set_author(line.strip())

    def set_author(self, url_author=''):
        """
        设置作者url

        """
        if url_author == '' or r'www.artstation.com/artist' not in url_author:
            print '无效网址'
            return
        items = url_author.split("/")
        self.authorName = items[- 1]
        print "艺术家: %s" % self.authorName
        self.url_author = url_author.replace('/artist/', '/users/')
        self.get_author(self.url_author)

    def get_author(self, url_author=''):
        """
        获取作者作品

        :param url_author: author url
        """
        target_url = url_author + '/projects.json?page=' + str(self.pageIndex)
        json_info = self.get_html(target_url)
        if json_info:
            self.parse_json(json_info)

    def get_html(self, url_target=''):
        """
        获取网页内容

        :param url_target: 网页url
        """
        html_info = ''
        for i in range(10):
            try:
                # print url_target
                target_request = urllib2.Request(url_target, headers=self.headers)
                target_response = urllib2.urlopen(target_request)
                html_info = target_response.read()
                time.sleep(self.wait_time)
                # print html_info
                break
            except urllib2.URLError as why:
                print '重试中......%d' % i
                if i >= 9:
                    self.write_file(self.root_dir + 'error.log', 'a+', traceback.format_exc())
                else:
                    time.sleep(self.wait_time)

        return html_info

    def parse_json(self, json_info):
        """
        解析json

        :param json_info: json内容
        """
        target_model = json.loads(json_info)
        # print target_model
        # print target_model.keys()

        size = target_model["total_count"] / 50 + 1
        for i in range(1, size + 1):
            print '当前页码：%d/%d' % (i, size)
            for item in target_model["data"]:
                print item["permalink"]
                html_info = self.get_html(item["permalink"])
                if not html_info == '':
                    self.parse_html(html_info)

            self.get_author(self.url_author)

    def parse_html(self, html_info):
        """
        解析html

        :param html_info: 网页内容
        """
        reg_target = 'image_url.*?http(.*?)\\\\'
        pattern_target = re.compile(reg_target, re.S)
        items = re.findall(pattern_target, html_info)
        for item in items:
            image_url = 'http' + item
            print '图片地址：' + image_url
            self.download_image_pre(image_url)

    def download_image_pre(self, image_url=''):
        """
        下载图片

        :param image_url: 图片下载地址
        """
        image_url = image_url.replace('small', 'large')
        image_url = image_url.replace('medium', 'large')
        image_url = image_url.replace('small_square', 'large')
        image_url = image_url.replace('smaller_square', 'large')
        image_url = image_url.replace('micro_square', 'large')

        # 截取图片名称
        image_item = image_url.split("/")
        image_name = image_item[- 1]
        image_name_item = image_name.split("?")
        image_name = image_name_item[0]
        print '图片名称：' + image_name

        # 创建本地文件夹
        dir_path = self.dir_path.replace('image', self.authorName)
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

        # 文件下载
        file_local = dir_path + image_name
        if not os.path.exists(file_local):
            print '下载中:',
            self.write_file(dir_path + 'image.txt', 'a+', image_url)
            self.download_image(image_url, file_local)
            time.sleep(self.wait_time)
        else:
            print '文件已存在，跳过下载\n'

    def download_image(self, image_url='', file_local=''):
        for i in range(10):
            try:
                urllib.urlretrieve(image_url, file_local, reporthook=self.schedule)
                break
            except Exception as why:
                print '重试中......%d' % i
                if i >= 9:
                    self.write_file(self.root_dir + 'error.log', 'a+', traceback.format_exc())
                else:
                    time.sleep(self.wait_time)

    @staticmethod
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

    @staticmethod
    def write_file(file_name='', model='', content=''):
        with open(file_name, model) as file_temp:
            file_temp.writelines(content + "\n\n")


def main():
    art = ArtDetail()
    try:
        art.read_art()
    except:
        print '下载出错'
        ex_info = traceback.format_exc()
        print ex_info
        art.write_file(art.root_dir + 'error.log', 'a+', str(ex_info))

    finally:
        time.sleep(3)
        raw_input('press [Enter]')


if __name__ == '__main__':
    main()
