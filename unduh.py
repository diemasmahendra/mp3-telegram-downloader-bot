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

    def get_source(self, raw_link, filename, ytlink=False):
        # url = "https://michaelbelgium.me/ytconverter/convert.php?youtubelink=https://www.youtube.com/watch?v="
        if ytlink:
            new = (
                "https://nuubi.herokuapp.com/api/y2mate/download/mp3?url=%s&quality=128"
            )
        else:
            new = "https://nuubi.herokuapp.com/api/y2mate/download/mp3?url=https://www.youtube.com/watch?v=%s&quality=128"
        url = requests.get(new % raw_link).json()

        if url.get("url"):
            get_size = requests.get(url.get("url"), stream=True)
            size = get_size.headers.get("Content-Length")
            if size:
                if 7200000 >= int(size):
                    with open(filename, "wb") as f:
                        response = requests.get(url.get("url"))
                        f.write(response.content)
                    with open("thumb-" + filename.split(".")[0] + ".jpg", "wb") as f:
                        f.write(requests.get(url.get("thumbnail")).content)
                    audio = eyed3.load(filename)
                    audio.tag.title = url.get("judul")
                    audio.tag.artist = "Ismrwtbot"
                    audio.tag.album = "Ismi Downloader"
                    audio.tag.images.set(
                        3,
                        open("thumb-" + filename.split(".")
                             [0] + ".jpg").read(),
                        "image/jpeg",
                    )
                    audio.tag.save()
                    return dict(success=True, judul=url.get("judul"))
                else:
                    return dict(success=False, judul=None, msg="Ukuran %s Kebesaran. Minimal 7 Mb" % url.get('judul'))
        else:
            return dict(success=False, judul=None, msg=url.get("error"))


# c = Main()
# c.get_source("6oi5_UyUnds", "asu.mp3")
