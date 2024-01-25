import datetime
import click
from naver_cafe.naver_cafe_downloader import get_contents


def get_next_sunday():
    today = datetime.datetime.today()
    diff = (6 - today.weekday()) % 7
    last_sun = today + datetime.timedelta(days=diff)
    return last_sun.strftime("%Y.%m.%d")


_next_sun_str = get_next_sunday()
_club_id = 30012903


@click.command()
@click.option('-c', '--club_id', default=_club_id, required=True, type=int, help='네이버카페 클럽ID')
@click.option('-a', '--articles', multiple=True, required=True, type=int, help='네이버카페 게시글번호')
@click.option('-d', '--dir', default=_next_sun_str, required=False, help='디렉토리명')
def cli(club_id, articles, dir):
    """네이버카페에서 게시된 글의 컨텐츠(이미지, 동영상)을 다운받기."""

    for _article in articles:
        get_contents(club_id, _article, dir)


if __name__ == '__main__':
    cli()
