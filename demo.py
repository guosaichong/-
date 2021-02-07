
import requests
import os
import aiohttp
import asyncio

# 获得每段视频的url


def get_url_list():

    prefix_url = "https://youku.com-youku.net/20180626/14085_604c6726/1000k/hls/"
    with open("./index.m3u8", "r")as f:
        content = f.read()
        # print(content)
        content_list = content.split("\n")
        # print(content_list)
        url_list = []
        for i in content_list:
            if ".ts" in i:

                url_list.append(prefix_url + i)
        print(url_list)
    # print(len(url_list))
    return url_list
# 根据url下载视频并保存


def download(url_list):
    if not os.path.exists("video"):
        os.makedirs("video")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
    for url in url_list:
        resp = requests.get(url, headers=headers)
        with open("video/"+url.split("/")[-1], "wb")as f:
            f.write(resp.content)


async def job(session, url):
    # 声明为异步函数
    name = url.split('/')[-1]
    # 获得名字
    ts = await session.get(url)
    # 触发到await就切换，等待get到数据
    tscode = await ts.read()
    # 读取内容
    with open("video/"+str(name), "wb") as fout:
        # 写入文件
        fout.write(tscode)
    return str(url)


async def main(loop, url):
    async with aiohttp.ClientSession() as session:
        # 建立会话 session
        tasks = [loop.create_task(job(session, url[_]))
                 for _ in range(len(get_url_list()))]
        # 建立所有任务
        finshed, unfinshed = await asyncio.wait(tasks)
        # 触发await，等待任务完成
        all_results = [r.result() for r in finshed]
        # 获取所有结果
        print("ALL RESULTS:" + str(all_results))
# 视频合并


def join_video(x, y):
    filedir = r"video"
    new_file = "%s\out.ts" % filedir
    f = open(new_file, "wb")
    for i in range(x, y):
        filepath = "%s\98dd3b961ba%03d.ts" % (filedir, i)
        for line in open(filepath, "rb"):
            f.write(line)
        f.flush()
    f.close()


if __name__ == "__main__":
    # 单独下载
    # url_list = ["https://youku.com-youku.net/20180626/14085_604c6726/1000k/hls/98dd3b961ba086.ts"]
    # download(url_list)

    # 批量下载
    # if not os.path.exists("video"):
    #     os.makedirs("video")
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main(loop, get_url_list()))

    join_video(0,836)
