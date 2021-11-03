import requests
import re
import json
import os
import subprocess
import argparse
from multiprocessing import Process


headers = {
'referer': 'https://www.bilibili.com',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50'
}
base_url = 'https://www.bilibili.com/video/'
save_path = './temp/'


def parse(bv):
    res = []
    url = base_url + bv
    r = requests.get(url=url, headers=headers)
    result = re.findall(r'<script>window.__INITIAL_STATE__=(.*?);.*?</script>', r.text, re.DOTALL)
    if len(result) == 0:
        return res
    video_info = json.loads(result[0])
    pages = video_info['videoData']['pages']
    print('视频选集(*代表全部视频)')
    for index, page in enumerate(pages):
        print(index, page['part'])
    input_text = input()
    cid_list = []
    if input_text == '*':
        for page in pages:
            cid_list.append(page['cid'])
    else:
        cid_list.append(pages[int(input_text)]['cid'])
    flag = True
    select = -1
    for cid in cid_list:
        request_url = 'https://api.bilibili.com/x/player/playurl?cid={}&bvid={}&qn=0&type=&otype=json&fourk=1&fnver=0&fnval=976'.format(cid, bv)
        resp = requests.get(url=request_url, headers=headers)
        json_obj = json.loads(resp.text)
        accept_description = json_obj['data']['accept_description']
        audio_list = json_obj['data']['dash']['audio']
        video_list = json_obj['data']['dash']['video']
        k = len(video_list) // 2
        if flag:
            flag = False
            print('请选择视频清晰度')
            for i in range(k):
                print(i, accept_description[len(accept_description)-i-1])
            input_text = input()
            i = int(input_text)
            select = i
        n = len(video_list)
        audio_url = audio_list[0]['baseUrl']
        video_url = video_list[n-(2*select+2)]['baseUrl']
        res.append({'video': video_url, 'audio': audio_url, 'cid': cid})
    return res


def download(target_url, cid, flag):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    r = requests.get(url=target_url, headers=headers)
    print('---- 正在下载 ----')
    if r.status_code == 200:
        with open(save_path + str(cid) + '.' + flag, 'wb') as f:
            f.write(r.content)
        print('---- 下载完成 ----')
    else:
        print('下载失败', r.status_code)


def merge(cid):
    cid = str(cid)
    print('---- 正在合并视频 ----')
    cmd = "ffmpeg -i ./temp/{}.mp4 -i ./temp/{}.mp3 -c:v copy -c:a aac -strict experimental ./temp/{}_completed.mp4".format(cid, cid, cid)
    if subprocess.call(cmd, shell=True):
        raise Exception("{} 执行失败".format(cmd))
    else:
        print('---- 视频合并完成 ----')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='哔哩哔哩')
    parser.add_argument('-bv', required=True)
    args = parser.parse_args()
    bv = args.bv
    result = parse(bv)
    for item in result:
        p1 = Process(target=download, args=(item['video'], item['cid'], 'mp4'))
        p2 = Process(target=download, args=(item['audio'], item['cid'], 'mp3'))
        p1.start()
        p1.join()
        p2.start()
        p2.join()
        merge(item['cid'])
