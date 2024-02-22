import datetime
import os

import click
from naver_cafe.naver_cafe_downloader import get_contents, _create_dir


def get_next_sunday():
    today = datetime.datetime.today()
    diff = (6 - today.weekday()) % 7
    last_sun = today + datetime.timedelta(days=diff)
    return last_sun.strftime("%Y.%m.%d")


_next_sun_str = get_next_sunday()
CLUB_ID = 30012903


@click.command()
@click.option(
    "-c", "--club_id", default=CLUB_ID, required=True, type=int, help="네이버카페 클럽ID"
)
@click.option(
    "-a", "--articles", multiple=True, required=True, type=int, help="네이버카페 게시글번호"
)
@click.option("-d", "--base_dir", default=_next_sun_str, required=False, help="디렉토리명")
def cli(club_id, articles, base_dir):
    """네이버카페에서 게시된 글의 컨텐츠(이미지, 동영상)을 다운받기."""
    user_home = os.path.expanduser("~")
    save_dir = user_home + "/Downloads/" + base_dir
    _create_dir(save_dir)

    for _article in articles:
        get_contents(club_id, _article, save_dir)


if __name__ == "__main__":
    # cli()
    # cli(article_no=1926)
    user_home = os.path.expanduser("~")
    save_dir = user_home + "/Downloads/" + "a"
    get_contents(30012903, 1926, dir_name=save_dir)
