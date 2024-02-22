import json
import logging
import os
import random
import ssl
import time
import urllib

import requests
from bs4 import BeautifulSoup

logging.basicConfig(filename="./crawling.log", level=logging.DEBUG)
ssl._create_default_https_context = ssl._create_unverified_context

r_times = list(range(1, 7))


def _get_request_html(req_url):
    html = requests.get(
        req_url,
        timeout=60,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/35.0.1916.47 Safari/537.36"
        },
    ).text
    return html
    # return BeautifulSoup(html, 'html.parser')


def _create_dir(dir_path: str):
    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        print(f"dir:  {dir_path} created")
    except OSError:
        print("Error: Create directory." + dir_path)


def get_contents(club_id: int, article_no: int, dir_name="Downloads"):
    time.sleep(random.choice(r_times))

    article_api_url = (
        f"https://apis.naver.com/cafe-web/cafe-articleapi/cafes/"
        f"{club_id}/articles/{article_no}?"
        f"query=&boardType=L&useCafeId=true&requestFrom=A"
    )

    _result_text = _get_request_html(article_api_url)

    _result = json.loads(_result_text)

    max_image_count = 0
    max_video_count = 0

    # if _result.get('article') is not None:
    _content_elements = _result["article"]["contentElements"]
    _subject = _result["article"]["subject"]

    # _content_dir = dir_name + "/" + (str(article_no) + "_" + _subject).strip()
    _content_dir = dir_name + "/" + (str(article_no)).strip()
    _create_dir(_content_dir)

    video_list = []
    image_list = []

    soup = BeautifulSoup(_result["article"]["content"], "html.parser")
    if soup.select_one("script") is not None:
        script_text = soup.select_one("script").get("data-module")
        json_data = json.loads(script_text)
        if json_data["type"] == "v2_video":
            vid = json_data["data"]["vid"]
            inkey = json_data["data"]["inkey"]
            _video_list = _get_video_list(in_key=inkey, vid=vid)
            video_list.extend(_video_list)

    if len(_content_elements) > 0:
        for idx, el in enumerate(_content_elements):
            print(f"{idx}번째 content element")
            if el["type"] == "IMAGE":
                _image_url = el["json"]["image"]["url"]

                """
                https://cafeptthumb-phinf.pstatic.net 의 이미지경로는 썸네일이어서 파일 사이즈가 작아짐.
                따라서, https://cafefiles.pstatic.net의 경로로 다시 가져옴.
                """

                try:
                    if "https://dthumb-phinf.pstatic.net" in _image_url:
                        _ps = urllib.parse.parse_qs(_image_url)
                        _keys = _ps.keys()

                        for _k in _keys:
                            _iu = _ps[_k][0]
                            _iu = _iu.replace('"', "")

                            image_list.append(_iu)
                    else:
                        image_list.append(_image_url)

                    max_image_count += 1
                except urllib.error.HTTPError:
                    print("not found")

            if el["type"] == "MOVIE":
                _vid = el["json"]["vid"]
                _in_key = el["json"]["inKey"]

                _video_list = _get_video_list(in_key=_in_key, vid=_vid)

                video_list.extend(_video_list)

    if len(video_list) > 0:
        for _idx, video in enumerate(video_list):
            _video_url = video["source"]
            video_name = f"{article_no}_video_{_idx}.mp4"
            video_full_name = _content_dir + "/" + video_name
            download_image(url=_video_url, file_path=video_full_name)
            max_video_count += 1

    if len(image_list) > 0:
        for _idx, image in enumerate(image_list):
            _image_url = image
            img_name = f"{article_no}_image_{_idx}.jpg"
            img_full_name = _content_dir + "/" + img_name
            download_image(url=_image_url, file_path=img_full_name)
            max_image_count += 1

    print(
        f"게시글({article_no})의 이미지: {max_image_count}개, 동영상: {max_video_count}개를 저장하였습니다."
    )


def _get_video_list(vid, in_key):
    _video_api_url = (
        f"https://apis.naver.com/rmcnmv/rmcnmv/vod/play/v2.0/{vid}?"
        f"key={in_key}&pid=rmcPlayer_15933305076787687&sid=5&ver=2.0&"
        f"devt=html5_pc&doct=json&ptc=https&sptc=https&cpt=vtt&"
        f"ctls=%7B%22visible%22%3A%7B%22fullscreen%22%3Atrue%2C%22logo"
        f"%22%3Afalse%2C%22playbackRate%22"
        f"%3Afalse%2C%22scrap%22%3Afalse%2C%22playCount%22%3Atrue%2C"
        f"%22commentCount%22%3Atrue%2C"
        f"%22title%22%3Atrue%2C%22writer%22%3Afalse%2C%22expand"
        f"%22%3Afalse%2C%22subtitles%22%3Atrue%2C"
        f"%22thumbnails%22%3Atrue%2C%22quality%22%3Atrue%2C%22setting"
        f"%22%3Atrue%2C%22script%22%3Afalse"
        f"%2C%22logoDimmed%22%3Atrue%2C%22badge%22%3Atrue%2C%22seekingTime"
        f"%22%3Atrue%2C%22muted%22"
        f"%3Atrue%2C%22muteButton%22%3Afalse%2C%22viewerNotice%22"
        f"%3Afalse%2C%22linkCount%22%3Atrue%2C"
        f"%22createTime%22%3Afalse%2C%22thumbnail%22%3Atrue%7D%2C"
        f"%22clicked%22%3A%7B%22expand%22"
        f"%3Afalse%2C%22subtitles%22%3Afalse%7D%7D&"
        f"pv=4.18.41&dr=1920x1080&lc=ko_KR&videoId"
        f"=D1CE2EB4D8DA6BE4F8CB5B6D9C178BE3077"
    )
    _video_soup = _get_request_html(_video_api_url)
    _video_result_text = _video_soup
    _video_api_result = json.loads(_video_result_text)
    _video_list = _video_api_result["videos"]["list"]
    return _video_list


def download_image(url: str, file_path: str):
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
        },
    )

    with urllib.request.urlopen(req) as response:
        data = response.read()

    with open(file_path, "wb") as img_file:
        img_file.write(data)
