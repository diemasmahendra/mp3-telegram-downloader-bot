from bs4 import BeautifulSoup as bs
import requests
import sys
import re


class Main:
    def __init__(self):
        self.__url = "https://www.downloadlagu321.net"

    def get_data(self, query):
        array = []
        data = requests.get(
            self.__url + "/api/search/%s" % query.replace(" ", "%20"), verify=False
        ).json()
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
        url = "https://michaelbelgium.me/ytconverter/convert.php?youtubelink=https://www.youtube.com/watch?v="
        url = requests.get(url + raw_link).json().get('file')
        if url:
            with open(filename, "wb") as f:
                response = requests.get(url)
                f.write(response.content)
                return True
        else:
            return False
