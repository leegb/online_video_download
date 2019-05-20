# -*-coding=utf-8-*-

# @Time : 2019/1/28 14:19
# @File : youtube_downloader.py

import subprocess
import sys

import pymongo
import re
import codecs


def extract_link(filename='web.html'):
    with codecs.open(filename, 'r', encoding='utf8') as f:
        content = f.read()

    try:
        result = re.findall('\{"videoId":"(\w+)"\}', content)
    except Exception as e:
        return []
    else:
        return result

# 从文件下载
def download_from_txt():
    db = pymongo.MongoClient('10.18.6.46', port=27001)
    doc = db['db_rocky']['youtube']

    CMD = 'python you-get {}'
    while 1:
        with open('youtube_link.txt', 'r') as f:
            lines = f.readlines()
            lines_copy = lines.copy()
            if not lines:
                break

            for line in lines_copy:
                print(line.strip())
                # line=line.strip()
                is_exists = doc.find({'url': line.strip()})

                if list(is_exists):
                    print('{} is exists !'.format(line))
                    lines_copy.remove(line)

                else:
                    try:
                        p = subprocess.Popen(CMD.format(line.strip()), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                             shell=True)

                        output, error = p.communicate()
                    except Exception as e:
                        print(e)
                        continue
                    else:
                        lines_copy.remove(line)
                        print('{} has been downloaded !'.format(line))
                        try:
                            doc.insert({'url': line.strip()})
                        except Exception as e:
                            print(e)

        with open('youtube_link.txt', 'w') as f:
            f.writelines(lines_copy)


def download_from_web():
    db = pymongo.MongoClient('10.18.6.46', port=27001)
    doc = db['db_rocky']['youtube']
    id_list = extract_link()
    base_url = 'https://www.youtube.com/watch?v={}'
    for idx in id_list:

        full_url = base_url.format(idx)
        cmd='python you-get {}'.format(full_url)
        is_exists = doc.find({'url': full_url})

        # if list(is_exists):
        #     print('已经下载过>>>>{}'.format(full_url))
        #     continue

        try:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 shell=True)
            output, error = p.communicate()
        except Exception as e:
            print(e)
            continue
        else:

            print('{} 下载好了!'.format(full_url))

            try:
                doc.insert({'url': full_url})
            except Exception as e:
                print(e)

funcition_map={'1':download_from_txt,
               '2':download_from_web}
option = sys.argv[1]
funcition_map.get(option)()

print('Done')
