import requests


def convert_bytes(bytes_number):
    tags = ["Byte", "Kilobyte", "Megabyte", "Gigabyte", "Terabyte"]

    i = 0
    double_bytes = bytes_number

    while i < len(tags) and bytes_number >= 1024:
        double_bytes = bytes_number / 1024.0
        i = i + 1
        bytes_number = bytes_number / 1024

    return str(round(double_bytes, 2)) + " " + tags[i]


class Main:
    def __init__(self):
        self.__url = "https://www.downloadlagu321.net"

    def get_data(self, query):
        array = []
        data = requests.get(
            self.__url + "/api/search/%s" % query.replace(" ", "%20")).json()
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
        url = requests.get(new % raw_link).json().get("url")

        if url:
            get_size = requests.get(url, stream=True)
            size = get_size.headers.get("Content-Length")
            if size:
                real = convert_bytes(int(size))
                if 7200000 >= int(size):
                    with open(filename, "wb") as f:
                        response = requests.get(url)
                        f.write(response.content)
                        return True
                else:
                    return False


c = Main()
c.get_source("6oi5_UyUnds", "asu")
