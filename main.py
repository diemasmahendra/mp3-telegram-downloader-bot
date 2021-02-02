from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from flask import Flask, request
from unduh import Main
import telepot
import time
import os

app = Flask(__name__)

bot = telepot.Bot("1468139592:AAFoNdHFTpOWWeYQAyT4yAWbQ3Y6mPb-j_0")

MESSAGES_NOW = []
AFTER_DOWNLOAD = []


class Downloader:
    def __init__(self, Token: None = str):
        self.__position = []
        self._bot = None
        self._song = Main()

    def download(self, uid, query, ytlink=False, delete=None):
        judul = str(int(time.time())) + ".mp3"
        stts = self._song.get_source(query, judul, ytlink=ytlink)
        if delete:
            for index, item in enumerate(delete):
                if uid == item["uid"]:
                    del_msg = telepot.message_identifier(item["identifier"])
                    bot.deleteMessage(del_msg)
                    delete.pop(index)
        if stts["success"]:
            bot.sendAudio(uid, open(judul, "rb"), title=stts.get("judul"))
        else:
            bot.sendMessage(uid, stts.get("msg"), parse_mode="Markdown")

    def inline_markup(self, new_msg):
        uid = new_msg["message"]["chat"]["id"]
        for count, msg in enumerate(MESSAGES_NOW):
            if msg["uid"] == uid:
                MESSAGES_NOW.pop(count)  # Delete element if user reply
                delete = msg["identifier"]
                data = new_msg["message"]["reply_markup"]["inline_keyboard"]
                for item in data:
                    if item[0]["callback_data"] == new_msg["data"]:
                        judul = item[0]["text"]
                        ident = telepot.message_identifier(delete)
                        bot.editMessageReplyMarkup(ident, reply_markup=None)
                        pesan = "Downloading *%s*" % judul
                        down = bot.editMessageText(
                            ident, pesan, parse_mode="Markdown")
                        AFTER_DOWNLOAD.append(dict(uid=uid, identifier=down))
                        self.download(
                            uid, new_msg["data"], delete=AFTER_DOWNLOAD)
        return

    def _received_msg(self, new_msg):
        uid = new_msg["message"]["chat"]["id"]
        pesan = new_msg["message"].get("text")
        if pesan:
            for count, msg in enumerate(MESSAGES_NOW):
                if msg["uid"] == uid:
                    # Delete element if user reply
                    MESSAGES_NOW.pop(count)
                    delete = msg["identifier"]
                    ident = telepot.message_identifier(delete)
                    bot.editMessageReplyMarkup(ident, reply_markup=None)
            if str(uid) in str(self.__position):
                for index, element in enumerate(self.__position):
                    if uid == element["uid"]:
                        if element["position"] == "dl":
                            self.__position.pop(index)
                        if element["position"] == "yt":
                            self.__position.pop(index)
                            return self.download(uid, pesan, ytlink=True)
                self._select_song(uid, pesan)
            else:

                if pesan.startswith("/dl"):
                    query = pesan.split(" ", maxsplit=1)
                    if len(query) == 1:
                        markup = ForceReply(selective=False)
                        pesan = "Ok, berikan saya query lagu yang mau dicari"
                        bot.sendMessage(uid, pesan, reply_markup=markup)
                        self.__position.append(dict(uid=uid, position="dl"))
                    else:
                        self._select_song(uid, query[1])
                elif pesan.startswith("/yt"):
                    url = pesan.split(" ", maxsplit=1)
                    if len(url) == 1:
                        markup = ForceReply(selective=False)
                        pesan = "Ok, berikan saya link youtubenya"
                        bot.sendMessage(uid, pesan, reply_markup=markup)
                        self.__position.append(dict(uid=uid, position="yt"))
                    else:
                        self.download(uid, url[1], ytlink=True)
                elif pesan.startswith("/start"):
                    pesan += "/dl [query]\n"
                    pesan += "Contoh:\n"
                    pesan += "/dl Noah\n\n\t"
                    pesan += "/yt [url]\n"
                    pesan += "Contoh:\n\t"
                    pesan += "/yt https://youtu.be/y6e_kztXG04"
                    bot.sendMessage(uid, pesan, disable_web_page_preview=True)
                else:
                    pesan = "Pesan tidak dikenali\n"
                    pesan += "/dl [query]\n"
                    pesan += "Contoh:\n"
                    pesan += "/dl Noah\n\n\t"
                    pesan += "/yt [url]\n"
                    pesan += "Contoh:\n\t"
                    pesan += "/yt https://youtu.be/y6e_kztXG04"
                    bot.sendMessage(uid, pesan, disable_web_page_preview=True)
        else:
            bot.sendMessage(uid, "Bot hanya mengenali pesan yang berupa text ")

    def _select_song(self, uid, query):
        arr = []
        results = self._song.get_data(query)
        if len(results) != 0:
            for item in results:
                arr.append(
                    [InlineKeyboardButton(
                        text=item["judul"], callback_data=item["id"])]
                )
            markup = InlineKeyboardMarkup(inline_keyboard=arr)
            for count, cek in enumerate(MESSAGES_NOW):
                if cek["uid"] == uid:
                    del_msg = telepot.message_identifier(cek["identifier"])
                    bot.deleteMessage(del_msg)
                    MESSAGES_NOW.pop(count)
            text = bot.sendMessage(uid, "Select song", reply_markup=markup)
            data = {"uid": uid, "identifier": text}
            MESSAGES_NOW.append(data)
        else:
            pesan = "Query *%s* tidak ditemukan" % query
            bot.sendMessage(uid, pesan, parse_mode="Markdown")
        return "ok"


mp = Downloader()


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        new_msg = request.get_json()
        if "message" in str(new_msg):
            if new_msg.get("message"):
                mp._received_msg(new_msg)
            else:
                if new_msg.get("callback_query"):
                    mp.inline_markup(new_msg["callback_query"])
        return "ok"
    else:
        return "Ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(
        os.environ.get("PORT", "5000")), debug=True)
