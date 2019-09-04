# -*- coding: utf-8 -*-
"""
@author: Zeng LH
@contact: 893843891@qq.com
@software: pycharm
@file: aria2_update_trackers_best.py
@time: 2019/9/4 0004 14:19
@desc: 为当前路径下的aria2配置文件更新trackers
"""
import os
import sys
import time
import getopt
import requests


def usage():
    print("-h help\n-p or --path custom path\n-f or --file_name config file name\n-t or --tracker_url tracker url")


def download_tracker(
        trackers_best_url="https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_best.txt"):
    try:
        trackers_best = "bt-tracker=" + requests.get(trackers_best_url).text.replace("\n\n", ",")[:-1]
        return trackers_best
    except Exception as e:
        print("网络错误! ", e)
        sys.exit(0)


def read_local_file(config_file_name="aria2.conf", trackers_url=None):
    if not os.path.exists(config_file_name):
        return False
    try:
        with open(config_file_name, "r", encoding="UTF-8") as f:
            data = list([])
            for line in f.readlines():
                if "bt-tracker=" not in line:
                    data.append(line)

        try:
            with open(config_file_name, "w", encoding="UTF-8") as f:
                for each in data:
                    f.write(each)
                if trackers_url:
                    f.write(download_tracker(trackers_url))
                else:
                    f.write(download_tracker())
        except Exception as e:
            print("读取都没问题, 写入居然出了问题, 请重新试试. 错误信息: ", e)
            return False

        print("success!")
        time.sleep(2)
    except Exception as e:
        print("似乎读取文件出了问题? 看看是否有其他程序正在占用这个文件. 错误信息: ", e)
        return False


def main(argv):
    config_file_name = None
    trackers_url = None
    path = None
    try:
        opts, args = getopt.getopt(argv, "hf:t:p:", ["file_name=", "tracker_url=", "path="])
    except getopt.GetoptError:
        print("不知道出了什么问题")
        sys.exit(2)

    for opt, arg in opts:
        if opt in "-h":
            usage()
            sys.exit(0)
        if opt in ("-f", "--file_name"):
            config_file_name = arg
        if opt in ("-t", "--tracker_url"):
            trackers_url = arg
        if opt in ("-p", "--path"):
            path = arg

    try:
        if path:
            print("输入了自定义路径: ", path)
            if path[:-1] != "/" or path[:-1] != "\\":
                config_file_name = path + "/" + config_file_name
            else:
                config_file_name = path + config_file_name
        if config_file_name and trackers_url:
            read_local_file(config_file_name, trackers_url)
        elif config_file_name:
            read_local_file(config_file_name)
        elif trackers_url:
            read_local_file(trackers_url=trackers_url)
        else:
            read_local_file()
    except SystemExit:
        print("网络都没有, 怎么运行?")
        time.sleep(2)


if __name__ == '__main__':
    main(sys.argv[1:])
