import requests
import re
import json
import os
import subprocess
from multiprocessing import Process


headers = {
'referer': 'https://www.bilibili.com',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50'
}
bv = 'BV1zU4y1F7vi'
url = 'https://www.bilibili.com/video/%s' % bv
save_path = './temp/'


def download(target_url, flag):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    r = requests.get(url=target_url, headers=headers)
    print('---- 正在下载 ----')
    if r.status_code == 200:
        with open(save_path + bv + '.' + flag, 'wb') as f:
            f.write(r.content)
        print('---- 下载完成 ----')
    else:
        print(r.status_code)


if __name__ == '__main__':
    r = requests.get(url=url, headers=headers)
    result = re.findall(r'<script>window.__playinfo__=(.*?)</script>', r.text, re.DOTALL)
    assert len(result) > 0
    play_info = result[0]
    play_info = json.loads(play_info)
    video_list = play_info['data']['dash']['video']
    audio_list = play_info['data']['dash']['audio']
    assert len(video_list) > 0
    assert len(audio_list) > 0
    video_url = video_list[0]['baseUrl']
    audio_url = audio_list[0]['baseUrl']
    print('video_url:', video_url)
    print('audio_url:', audio_url)
    p1 = Process(target=download, args=(video_url, 'flv'))
    p2 = Process(target=download, args=(audio_url, 'mp3'))
    p1.start()
    p1.join()
    p2.start()
    p2.join()
    print('---- 正在合并视频 ----')
    cmd = "ffmpeg -i ./temp/{}.flv -i ./temp/{}.mp3 -c:v copy -c:a aac -strict experimental ./temp/{}.mp4".format(bv, bv, bv)
    if subprocess.call(cmd, shell=True):
        raise Exception("{} 执行失败".format(cmd))
    else:    
        print('---- 视频合并完成 ----')
