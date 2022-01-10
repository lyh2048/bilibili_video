import argparse
from video_download import VideoDownload

'''
哔哩哔哩视频下载
'''

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='哔哩哔哩 (゜-゜)つロ 干杯~-bilibili')
    parser.add_argument('-url', type=str, required=True, help='视频的URL')
    parser.add_argument('-output', type=str, default='./', help='视频的保存位置')
    args = parser.parse_args()
    # 获取视频的URL
    video_url = args.url
    # 获取视频的保存路径
    output = args.output
    print('哔哩哔哩 (゜-゜)つロ 干杯~-bilibili')
    VideoDownload(video_url, output).run()