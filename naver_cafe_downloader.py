import datetime
import json
import logging
import os
import random
import time
import urllib

import requests

logging.basicConfig(filename='./crawling.log', level=logging.DEBUG)

r_times = list(range(1, 7))


def _get_request_html(req_url):
    html = requests.get(req_url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}).text
    return html
    # return BeautifulSoup(html, 'html.parser')


def _create_dir(dirPath):
    try:
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
    except OSError:
        print('Error: Create directory.' + dirPath)


def get_contents(club_id: int, article_no: int, dir_name=None):
    time.sleep(random.choice(r_times))

    _create_dir(dir_name)

    article_api_url = 'https://apis.naver.com/cafe-web/cafe-articleapi/cafes/' + str(club_id) + '/articles/' + str(
        article_no) + '?query=&boardType=L&useCafeId=true&requestFrom=A'

    print(article_api_url)
    _result_text = _get_request_html(article_api_url)

    _result = json.loads(_result_text)

    max_image_count = 0
    max_video_count = 0

    _contentElements = _result['article']['contentElements']
    _subject = _result['article']['subject']

    if len(_contentElements) > 0:

        _content_dir = dir_name + "/" + (str(article_no) + "_" + _subject).strip()
        _create_dir(_content_dir)

        for idx, el in enumerate(_contentElements):

            if el['type'] == 'IMAGE':
                _image_url = el['json']['image']['url']

                '''
                https://cafeptthumb-phinf.pstatic.net 의 이미지경로는 썸네일이어서 파일 사이즈가 작아짐.
                따라서, https://cafefiles.pstatic.net의 경로로 다시 가져옴.
                '''
                _image_url = _image_url.replace('https://cafeptthumb-phinf.pstatic.net',
                                                'https://cafefiles.pstatic.net')

                urllib.request.urlretrieve(_image_url, _content_dir + "/" + str(
                    article_no) + "_image_" + str(idx) + ".jpg")

                max_image_count = max_image_count + 1

            if el['type'] == 'MOVIE':

                _vid = el['json']['vid']
                _inKey = el['json']['inKey']

                _video_api_url = 'https://apis.naver.com/rmcnmv/rmcnmv/vod/play/v2.0/' + _vid + '?key=' + _inKey + '&pid=rmcPlayer_15933305076787687&sid=5&ver=2.0&devt=html5_pc&doct=json&ptc=https&sptc=https&cpt=vtt&ctls=%7B%22visible%22%3A%7B%22fullscreen%22%3Atrue%2C%22logo%22%3Afalse%2C%22playbackRate%22%3Afalse%2C%22scrap%22%3Afalse%2C%22playCount%22%3Atrue%2C%22commentCount%22%3Atrue%2C%22title%22%3Atrue%2C%22writer%22%3Afalse%2C%22expand%22%3Afalse%2C%22subtitles%22%3Atrue%2C%22thumbnails%22%3Atrue%2C%22quality%22%3Atrue%2C%22setting%22%3Atrue%2C%22script%22%3Afalse%2C%22logoDimmed%22%3Atrue%2C%22badge%22%3Atrue%2C%22seekingTime%22%3Atrue%2C%22muted%22%3Atrue%2C%22muteButton%22%3Afalse%2C%22viewerNotice%22%3Afalse%2C%22linkCount%22%3Atrue%2C%22createTime%22%3Afalse%2C%22thumbnail%22%3Atrue%7D%2C%22clicked%22%3A%7B%22expand%22%3Afalse%2C%22subtitles%22%3Afalse%7D%7D&pv=4.18.41&dr=1920x1080&lc=ko_KR&videoId=D1CE2EB4D8DA6BE4F8CB5B6D9C178BE3077'
                _video_soup = _get_request_html(_video_api_url)
                _video_result_text = _video_soup

                _video_api_result = json.loads(_video_result_text)
                _video_list = _video_api_result['videos']['list']

                if len(_video_list) > 0:

                    for _idx, video in enumerate(_video_list):
                        _video_url = video['source']

                        urllib.request.urlretrieve(_video_url,
                                                   _content_dir + "/" + str(article_no) + "_video_" + str(
                                                       idx) + ".mp4")
                max_video_count = max_video_count + 1

        print('게시글(' + str(article_no) + ')의 ' + '이미지:' + str(max_image_count) + '개, ' + '동영상:' + str(
            max_video_count) + '개를 저장하였습니다.')
