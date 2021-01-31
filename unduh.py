import requests
import eyed3


class Main:
    def __init__(self):
        self.__url = "https://www.downloadlagu321.net"

    def get_data(self, query):
        array = []
        data = requests.get(
            self.__url + "/api/search/%s" % query.replace(" ", "%20"), verify=False
        ).json()
        if len(data) != 0:
            array.extend(
                [
                    {
                        "judul": item.get("title"),
                        "id": item.get("id"),
                    }
                    for item in data
                ]
            )
        return array

    def get_source(self, raw_link, filename):
        # url = "https://michaelbelgium.me/ytconverter/convert.php?youtubelink=https://www.youtube.com/watch?v="
        new = "https://nuubi.herokuapp.com/api/y2mate/download/mp3?url=https://www.youtube.com/watch?v=%s&quality=128"
        url = requests.get(new % raw_link).json()

        if url.get("url"):
            get_size = requests.get(url.get("url"), stream=True)
            size = get_size.headers.get("Content-Length")
            if size:
                if 7200000 >= int(size):
                    with open(filename, "wb") as f:
                        response = requests.get(url.get('url'))
                        f.write(response.content)
                    with open("thumb-" + filename, "rb") as f:
                        f.write(requests.get(url.get("thumbnail")).content)
                    audio = eyed3.load(now)
                    audio.tag.title = url.get("judul")
                    audio.tag.artist = "Ismrwtbot"
                    audio.tag.album = "Ismi Downloader"
                    audio.tag.images.set(
                        3, open("thumb-" + now).read(), "images/jpeg")
                    audio.tag.save()
                    return True
                else:
                    return False


c = Main()
c.get_source("6oi5_UyUnds", "asu")
