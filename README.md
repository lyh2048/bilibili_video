# 哔哩哔哩 (゜-゜)つロ 干杯~

[![License](assets/License-MIT%20License-blue.svg)](https://opensource.org/licenses/MIT)

[![哔哩哔哩](assets/e5281b0f1a5987c8213018010d985d6e95a96e40.png)](https://www.bilibili.com/)

## 简介

基于`Python`的B站视频下载工具，实现了基本的下载功能，但仍存在许多不足与bug。如果发现错误，还请在`Issues`中指出，欢迎`Fork`和`Pull requests`改善代码，谢谢！

## 需要

- `python`
- `ffmpeg`

## 运行

1. 克隆仓库

```bash
git clone https://github.com/lyh2048/bilibili_video.git
cd bilibili_video
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 运行

```bash
python main.py -url https://www.bilibili.com/video/BV1Gr4y1m7AD?spm_id_from=333.6.0.0 -output D:/哔哩哔哩
```



> usage: main.py [-h] -url URL [-output OUTPUT]
>
> 哔哩哔哩 (゜-゜)つロ 干杯~-bilibili
>
> optional arguments:
>   -h, --help      show this help message and exit
>   -url URL        视频的URL
>   -output OUTPUT  视频的保存位置

## 注意

由于项目使用了FFmpeg，因此在运行程序之前，请先安装好FFmpeg，并配置好环境变量。

[FFmpeg](https://ffmpeg.org/)

