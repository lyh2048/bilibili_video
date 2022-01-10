import requests
import json
import os
import math
import subprocess
from config import *
from tqdm import tqdm


class VideoDownload:
    def __init__(self, video_url, output) -> None:
        self.video_url = video_url
        self.output = output
        self.headers = {
            'referer': 'https://www.bilibili.com',
            'user-agent': UA
        }
        self.request = requests.Session()
        self.bv = None
        self.page_list = None
        self.cid_list = []
        self.download_url_list = []

    def run(self):
        # 创建临时文件夹
        if not os.path.exists(TEMP_PATH):
            os.makedirs(TEMP_PATH)
        try:
            self.check_video_url()
            self.get_video_info()
            self.show_page_list()
            if len(self.page_list) <= 1:
                self.cid_list.append(self.page_list[0]['cid'])
            else:
                page_str = input('请输入要下载的P号，多个P号用英文逗号分隔，*表示全部下载\r\n')
                if page_str == "*":
                    for item in self.page_list:
                        self.cid_list.append(item['cid'])
                else:
                    page_no_list = page_str.split(',')
                    for item in page_no_list:
                        index = int(item.strip())
                        if index <= len(self.page_list):
                            self.cid_list.append(self.page_list[index-1]['cid'])
            self.get_download_url()
            for item in self.download_url_list:
                self.download_and_merge(item)
        except Exception as e:
            print("Error: %s" % e)
            exit(-1)

    def get_video_info(self):
        resp = self.request.get(f'https://api.bilibili.com/x/player/pagelist?bvid={self.bv}&jsonp=jsonp', headers=self.headers)
        resp = json.loads(resp.text)
        if resp['code'] != 0:
            raise Exception('获取视频列表失败')
        self.page_list = resp['data']
        self.page_list = list(map(lambda item: {'cid': item['cid'], 'page': item['page'], 'name': item['part']}, self.page_list))

    def check_video_url(self):
        if 'bilibili.com/video' not in self.video_url:
            raise Exception('视频URL错误')
        # 提取视频URL中的bv号
        bv = self.video_url.split('?')[0].split('/')[-1]
        self.bv = bv

    def show_page_list(self):
        for item in self.page_list:
            print(item)

    def get_download_url(self):
        for cid in self.cid_list:
            resp = self.request.get(f'https://api.bilibili.com/x/player/playurl?cid={str(cid)}&bvid={self.bv}&qn=0&type=&otype=json&fourk=1&fnver=0&fnval=976', headers=self.headers)
            resp = json.loads(resp.text)
            if resp['code'] != 0:
                raise Exception(resp['message'])
            video = resp['data']['dash']['video'][0]['baseUrl']
            audio = resp['data']['dash']['audio'][0]['baseUrl']
            self.download_url_list.append({
                'cid': cid,
                'bv': self.bv,
                'video': video,
                'audio': audio
            })
    
    def download_and_merge(self, item):
        video_name = item['bv'] + '_' + str(item['cid']) + '.mp4'
        audio_name = item['bv'] + '_' + str(item['cid']) + '.mp3'
        print('正在下载视频: %s' % video_name)
        self.download(item['video'], video_name)
        print('正在下载音频: %s' % audio_name)
        self.download(item['audio'], audio_name)
        video_path = os.path.join(TEMP_PATH, video_name)
        audio_path = os.path.join(TEMP_PATH, audio_name)
        output_path = os.path.join(self.output, video_name)
        print("正在合并视频: %s" % video_name)
        cmd = f"ffmpeg -i {video_path} -i {audio_path} -c:v copy -c:a aac -strict experimental {output_path}"
        if subprocess.call(cmd, shell=False):
            raise Exception("{}执行失败".format(cmd))

    def download(self, url, name):
        head = self.request.head(url=url, headers=self.headers)
        file_size = head.headers.get('Content-Length')
        if file_size is not None:
            file_size = int(file_size)
        else:
            file_size = 0
        resp = self.request.get(url=url, headers=self.headers, stream=True)
        chunk_size = 1024*1024
        path = os.path.join(TEMP_PATH, name)
        with open(path, 'wb') as f:
            for chunk in tqdm(iterable=resp.iter_content(chunk_size), total=math.ceil(file_size/1024/1024), desc='正在下载', unit='MB'):
                f.write(chunk)