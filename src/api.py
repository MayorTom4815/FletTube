from dataclasses import dataclass
import pytubefix as pt
from os.path import expandvars, expanduser


@dataclass
class Video:
    title: str = "Untitled"
    author: str = "John Doe"
    thumbnail: str = "no_image.png"
    url: str = "https://www.youtube.com/watch?v=Pgn-BSNgirk"


def query_video(url: str) -> Video:
    try:
        yt = pt.YouTube(url)
        return Video(
            title=yt.title, author=yt.author, thumbnail=yt.thumbnail_url, url=url
        )

    except:
        return Video()


def download_video(url: str, path: str, only_sound: bool) -> None:
    try:
        yt = pt.YouTube(url)
        stream = (
            yt.streams.get_audio_only()
            if only_sound
            else yt.streams.get_highest_resolution()
        )
        stream.download(output_path=expanduser(path))

    except:
        pass
