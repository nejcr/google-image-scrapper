# pip install requests
import abc
import html
import json
import os
import re

import requests

IMAGES_DIR = "../images/"

image_storage = []


class ParsedImage:
    @abc.abstractclassmethod
    def get_image_src(self):
        pass


class GoogleImage(ParsedImage):
    def __init__(self, json_image):
        self.id = json_image["id"]
        self.height = json_image["oh"]
        self.width = json_image["ow"]
        self.description1 = json_image["pt"]
        self.description2 = json_image["s"]
        self.source_url = json_image["isu"]
        self.image_src = json_image["ou"]

    def get_human_size(self):
        return str(self.height) + "x" + str(self.width)

    def get_image_src(self):
        return self.image_src(self)


def make_dir(search_keyword):
    final_dir = IMAGES_DIR + search_keyword.replace(" ", "_").replace("+", "-")
    if os.path.isdir(final_dir):

        return final_dir + "/"
    else:
        os.makedirs(final_dir)
        return final_dir + "/"


def parse_google(keyword):
    # TODO Accept param search
    google_url = 'https://www.google.si/search?q={0}&espv=1&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg&iact=ms&start=250&num=230'

    request_header = {"User-Agent":
                          "Mozilla/5.0 (Windows NT 6.1) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/41.0.2228.0 "
                          "Safari/537.36"}

    escaped_keyword = html.escape(keyword)
    site = requests.get(url=google_url.format(escaped_keyword), headers=request_header).content.decode("utf-8")
    raw_data = re.finditer('({"clt":|{"cb":|{"cl":).+?(?=<)', site)
    for raw_image in raw_data:
        json_image = json.loads(raw_image.group(0))
        print(json_image)
        image_storage.append(GoogleImage(json_image))


def download_and_store(base_directory, filename_keyword):
    iteration = 1
    for image in image_storage:
        print(image.image_src)
        response = requests.get(image.image_src)
        binary_file = response.content
        if response.status_code == 200:
            file_type = image.image_src.split("/")[-1]
            if file_type.endswith((".jpg", ".png", ".bmp", "tiff", "bmp")):
                file_name = base_directory + filename_keyword + "_" + str(
                    iteration) + "_" + image.get_human_size() + "." + file_type.split(".")[-1]
                with open(file_name, "w") as file:
                    file.write(binary_file)

        iteration = iteration + 1


def go():
    search_keyword = "monkey"
    parse_google(search_keyword)
    download_and_store(make_dir(search_keyword), search_keyword)


go()
